try:
    from src.personagem import Personagem
except ModuleNotFoundError:
    from personagem import Personagem


class Guerreiro(Personagem):

    def __init__(self, nome):
        super().__init__(
            nome=nome,
            vida=120,
            ataque=20,
            defesa=10
        )

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} avança com sua espada e investe contra {alvo.nome}!",
            f"{self.nome} acerta um golpe firme em {alvo.nome}!",
            f"{self.nome} desfere um ataque decidido e atinge {alvo.nome}!"
        ]
        print(mensagens[0])
        alvo.receber_dano(self.ataque)
