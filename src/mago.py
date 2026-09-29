import random

try:
    from src.item import Item
    from src.personagem import Personagem
except ModuleNotFoundError:
    from item import Item
    from personagem import Personagem


class Mago(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=80,
            ataque=30,
            defesa=5,
            vida_maxima=80,
        )

        self.mana = 100
        self.mana_maxima = 100
        self.dano_bonus_rodada = 1.0
        self.inventario = [
            Item("Poção de vida", 20, "cura", "Recupera vida"),
            Item("Poção de mana", 25, "mana", "Recupera mana"),
            Item("Pergaminho arcano", 18, "cura", "Pergaminho de suporte")
        ]

    def mostrar_status(self):
        print(
            f"{self.nome} | "
            f"Vida: {self.vida}/{self.vida_maxima} | "
            f"Mana: {self.mana}/{self.mana_maxima} | "
            f"Ataque: {self.ataque} | "
            f"Defesa: {self.defesa}"
        )

    def atacar(self, alvo):
        dano_final = self.ataque * self.dano_bonus_rodada
        self.dano_bonus_rodada = 1.0

        mensagens = [
            f"{self.nome} concentra energia e dispara um raio arcano em {alvo.nome}!",
            f"{self.nome} perfura o ar com um projétil mágico em direção a {alvo.nome}!",
            f"{self.nome} lança um feixe místico contra {alvo.nome}!"
        ]
        print(mensagens[2])
        alvo.receber_dano(int(dano_final))

    def usar_magia(self, alvo):
        if self.mana < 20:
            mensagens = [
                f"{self.nome} tenta conjurar magia, mas o círculo falha.",
                f"{self.nome} estica a mão, mas não há mana suficiente.",
                f"{self.nome} sente a magia falhar por falta de energia."
            ]
            print(mensagens[0])
            return False

        chance_falha = random.randint(1, 5)
        if chance_falha == 1:
            print(f"{self.nome} tenta lançar a magia, mas a runa se desfaz e falha!")
            self.gastar_mana(10)
            return False

        if not self.gastar_mana(20):
            print(f"{self.nome} não tem mana suficiente para conjurar a magia.")
            return False

        dano_magico = random.randint(20, 45)
        if random.randint(1, 8) == 1:
            dano_magico += 20
            print(f"{self.nome} ativa um crítico arcano! A magia explode com força extra!")

        dano_magico = int(dano_magico * self.dano_bonus_rodada)
        self.dano_bonus_rodada = 1.0

        mensagens = [
            f"{self.nome} ergue os braços e dispara uma explosão de fogo sobre {alvo.nome}!",
            f"{self.nome} canaliza uma esfera de energia e a lança em {alvo.nome}!",
            f"{self.nome} invoca uma tempestade arcana e atinge {alvo.nome}!"
        ]
        print(mensagens[1])
        print(f"Dano mágico: {dano_magico} (multiplicador ativo: {self.dano_bonus_rodada}x)")
        alvo.receber_dano(dano_magico)
        return True
