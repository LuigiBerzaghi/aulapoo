"""Teste de fumaça da interface pygame, sem abrir janela nem tocar som."""

import os

import pytest

pygame = pytest.importorskip("pygame")


@pytest.fixture
def jogo():
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    from src.interface.app import Jogo

    instancia = Jogo()
    yield instancia
    pygame.quit()


@pytest.mark.filterwarnings("ignore:no fast renderer available")
def test_batalha_completa_ate_a_vitoria(jogo):
    from src.inimigo import Goblin
    from src.interface.cena_batalha import CenaBatalha

    cena = CenaBatalha(jogo, "guerreiro", Goblin)
    jogo.cena = cena
    espaco = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE, unicode=" ", mod=0, scancode=0)

    for _ in range(3000):
        jogo.passo(1 / 30, [])
        if cena.estado == "intro" and cena.t > 1.2:
            cena.tratar_evento(espaco)
        elif cena.estado == "escolha":
            cena.ctrl.jogador.vida = cena.ctrl.jogador.vida_maxima
            cena.acao_atacar()
        elif cena.estado == "fim":
            break

    assert cena.fim == "vitoria"
    assert not cena.ctrl.inimigo.esta_vivo()
