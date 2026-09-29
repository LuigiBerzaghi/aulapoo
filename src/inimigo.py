try:
    from src.personagem import Personagem
except ModuleNotFoundError:
    from personagem import Personagem


class Inimigo(Personagem):

    def __init__(self, nome, vida, ataque, defesa):
        super().__init__(
            nome=nome,
            vida=vida,
            ataque=ataque,
            defesa=defesa
        )

    def atacar(self, alvo):
        mensagens = [
            f"{self.nome} salta para a frente e ataca {alvo.nome}!",
            f"{self.nome} desferiu um golpe rápido sobre {alvo.nome}!",
            f"{self.nome} aproveita a abertura e acerta {alvo.nome}!"
        ]
        print(mensagens[1])
        alvo.receber_dano(self.ataque)
