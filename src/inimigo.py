import random

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
        self.local = "Um campo de batalha silencioso, onde só o vento se move."
        self.fala = "Prepare-se para lutar!"

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
        print(random.choice(mensagens))
        alvo.receber_dano(self.ataque)

    def ataque_especial(self, alvo):
        self.atacar(alvo)


class Goblin(Inimigo):

    def __init__(self, nome="Goblin"):
        super().__init__(nome=nome, vida=70, ataque=18, defesa=4, tipo="goblin")
        self.local = "Uma floresta escura, cheia de galhos retorcidos e olhos brilhando entre as árvores."
        self.fala = "Hehehe! Suas moedas e sua comida agora são minhas!"


class Esqueleto(Inimigo):

    def __init__(self, nome="Esqueleto"):
        super().__init__(nome=nome, vida=70, ataque=18, defesa=4, tipo="esqueleto")
        self.local = "Uma cripta antiga e úmida. Ossos se espalham pelo chão e algo range no escuro."
        self.fala = "Mais um aventureiro... logo você fará parte da minha coleção de ossos."

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} golpeia com ossos quebrados em {alvo.nome}!",
            f"{self.nome} range os dentes e arranha {alvo.nome} com seus dedos de osso!",
            f"{self.nome} gira o braço de osso e acerta {alvo.nome}!"
        ]
        print(random.choice(mensagens))
        alvo.receber_dano(self.ataque)


class GuerreiroSombrio(Inimigo):
    incompativeis = ["Guerreiro"]

    def __init__(self, nome="Guerreiro Sombrio"):
        super().__init__(nome=nome, vida=100, ataque=22, defesa=8, tipo="guerreiro_sombrio")
        self.local = "As ruínas de um castelo em chamas. Uma armadura negra brilha entre a fumaça."
        self.fala = "Eu já fui um herói como você. Veja no que me tornei!"


class MagoSombrio(Inimigo):
    incompativeis = ["Mago"]

    def __init__(self, nome="Mago Sombrio"):
        super().__init__(nome=nome, vida=90, ataque=24, defesa=6, tipo="mago_sombrio")
        self.local = "Uma torre coberta de runas roxas. O ar pesa com magia proibida."
        self.fala = "Seus truques não são páreo para o poder das sombras!"


class ArqueiroSombrio(Inimigo):
    incompativeis = ["Arqueiro"]

    def __init__(self, nome="Arqueiro Sombrio"):
        super().__init__(nome=nome, vida=85, ataque=20, defesa=7, tipo="arqueiro_sombrio")
        self.local = "Um desfiladeiro estreito e coberto de névoa. Você sente que está sendo observado."
        self.fala = "Eu nunca erro um alvo. E você é o próximo."


class ChefeFinal(Inimigo):

    def __init__(self, nome="Chefe Final"):
        super().__init__(nome=nome, vida=200, ataque=35, defesa=12, tipo="chefe")
        self.local = "O salão do trono do Castelo da Noite. Tochas azuis iluminam um trono de pedra negra."
        self.fala = "Você chegou longe, pequeno herói. Mas aqui sua jornada termina!"

    def ataque_especial(self, alvo):
        dano = self.ataque + 15
        print(f"{self.nome} usa Golpe do Crepúsculo em {alvo.nome}!")
        alvo.receber_dano(dano)
