"""Versão gráfica do jogo (pygame).

Na raiz do projeto: python src/main_pygame.py
"""

try:
    from src.interface.app import Jogo
except ModuleNotFoundError:
    from interface.app import Jogo


def main():
    Jogo().executar()


if __name__ == "__main__":
    main()
