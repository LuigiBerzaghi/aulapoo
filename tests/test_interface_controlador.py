import random

from src.arqueiro import Arqueiro
from src.guerreiro import Guerreiro
from src.inimigo import ChefeFinal, Goblin, GuerreiroSombrio, Inimigo
from src.interface.controlador import ControladorBatalha, criar_heroi, criar_inimigo, inimigos_disponiveis
from src.mago import Mago


def sequencia_randint(monkeypatch, valores):
    valores = iter(valores)
    monkeypatch.setattr(random, "randint", lambda a, b: next(valores))


def test_ataque_captura_mensagens_sem_imprimir(capsys):
    controlador = ControladorBatalha(Guerreiro("Arthur"), Goblin())

    resultado = controlador.atacar()

    assert resultado.dano == 16
    assert controlador.inimigo.vida == 54
    assert any("Goblin sofre 16 de dano" in mensagem for mensagem in resultado.mensagens)
    assert capsys.readouterr().out == ""


def test_turno_inimigo_causa_dano_ao_jogador():
    controlador = ControladorBatalha(Guerreiro("Arthur"), Goblin())

    resultado = controlador.turno_inimigo()

    assert resultado.ator == "inimigo"
    assert resultado.dano == 8
    assert controlador.jogador.vida == 112


def test_golpe_fraco_e_bloqueado():
    controlador = ControladorBatalha(Guerreiro("Arthur"), Inimigo("Rato", 30, 5, 0))

    resultado = controlador.turno_inimigo()

    assert resultado.bloqueado is True
    assert controlador.jogador.vida == 120


def test_arqueiro_sem_flechas_nao_tem_sucesso():
    arqueiro = Arqueiro("Legolas")
    arqueiro.flechas = 0
    controlador = ControladorBatalha(arqueiro, Goblin())

    resultado = controlador.atacar()

    assert resultado.sucesso is False
    assert resultado.dano == 0


def test_magia_sem_mana_falha():
    mago = Mago("Merlin")
    mago.mana = 10
    controlador = ControladorBatalha(mago, Goblin())

    resultado = controlador.usar_magia()

    assert resultado.sucesso is False
    assert resultado.mana == 0
    assert controlador.inimigo.vida == 70


def test_magia_com_sucesso_gasta_mana(monkeypatch):
    controlador = ControladorBatalha(Mago("Merlin"), Goblin())
    sequencia_randint(monkeypatch, [3, 40, 5])

    resultado = controlador.usar_magia()

    assert resultado.sucesso is True
    assert resultado.mana == -20
    assert resultado.dano == 36
    assert resultado.critico is False


def test_magia_critica_e_detectada(monkeypatch):
    controlador = ControladorBatalha(Mago("Merlin"), Goblin())
    sequencia_randint(monkeypatch, [3, 30, 1])

    resultado = controlador.usar_magia()

    assert resultado.critico is True
    assert resultado.dano == 46


def test_usar_item_cura_e_remove_do_inventario():
    guerreiro = Guerreiro("Arthur")
    guerreiro.vida = 50
    controlador = ControladorBatalha(guerreiro, Goblin())

    resultado = controlador.usar_item(0)

    assert resultado.item.nome == "Poção de vida"
    assert resultado.cura == 20
    assert len(guerreiro.inventario) == 2


def test_troca_coloca_heroi_novo_com_vida_cheia():
    controlador = ControladorBatalha(Guerreiro("Arthur"), Goblin())
    controlador.jogador.vida = 10
    inimigo = controlador.inimigo

    resultado = controlador.trocar_personagem("mago")

    assert resultado.sucesso is True
    assert isinstance(controlador.jogador, Mago)
    assert controlador.jogador.vida == 80
    assert controlador.inimigo is inimigo


def test_chefe_ferido_usa_golpe_do_crepusculo():
    controlador = ControladorBatalha(Guerreiro("Arthur"), criar_inimigo(ChefeFinal))
    controlador.inimigo.vida = 50

    resultado = controlador.turno_inimigo()

    assert resultado.furia is True
    assert resultado.especial is True
    assert resultado.dano == 40


def test_criacao_de_personagens_e_oponentes():
    assert criar_inimigo(ChefeFinal).nome == "Mestre da Noite"
    assert isinstance(criar_heroi("arqueiro"), Arqueiro)
    assert GuerreiroSombrio not in inimigos_disponiveis(criar_heroi("guerreiro"))


def test_estado_e_rodadas():
    controlador = ControladorBatalha(Guerreiro("Arthur"), Goblin())

    assert controlador.estado() == "em_andamento"
    assert controlador.proxima_rodada() == 2
    controlador.inimigo.vida = 0
    assert controlador.estado() == "vitoria"
