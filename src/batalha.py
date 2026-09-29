try:
    from src.item import Item
    from src.guerreiro import Guerreiro
    from src.mago import Mago
    from src.arqueiro import Arqueiro
except ModuleNotFoundError:
    from item import Item
    from guerreiro import Guerreiro
    from mago import Mago
    from arqueiro import Arqueiro


class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
        self.itens = self.jogador.inventario

    @property
    def itens(self):
        return self.jogador.inventario

    @itens.setter
    def itens(self, valor):
        self.jogador.inventario = valor

    def trocar_personagem(self, novo_personagem):
        if novo_personagem is None:
            return False

        print(f"{self.jogador.nome} sai do campo e {novo_personagem.nome} entra na batalha!")
        self.jogador = novo_personagem
        return True

    def escolher_personagem(self):
        print("\nTroca de personagem:")
        print("1 - Guerreiro")
        print("2 - Mago")
        print("3 - Arqueiro")
        print("4 - Manter personagem atual")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            return Guerreiro("Arthur")
        if opcao == "2":
            return Mago("Merlin")
        if opcao == "3":
            return Arqueiro("Legolas")
        return None

    def menu_itens(self):
        itens = self.jogador.inventario
        if not itens:
            print("Seu inventário está vazio.")
            return None

        print("\n--- ITENS DISPONÍVEIS ---")
        for indice, item in enumerate(itens, start=1):
            print(f"{indice} - {item.nome} ({item.tipo})")

        escolha = input("Escolha um item: ").strip()
        if not escolha.isdigit():
            print("Opção inválida.")
            return None

        posicao = int(escolha) - 1
        if posicao not in range(len(itens)):
            print("Item inexistente.")
            return None

        return itens[posicao]

    def usar_item(self, item=None):
        itens = self.jogador.inventario
        if not itens:
            print("Você não possui itens.")
            return False

        if item is None:
            if len(itens) == 1:
                item = itens[0]
            else:
                item = self.menu_itens()
                if item is None:
                    return False

        try:
            indice = itens.index(item)
        except ValueError:
            print("Esse item não está no seu inventário.")
            return False

        item.usar(self.jogador)
        del itens[indice]
        return True

    def turno_inimigo(self):
        if not self.jogador.esta_vivo() or not self.inimigo.esta_vivo():
            return False

        if hasattr(self.inimigo, "ataque_especial") and self.inimigo.vida <= self.inimigo.vida_maxima * 0.3:
            self.inimigo.ataque_especial(self.jogador)
        else:
            self.inimigo.atacar(self.jogador)

        return self.jogador.esta_vivo()

    def condicao_vitoria(self):
        if self.inimigo.esta_vivo() is False and self.jogador.esta_vivo() is True:
            return "vitoria"
        if self.jogador.esta_vivo() is False and self.inimigo.esta_vivo() is True:
            return "derrota"
        if self.jogador.esta_vivo() is False and self.inimigo.esta_vivo() is False:
            return "empate"
        return "em_andamento"

    def executar_turno_jogador(self, acao="atacar"):
        if acao == "atacar":
            self.jogador.atacar(self.inimigo)
        elif acao == "magia" and hasattr(self.jogador, "usar_magia"):
            self.jogador.usar_magia(self.inimigo)
        elif acao == "item":
            self.usar_item()
        else:
            raise ValueError(f"Ação inválida: {acao}")

        if self.inimigo.esta_vivo() and self.jogador.esta_vivo():
            self.turno_inimigo()

    def realizar_turno_inimigo(self):
        return self.turno_inimigo()

    def iniciar(self):
        print("=" * 40)
        print("        INÍCIO DA BATALHA")
        print("=" * 40)

        while self.jogador.esta_vivo() and self.inimigo.esta_vivo():
            print("\n--- STATUS ---")
            self.jogador.mostrar_status()
            self.inimigo.mostrar_status()

            print("\n--- AÇÕES ---")
            print("0 - Trocar de personagem")
            print("1 - Atacar")

            if hasattr(self.jogador, "usar_magia"):
                print("2 - Usar magia")
                print("3 - Usar item")
                print("4 - Fugir")
            else:
                print("2 - Usar item")
                print("3 - Fugir")

            if self.jogador.inventario:
                print(f"Inventário: {', '.join(item.nome for item in self.jogador.inventario)}")

            if hasattr(self.jogador, "mana"):
                print(f"Mana: {self.jogador.mana}/{self.jogador.mana_maxima}")

            if hasattr(self.jogador, "dano_bonus_rodada") and self.jogador.dano_bonus_rodada > 1.0:
                print(f"Bônus de dano ativo: {self.jogador.dano_bonus_rodada}x")

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "0":
                novo_personagem = self.escolher_personagem()
                if novo_personagem is not None:
                    self.trocar_personagem(novo_personagem)
                continue

            if opcao == "1":
                print(f"\n{self.jogador.nome} decide atacar!")
                self.executar_turno_jogador("atacar")

            elif opcao == "2" and hasattr(self.jogador, "usar_magia"):
                print(f"\n{self.jogador.nome} prepara uma magia poderosa!")
                self.executar_turno_jogador("magia")

            elif opcao == "2":
                print(f"\n{self.jogador.nome} usa uma poção de cura.")
                self.executar_turno_jogador("item")

            elif opcao == "3" and hasattr(self.jogador, "usar_magia"):
                print(f"\n{self.jogador.nome} bebe uma poção e se fortalece.")
                self.executar_turno_jogador("item")

            elif opcao == "3":
                print(f"{self.jogador.nome} tenta escapar da batalha!")
                print("Você fugiu da batalha!")
                return

            elif opcao == "4" and hasattr(self.jogador, "usar_magia"):
                print(f"{self.jogador.nome} decidiu fugir da batalha.")
                print("Você fugiu da batalha!")
                return

            else:
                print("Opção inválida.")
                continue

            estado = self.condicao_vitoria()
            if estado == "vitoria":
                print(f"{self.inimigo.nome} cai no chão, derrotado!")
                print("Você venceu a batalha!")
                return
            if estado == "derrota":
                print(f"{self.jogador.nome} sucumbe ao combate.")
                print("Você perdeu a batalha!")
                return

        estado = self.condicao_vitoria()
        if estado == "vitoria":
            print("Você venceu a batalha!")
        elif estado == "derrota":
            print("Você perdeu a batalha!")

    @property
    def venceu(self):
        return self.condicao_vitoria() == "vitoria"

    @property
    def perdeu(self):
        return self.condicao_vitoria() == "derrota"
