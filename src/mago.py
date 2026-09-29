import random

try:
    from src.personagem import Personagem
except ModuleNotFoundError:
    from personagem import Personagem

class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=80,
            ataque=30,
            defesa=5
        )

        self.mana = 100

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} concentra energia e dispara um raio arcano em {alvo.nome}!",
            f"{self.nome} perfura o ar com um projétil mágico em direção a {alvo.nome}!",
            f"{self.nome} lança um feixe místico contra {alvo.nome}!"
        ]
        print(mensagens[2])
        alvo.receber_dano(self.ataque)

    def usar_magia(self, alvo):
        if self.mana < 20:
            mensagens = [
                f"{self.nome} tenta conjurar magia, mas o círculo falha.",
                f"{self.nome} estica a mão, mas não há mana suficiente.",
                f"{self.nome} sente a magia falhar por falta de energia."
            ]
            print(mensagens[0])
            return

        chance_falha = random.randint(1, 5)
        if chance_falha == 1:
            print(f"{self.nome} tenta lançar a magia, mas a runa se desfaz e falha!")
            self.mana -= 10
            return

        dano_magico = random.randint(20, 45)
        if random.randint(1, 8) == 1:
            dano_magico += 20
            print(f"{self.nome} ativa um crítico arcano! A magia explode com força extra!")

        mensagens = [
            f"{self.nome} ergue os braços e dispara uma explosão de fogo sobre {alvo.nome}!",
            f"{self.nome} canaliza uma esfera de energia e a lança em {alvo.nome}!",
            f"{self.nome} invoca uma tempestade arcana e atinge {alvo.nome}!"
        ]
        print(mensagens[1])
        self.mana -= 20
        print(f"Dano mágico: {dano_magico}")
        alvo.receber_dano(dano_magico)
