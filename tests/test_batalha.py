from src.batalha import Batalha
from src.guerreiro import Guerreiro
from src.inimigo import ChefeFinal, Esqueleto
from src.item import Item


def test_batalha_troca_personagem():
    guerra = Guerreiro("Arthur")
    inimigo = Esqueleto("Esqueleto")
    batalha = Batalha(guerra, inimigo)

    assert batalha.jogador is guerra
    assert batalha.inimigo is inimigo

    nova = Guerreiro("Arthur II")
    assert batalha.trocar_personagem(nova) is True
    assert batalha.jogador is nova


def test_batalha_usa_item_e_turno_inimigo():
    guerra = Guerreiro("Arthur")
    guerra.receber_dano(40)
    inimigo = Esqueleto("Esqueleto")
    batalha = Batalha(guerra, inimigo)

    batalha.itens = [Item("Pocao de vida", 25)]
    batalha.usar_item()

    assert guerra.vida > 70
    assert batalha.condicao_vitoria() in {"em_andamento", "vitoria", "derrota"}


def test_batalha_condicao_vitoria_e_derrota():
    guerreiro = Guerreiro("Arthur")
    chefe = ChefeFinal("Boss")
    batalha = Batalha(guerreiro, chefe)

    chefe.receber_dano(500)
    assert batalha.condicao_vitoria() == "vitoria"

    guerreiro2 = Guerreiro("Arthur")
    chefe2 = ChefeFinal("Boss")
    batalha2 = Batalha(guerreiro2, chefe2)
    guerreiro2.receber_dano(500)
    assert batalha2.condicao_vitoria() == "derrota"
