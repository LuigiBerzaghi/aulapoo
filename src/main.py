import sys

try:
    from src.guerreiro import Guerreiro
    from src.inimigo import Inimigo
    from src.batalha import Batalha
    from src.mago import Mago
except ModuleNotFoundError:
    from guerreiro import Guerreiro
    from inimigo import Inimigo
    from batalha import Batalha
    from mago import Mago


def selecionar_personagem():
    print("\nEscolha seu personagem:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Sair")

    opcao = input("Opção: ").strip()

    if opcao == "2":
        return Mago("Merlin")
    if opcao == "3":
        raise SystemExit
    return Guerreiro("Arthur")


def main():
    personagem = (sys.argv[1] if len(sys.argv) > 1 else "").lower()

    if personagem == "mago":
        jogador = Mago("Merlin")
    elif personagem == "guerreiro":
        jogador = Guerreiro("Arthur")
    else:
        jogador = selecionar_personagem()

    inimigo = Inimigo(
        nome="Goblin",
        vida=1000,
        ataque=15,
        defesa=5
    )

    batalha = Batalha(jogador, inimigo)
    batalha.iniciar()


if __name__ == "__main__":
    main()
