from abc import ABC, abstractmethod


class Personagem(ABC):

    def __init__(self, nome, vida, ataque, defesa, vida_maxima=None):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
        self.defesa = defesa
        self.vida_maxima = vida if vida_maxima is None else vida_maxima
        self.inventario = []

    def esta_vivo(self):
        return self.vida > 0

    def curar(self, quantidade):
        if quantidade <= 0:
            return self.vida
        self.vida = min(self.vida_maxima, self.vida + quantidade)
        return self.vida

    def adicionar_item(self, item):
        self.inventario.append(item)
        return self.inventario

    def listar_itens(self):
        return [item.nome for item in self.inventario]

    def receber_dano(self, dano):
        if dano <= 0:
            return self.vida

        dano_real = max(dano - self.defesa, 0)
        self.vida = max(0, self.vida - dano_real)
        return self.vida

    @abstractmethod
    def atacar(self, alvo):
        pass

    def mostrar_status(self):
        print(
            f"{self.nome} | "
            f"Vida: {self.vida}/{self.vida_maxima} | "
            f"Ataque: {self.ataque} | "
            f"Defesa: {self.defesa}"
        )

    def gastar_mana(self, quantidade):
        if not hasattr(self, "mana"):
            return False

        if self.mana < quantidade:
            return False

        self.mana -= quantidade
        return True

    def recuperar_mana(self, quantidade):
        if not hasattr(self, "mana"):
            return False

        maximo = getattr(self, "mana_maxima", 100)
        self.mana = min(maximo, self.mana + quantidade)
        return True
