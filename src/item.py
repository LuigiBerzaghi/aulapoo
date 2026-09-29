class Item:

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def usar(self, personagem):
        personagem.vida += self.valor
        print(f"{personagem.nome} recuperou {self.valor} de vida.")
