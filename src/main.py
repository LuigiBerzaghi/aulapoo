import sys

try:
    from src.guerreiro import Guerreiro
    from src.inimigo import ArqueiroSombrio, ChefeFinal, Esqueleto, Goblin, GuerreiroSombrio, Inimigo, MagoSombrio
    from src.batalha import Batalha
    from src.mago import Mago
    from src.arqueiro import Arqueiro
except ModuleNotFoundError:
    from guerreiro import Guerreiro
    from inimigo import ArqueiroSombrio, ChefeFinal, Esqueleto, Goblin, GuerreiroSombrio, Inimigo, MagoSombrio
    from batalha import Batalha
    from mago import Mago
    from arqueiro import Arqueiro


def listar_inimigos_disponiveis(jogador):
    classes_vilao = [Goblin, Esqueleto, GuerreiroSombrio, MagoSombrio, ArqueiroSombrio, ChefeFinal]
    return [classe for classe in classes_vilao if classe.pode_enfrentar(jogador.__class__)]


def selecionar_personagem():
    print("\nEscolha seu personagem:")
    print("1 - Guerreiro")
    print("2 - Mago")
    print("3 - Arqueiro")
    print("4 - Sair")

    opcao = input("Opção: ").strip()

    if opcao == "2":
        return Mago("Merlin")
    if opcao == "3":
        return Arqueiro("Legolas")
    if opcao == "4":
        raise SystemExit
    return Guerreiro("Arthur")


def selecionar_inimigo(jogador):
    inimigos = listar_inimigos_disponiveis(jogador)
    if not inimigos:
        return ChefeFinal("Mestre da Noite")

    print("\nEscolha o vilão que deseja enfrentar:")
    for indice, classe in enumerate(inimigos, start=1):
        print(f"{indice} - {classe.__name__}")

    opcao = input("Opção: ").strip()
    if opcao.isdigit():
        escolha = int(opcao) - 1
        if 0 <= escolha < len(inimigos):
            return inimigos[escolha]()

    return inimigos[0]()


def main():
    personagem = (sys.argv[1] if len(sys.argv) > 1 else "").lower()

    if personagem == "mago":
        jogador = Mago("Merlin")
    elif personagem == "arqueiro":
        jogador = Arqueiro("Legolas")
    elif personagem == "guerreiro":
        jogador = Guerreiro("Arthur")
    elif personagem == "chefe":
        jogador = Guerreiro("Arthur")
        inimigo = ChefeFinal("Mestre da Noite")
        batalha = Batalha(jogador, inimigo)
        batalha.iniciar()
        return
    else:
        jogador = selecionar_personagem()

    inimigo = selecionar_inimigo(jogador)
    batalha = Batalha(jogador, inimigo)
    batalha.iniciar()


if __name__ == "__main__":
    main()
