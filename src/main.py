import sys

try:
    from src.guerreiro import Guerreiro
    from src.inimigo import ArqueiroSombrio, ChefeFinal, Esqueleto, Goblin, GuerreiroSombrio, Inimigo, MagoSombrio
    from src.batalha import Batalha, mostrar_titulo
    from src.mago import Mago
    from src.arqueiro import Arqueiro
except ModuleNotFoundError:
    from guerreiro import Guerreiro
    from inimigo import ArqueiroSombrio, ChefeFinal, Esqueleto, Goblin, GuerreiroSombrio, Inimigo, MagoSombrio
    from batalha import Batalha, mostrar_titulo
    from mago import Mago
    from arqueiro import Arqueiro


def listar_inimigos_disponiveis(jogador):
    classes_vilao = [Goblin, Esqueleto, GuerreiroSombrio, MagoSombrio, ArqueiroSombrio, ChefeFinal]
    return [classe for classe in classes_vilao if classe.pode_enfrentar(jogador.__class__)]


def mostrar_abertura():
    mostrar_titulo("JOGO DE BATALHA RPG")
    print("O Reino de Eldoria vive dias sombrios.")
    print("Criaturas da noite atacam os vilarejos e o Mestre da Noite espera em seu castelo.")
    print("Um herói precisa se levantar. Será você?")


def selecionar_personagem():
    mostrar_titulo("ESCOLHA SEU HERÓI")
    print("1 - Guerreiro (Arthur)  | Vida 120 | Ataque 20 | Defesa 10")
    print("2 - Mago (Merlin)       | Vida 80  | Ataque 30 | Defesa 5  | Usa magia")
    print("3 - Arqueiro (Legolas)  | Vida 100 | Ataque 18 | Defesa 8  | Usa flechas")
    print("4 - Sair")

    opcao = input("Opção: ").strip()

    if opcao == "2":
        return Mago("Merlin")
    if opcao == "3":
        return Arqueiro("Legolas")
    if opcao == "4":
        print("Até a próxima, aventureiro!")
        raise SystemExit
    return Guerreiro("Arthur")


def selecionar_inimigo(jogador):
    inimigos = listar_inimigos_disponiveis(jogador)
    if not inimigos:
        return ChefeFinal("Mestre da Noite")

    mostrar_titulo("ESCOLHA SEU OPONENTE")
    for indice, classe in enumerate(inimigos, start=1):
        vilao = classe()
        print(f"{indice} - {vilao.nome} | Vida {vilao.vida} | Ataque {vilao.ataque}")

    opcao = input("Opção: ").strip()
    if opcao.isdigit():
        escolha = int(opcao) - 1
        if 0 <= escolha < len(inimigos):
            return inimigos[escolha]()

    return inimigos[0]()


def main():
    personagem = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
    mostrar_abertura()

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
