class Item:

    def __init__(self, nome, valor, tipo="cura", descricao=""):
        self.nome = nome
        self.valor = valor
        self.tipo = tipo
        self.descricao = descricao or "Item de suporte"

    def usar(self, personagem):
        if self.nome == "Pergaminho arcano" and hasattr(personagem, "dano_bonus_rodada"):
            personagem.dano_bonus_rodada = 1.5
            print(f"{personagem.nome} ativou o pergaminho arcano! O próximo ataque recebe 1.5x de dano.")
            return 1.5

        if self.tipo == "cura":
            vida_antes = personagem.vida
            personagem.curar(self.valor)
            recuperado = personagem.vida - vida_antes
            print(f"{personagem.nome} usa {self.nome} e recupera {recuperado} de vida.")
            return recuperado

        if self.tipo == "mana" and hasattr(personagem, "mana"):
            mana_antes = personagem.mana
            personagem.recuperar_mana(self.valor)
            restaurado = personagem.mana - mana_antes
            print(f"{personagem.nome} usa {self.nome} e recupera {restaurado} de mana.")
            return restaurado

        if self.tipo == "flecha" and hasattr(personagem, "flechas"):
            personagem.flechas += self.valor
            print(f"{personagem.nome} usa {self.nome} e recebe {self.valor} flechas extras.")
            return self.valor

        print(f"{personagem.nome} usou {self.nome}, mas não há efeito.")
        return 0

    def __repr__(self):
        return f"Item(nome='{self.nome}', valor={self.valor}, tipo='{self.tipo}')"
