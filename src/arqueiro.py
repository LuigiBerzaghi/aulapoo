import random

try:
    from src.item import Item
    from src.personagem import Personagem
except ModuleNotFoundError:
    from item import Item
    from personagem import Personagem


class Arqueiro(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=100,
            ataque=18,
            defesa=8,
            vida_maxima=100,
        )
        self.flechas = 10
        self.inventario = [
            Item("Poção de vida", 20, "cura", "Recupera vida"),
            Item("Flecha especial", 5, "flecha", "Recarrega flechas"),
            Item("Elixir do arqueiro", 18, "cura", "Poção de suporte")
        ]

    def atacar(self, alvo):
        if self.flechas <= 0:
            print(f"{self.nome} tenta atirar, mas não há flechas restantes!")
            return

        self.flechas -= 1
        dano = self.ataque + random.randint(0, 8)
        mensagens = [
            f"{self.nome} dispara uma flecha certeira em {alvo.nome}!",
            f"{self.nome} acerta um tiro preciso em {alvo.nome}!",
            f"{self.nome} mira e atira em {alvo.nome}!"
        ]
        print(random.choice(mensagens))
        alvo.receber_dano(dano)
