try:
    from src.personagem import Personagem
except ModuleNotFoundError:
    from personagem import Personagem


class Inimigo(Personagem):
    incompativeis = []

    def __init__(self, nome, vida, ataque, defesa, tipo="inimigo"):
        super().__init__(
            nome=nome,
            vida=vida,
            ataque=ataque,
            defesa=defesa,
            vida_maxima=vida,
        )
        self.tipo = tipo

    @classmethod
    def pode_enfrentar(cls, classe_heroi):
        nome_heroi = classe_heroi.__name__ if isinstance(classe_heroi, type) else classe_heroi
        return nome_heroi not in getattr(cls, "incompativeis", [])

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} salta para a frente e ataca {alvo.nome}!",
            f"{self.nome} desferiu um golpe rápido sobre {alvo.nome}!",
            f"{self.nome} aproveita a abertura e acerta {alvo.nome}!"
        ]
        print(mensagens[1])
        alvo.receber_dano(self.ataque)

    def ataque_especial(self, alvo):
        self.atacar(alvo)


class Goblin(Inimigo):

    def __init__(self, nome="Goblin"):
        super().__init__(nome=nome, vida=70, ataque=18, defesa=4, tipo="goblin")


class Esqueleto(Inimigo):

    def __init__(self, nome="Esqueleto"):
        super().__init__(nome=nome, vida=70, ataque=18, defesa=4, tipo="esqueleto")

    def atacar(self, alvo):
        print(f"{self.nome} golpeia com ossos quebrados em {alvo.nome}!")
        alvo.receber_dano(self.ataque)


class GuerreiroSombrio(Inimigo):
    incompativeis = ["Guerreiro"]

    def __init__(self, nome="Guerreiro Sombrio"):
        super().__init__(nome=nome, vida=100, ataque=22, defesa=8, tipo="guerreiro_sombrio")


class MagoSombrio(Inimigo):
    incompativeis = ["Mago"]

    def __init__(self, nome="Mago Sombrio"):
        super().__init__(nome=nome, vida=90, ataque=24, defesa=6, tipo="mago_sombrio")


class ArqueiroSombrio(Inimigo):
    incompativeis = ["Arqueiro"]

    def __init__(self, nome="Arqueiro Sombrio"):
        super().__init__(nome=nome, vida=85, ataque=20, defesa=7, tipo="arqueiro_sombrio")


class ChefeFinal(Inimigo):

    def __init__(self, nome="Chefe Final"):
        super().__init__(nome=nome, vida=200, ataque=35, defesa=12, tipo="chefe")

    def ataque_especial(self, alvo):
        dano = self.ataque + 15
        print(f"{self.nome} usa Golpe do Crepúsculo em {alvo.nome} causando {dano} de dano!")
        alvo.receber_dano(dano)
