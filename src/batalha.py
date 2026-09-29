try:
    from src.item import Item
    from src.guerreiro import Guerreiro
    from src.mago import Mago
except ModuleNotFoundError:
    from item import Item
    from guerreiro import Guerreiro
    from mago import Mago


class Batalha:

    def __init__(self, jogador, inimigo):
        self.jogador = jogador
        self.inimigo = inimigo
        self.itens = [Item("Poção de vida", 20)]

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
        print("3 - Manter personagem atual")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            return Guerreiro("Arthur")
        if opcao == "2":
            return Mago("Merlin")
        return None

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

            opcao = input("Escolha uma opção: ")

            if opcao == "0":
                novo_personagem = self.escolher_personagem()
                if novo_personagem is not None:
                    self.trocar_personagem(novo_personagem)
                continue

            if opcao == "1":
                print(f"\n{self.jogador.nome} decide atacar!")
                self.jogador.atacar(self.inimigo)

                if not self.inimigo.esta_vivo():
                    print(f"{self.inimigo.nome} cai no chão, derrotado!")
                    break

                print(f"\n{self.inimigo.nome} contra-ataca com fúria!")
                self.inimigo.atacar(self.jogador)

                if not self.jogador.esta_vivo():
                    print(f"{self.jogador.nome} sucumbe ao combate.")
                    break

            elif opcao == "2" and hasattr(self.jogador, "usar_magia"):
                print(f"\n{self.jogador.nome} prepara uma magia poderosa!")
                self.jogador.usar_magia(self.inimigo)

                if not self.inimigo.esta_vivo():
                    print(f"{self.inimigo.nome} é derrotado pela magia!")
                    break

                if self.inimigo.esta_vivo():
                    print(f"\n{self.inimigo.nome} reage antes que o feitiço termine!")
                    self.inimigo.atacar(self.jogador)

                    if not self.jogador.esta_vivo():
                        print(f"{self.jogador.nome} foi abatido.")
                        break

            elif opcao == "2":
                if not self.itens:
                    print("Você não possui itens.")
                    continue

                print(f"\n{self.jogador.nome} usa uma poção de cura.")
                item = self.itens.pop(0)
                item.usar(self.jogador)

                if self.inimigo.esta_vivo():
                    print(f"\nO inimigo aproveita a abertura e ataca!")
                    self.inimigo.atacar(self.jogador)

                    if not self.jogador.esta_vivo():
                        print(f"{self.jogador.nome} foi derrotado!")
                        break

            elif opcao == "3" and hasattr(self.jogador, "usar_magia"):
                if not self.itens:
                    print("Você não possui itens.")
                    continue

                print(f"\n{self.jogador.nome} bebe uma poção e se fortalece.")
                item = self.itens.pop(0)
                item.usar(self.jogador)

                if self.inimigo.esta_vivo():
                    print(f"\n{self.inimigo.nome} não deixa a oportunidade passar!")
                    self.inimigo.atacar(self.jogador)

                    if not self.jogador.esta_vivo():
                        print(f"{self.jogador.nome} foi derrotado!")
                        break

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

        if self.jogador.esta_vivo() and not self.inimigo.esta_vivo():
            print("Você venceu a batalha!")
        elif self.inimigo.esta_vivo() and not self.jogador.esta_vivo():
            print("Você perdeu a batalha!")
