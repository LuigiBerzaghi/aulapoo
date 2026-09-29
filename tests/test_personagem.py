from src.arqueiro import Arqueiro
from src.batalha import Batalha
from src.guerreiro import Guerreiro
from src.inimigo import ChefeFinal, Esqueleto, GuerreiroSombrio, Inimigo
from src.item import Item
from src.mago import Mago
from src.main import listar_inimigos_disponiveis


def test_guerreiro_esta_vivo():
    guerreiro = Guerreiro("Arthur")

    assert guerreiro.esta_vivo() is True


def test_personagem_recebe_dano():
    guerreiro = Guerreiro("Arthur")

    guerreiro.receber_dano(20)

    assert guerreiro.vida == 110


def test_personagem_morre():
    guerreiro = Guerreiro("Arthur")

    guerreiro.receber_dano(500)

    assert guerreiro.vida == 0
    assert guerreiro.esta_vivo() is False


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


def test_heroi_arquero_ataca():
    arqueiro = Arqueiro("Legolas")
    inimigo = Inimigo("Goblin", 90, 15, 4)

    arqueiro.atacar(inimigo)

    assert inimigo.vida < 90


def test_item_pocao_recupera_vida():
    guerreiro = Guerreiro("Arthur")
    guerreiro.receber_dano(25)
    pocao = Item("Poção de vida", 20)

    pocao.usar(guerreiro)

    assert guerreiro.vida == 120


def test_novo_inimigo_e_chefe_final():
    esqueleto = Esqueleto("Esqueleto")
    chefe = ChefeFinal("Mestre da Noite")

    assert isinstance(esqueleto, Inimigo)
    assert isinstance(chefe, Inimigo)
    assert chefe.vida > esqueleto.vida


def test_pergaminho_arcano_aumenta_dano_na_proxima_rodada():
    mago = Mago("Merlin")
    inimigo = Inimigo("Goblin", 100, 20, 5)

    pergaminho = next(item for item in mago.inventario if item.nome == "Pergaminho arcano")
    pergaminho.usar(mago)
    mago.atacar(inimigo)

    assert mago.dano_bonus_rodada == 1.0
    assert inimigo.vida < 70


def test_magia_respeita_multiplicador_do_pergaminho():
    mago = Mago("Merlin")
    inimigo = Inimigo("Goblin", 100, 20, 5)

    pergaminho = next(item for item in mago.inventario if item.nome == "Pergaminho arcano")
    pergaminho.usar(mago)
    vida_antes = inimigo.vida
    mago.usar_magia(inimigo)

    assert mago.dano_bonus_rodada == 1.0
    assert inimigo.vida < vida_antes


def test_mago_gasta_mana_ao_usar_magia():
    mago = Mago("Merlin")
    inimigo = Inimigo("Goblin", 100, 20, 5)

    mago.mana = 25

    import random
    original = random.randint
    random.randint = lambda a, b: 3
    try:
        mago.usar_magia(inimigo)
    finally:
        random.randint = original

    assert mago.mana == 5


def test_pocao_de_mana_recupera_mana():
    mago = Mago("Merlin")
    mago.mana = 30
    item = next(item for item in mago.inventario if item.nome == "Poção de mana")

    item.usar(mago)

    assert mago.mana >= 30


def test_mago_sem_mana_nao_conjura():
    mago = Mago("Merlin")
    inimigo = Inimigo("Goblin", 100, 20, 5)
    mago.mana = 10

    vida_antes = inimigo.vida
    mago.usar_magia(inimigo)

    assert mago.mana == 10
    assert inimigo.vida == vida_antes


def test_inventario_diferente_por_personagem():
    guerreiro = Guerreiro("Arthur")
    mago = Mago("Merlin")
    arqueiro = Arqueiro("Legolas")

    assert any(item.nome == "Poção de vida" for item in guerreiro.inventario)
    assert any(item.nome == "Poção de mana" for item in mago.inventario)
    assert any(item.nome == "Flecha especial" for item in arqueiro.inventario)
    assert guerreiro.inventario != mago.inventario
    assert arqueiro.inventario != mago.inventario


def test_listar_inimigos_disponiveis_respeita_compatibilidade():
    guerreiro = Guerreiro("Arthur")
    inimigos = listar_inimigos_disponiveis(guerreiro)

    assert GuerreiroSombrio.__name__ not in {tipo.__name__ for tipo in inimigos}
    assert any(tipo.__name__ == "Esqueleto" for tipo in inimigos)
