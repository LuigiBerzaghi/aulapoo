"""Ponte entre a interface gráfica e a lógica do jogo.

Este módulo não depende do pygame: ele executa as ações através de ``Batalha``,
captura o que o jogo imprime no terminal e devolve um ``Resultado`` com o que
aconteceu, para que a interface possa animar cada evento.
"""

import io
from contextlib import redirect_stdout
from dataclasses import dataclass, field

try:
    from src.arqueiro import Arqueiro
    from src.batalha import Batalha
    from src.guerreiro import Guerreiro
    from src.inimigo import ChefeFinal
    from src.main import listar_inimigos_disponiveis
    from src.mago import Mago
except ModuleNotFoundError:
    from arqueiro import Arqueiro
    from batalha import Batalha
    from guerreiro import Guerreiro
    from inimigo import ChefeFinal
    from main import listar_inimigos_disponiveis
    from mago import Mago


HEROIS = {
    "guerreiro": (Guerreiro, "Arthur"),
    "mago": (Mago, "Merlin"),
    "arqueiro": (Arqueiro, "Legolas"),
}


def criar_heroi(chave):
    classe, nome = HEROIS[chave]
    return classe(nome)


def chave_personagem(personagem):
    return type(personagem).__name__.lower()


def criar_inimigo(classe):
    if classe is ChefeFinal:
        return ChefeFinal("Mestre da Noite")
    return classe()


def inimigos_disponiveis(heroi):
    return listar_inimigos_disponiveis(heroi)


@dataclass
class Resultado:
    ator: str
    acao: str
    mensagens: list = field(default_factory=list)
    dano: int = 0
    cura: int = 0
    mana: int = 0
    flechas: int = 0
    sucesso: bool = True
    critico: bool = False
    especial: bool = False
    furia: bool = False
    item: object = None

    @property
    def bloqueado(self):
        return self.sucesso and self.dano == 0 and self.acao in ("atacar", "magia", "turno_inimigo")


class ControladorBatalha:

    def __init__(self, jogador, inimigo):
        self.batalha = Batalha(jogador, inimigo)
        self.rodada = 1

    @property
    def jogador(self):
        return self.batalha.jogador

    @property
    def inimigo(self):
        return self.batalha.inimigo

    @property
    def pode_usar_magia(self):
        return hasattr(self.jogador, "usar_magia")

    def _foto(self):
        return {
            "vida_jogador": self.jogador.vida,
            "vida_inimigo": self.inimigo.vida,
            "mana": getattr(self.jogador, "mana", 0),
            "flechas": getattr(self.jogador, "flechas", 0),
        }

    def _executar(self, ator, acao, funcao, *argumentos):
        antes = self._foto()
        saida = io.StringIO()
        with redirect_stdout(saida):
            retorno = funcao(*argumentos)
        depois = self._foto()

        mensagens = [linha.strip() for linha in saida.getvalue().splitlines()]
        mensagens = [linha for linha in mensagens if linha and not linha.startswith("---")]
        texto = " ".join(mensagens)

        alvo = "vida_inimigo" if ator == "jogador" else "vida_jogador"
        resultado = Resultado(
            ator=ator,
            acao=acao,
            mensagens=mensagens,
            dano=antes[alvo] - depois[alvo],
            critico="crítico" in texto,
            especial="Crepúsculo" in texto,
            furia="fúria" in texto,
        )
        if ator == "jogador" and acao != "troca":
            resultado.cura = max(0, depois["vida_jogador"] - antes["vida_jogador"])
            resultado.mana = depois["mana"] - antes["mana"]
            resultado.flechas = depois["flechas"] - antes["flechas"]
        return resultado, retorno

    def atacar(self):
        sem_flechas = getattr(self.jogador, "flechas", 1) <= 0
        resultado, _ = self._executar("jogador", "atacar", self.jogador.atacar, self.inimigo)
        resultado.sucesso = not sem_flechas
        return resultado

    def usar_magia(self):
        resultado, retorno = self._executar("jogador", "magia", self.jogador.usar_magia, self.inimigo)
        resultado.sucesso = retorno is True
        return resultado

    def usar_item(self, indice):
        item = self.jogador.inventario[indice]
        resultado, retorno = self._executar("jogador", "item", self.batalha.usar_item, item)
        resultado.sucesso = retorno is True
        resultado.item = item
        return resultado

    def trocar_personagem(self, chave):
        novo = criar_heroi(chave)
        resultado, retorno = self._executar("jogador", "troca", self.batalha.trocar_personagem, novo)
        resultado.sucesso = retorno is True
        return resultado

    def turno_inimigo(self):
        resultado, _ = self._executar("inimigo", "turno_inimigo", self.batalha.turno_inimigo)
        return resultado

    def proxima_rodada(self):
        self.rodada += 1
        return self.rodada

    def estado(self):
        return self.batalha.condicao_vitoria()
