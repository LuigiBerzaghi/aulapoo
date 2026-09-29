try:
    from src.item import Item
    from src.personagem import Personagem
except ModuleNotFoundError:
    from item import Item
    from personagem import Personagem


class Guerreiro(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=120,
            ataque=20,
            defesa=10,
            vida_maxima=120,
        )
        self.inventario = [
            Item("Poção de vida", 20, "cura", "Recupera vida"),
            Item("Bandagem", 15, "cura", "Curativo básico"),
            Item("Elixir do soldado", 25, "cura", "Poção reforçada")
        ]

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} avança com sua espada e investe contra {alvo.nome}!",
            f"{self.nome} acerta um golpe firme em {alvo.nome}!",
            f"{self.nome} desfere um ataque decidido e atinge {alvo.nome}!"
        ]
        print(mensagens[0])
        alvo.receber_dano(self.ataque)
