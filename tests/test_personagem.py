from src.guerreiro import Guerreiro
from src.inimigo import Inimigo
from src.mago import Mago
from src.batalha import Batalha


def test_guerreiro_esta_vivo():

    guerreiro = Guerreiro("Arthur")

    assert guerreiro.esta_vivo() is True


def test_personagem_recebe_dano():
    guerreiro = Guerreiro("Arthur")

    guerreiro.receber_dano(20)

    assert guerreiro.vida == 110


def test_personagem_morre():
    # TODO
    pass


def test_guerreiro_ataca():
    guerreiro = Guerreiro("Arthur")
    inimigo = Inimigo("Goblin", 100, 20, 5)

    guerreiro.atacar(inimigo)

    assert inimigo.vida == 85


def test_inimigo_ataca():
    guerreiro = Guerreiro("Arthur")
    inimigo = Inimigo("Goblin", 100, 20, 5)

    inimigo.atacar(guerreiro)

    assert guerreiro.vida == 110


def test_mago_usa_magia():
    mago = Mago("Merlin")
    guerreiro = Guerreiro("Arthur")

    vida_antes = guerreiro.vida
    mago.usar_magia(guerreiro)

    assert 70 <= mago.mana <= 100
    assert 0 <= guerreiro.vida <= vida_antes


def test_batalha_troca_personagem():
    guerra = Guerreiro("Arthur")
    inimigo = Inimigo("Goblin", 100, 20, 5)
    batalha = Batalha(guerra, inimigo)

    novo = Mago("Merlin")
    batalha.trocar_personagem(novo)

    assert batalha.jogador is novo
    assert isinstance(batalha.jogador, Mago)
    assert batalha.jogador.nome == "Merlin"
