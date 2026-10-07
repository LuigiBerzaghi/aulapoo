"""Personagens desenhados por código.

Todas as figuras são desenhadas olhando para a direita, num quadro de 240x300
com os pés em y=290. Os vilões são espelhados na hora de entrar na arena.
"""

import pygame

from . import tema
from .graficos import Pincel, clarear, escurecer

QUADRO = (240, 300)
PELE = (234, 196, 160)

_cache = {}


def _bota(p, cor, x, y, frente=1):
    p.poligono(cor, [(x - 11, y - 14), (x + 9, y - 14), (x + 12 + 6 * frente, y - 4), (x + 14 + 6 * frente, y), (x - 12, y)])


def guerreiro():
    p = Pincel(*QUADRO)
    aco = (156, 166, 186)
    aco_esc = (82, 90, 108)
    aco_claro = (214, 222, 236)
    ouro = (232, 186, 92)
    capa = (156, 26, 40)

    # capa ao vento
    p.poligono(escurecer(capa, 0.65), [(100, 98), (134, 96), (118, 196), (74, 272), (40, 262), (58, 200), (80, 140)])
    p.poligono(escurecer(capa, 0.85), [(100, 98), (120, 98), (96, 190), (60, 256), (52, 250), (74, 180)])

    # escudo no braço de trás
    escudo = [(64, 112), (112, 108), (114, 170), (90, 212), (66, 172)]
    p.poligono(aco_esc, escudo)
    p.poligono(capa, [(70, 118), (106, 114), (108, 166), (90, 200), (72, 168)])
    p.poligono(ouro, escudo, 3)
    p.poligono(ouro, [(89, 128), (96, 150), (89, 176), (82, 150)])

    # pernas
    p.linha(aco_esc, (112, 188), (100, 278), 19)
    p.linha(aco, (132, 188), (150, 278), 19)
    p.circulo(aco_claro, (141, 232), 8)
    _bota(p, escurecer(aco_esc, 0.8), 100, 290)
    _bota(p, aco_esc, 152, 290)

    # tronco e armadura
    p.poligono(aco, [(98, 100), (150, 100), (144, 192), (104, 192)])
    p.poligono(aco_claro, [(122, 106), (146, 106), (140, 150), (124, 152)])
    p.poligono(escurecer(aco, 0.8), [(100, 104), (118, 104), (116, 186), (106, 186)])
    p.retangulo(ouro, (101, 176, 46, 10), 3)
    p.circulo(clarear(ouro, 0.4), (124, 181), 5)
    p.poligono(capa, [(110, 190), (138, 190), (136, 236), (124, 228), (112, 236)])

    # ombreiras
    p.circulo(aco_esc, (102, 104), 15)
    p.circulo(aco, (148, 104), 18)
    p.arco(ouro, (130, 86, 36, 36), 0.2, 2.9, 3)

    # cabeça com elmo
    p.circulo(aco, (124, 72), 22)
    p.poligono(aco_claro, [(122, 52), (138, 56), (146, 70), (130, 66)])
    p.poligono(aco_esc, [(128, 66), (148, 64), (148, 86), (130, 88)])
    p.linha((30, 22, 18), (131, 73), (147, 72), 3)
    p.linha(ouro, (124, 50), (124, 92), 3)
    p.poligono(capa, [(120, 52), (108, 34), (84, 26), (60, 36), (82, 42), (104, 56)])
    p.poligono(clarear(capa, 0.2), [(118, 50), (108, 38), (88, 32), (104, 46)])

    # braço da espada
    p.linha(aco, (148, 110), (170, 150), 15)
    p.linha(aco_claro, (170, 150), (190, 136), 13)
    p.circulo(aco_esc, (192, 134), 8)

    # espada
    p.brilho((255, 240, 200), (206, 84), 32, 60)
    p.poligono((226, 232, 244), [(188, 128), (198, 134), (232, 32), (226, 22), (220, 30)])
    p.linha((255, 255, 255), (194, 126), (226, 30), 2)
    p.linha(ouro, (178, 124), (206, 142), 7)
    p.circulo(ouro, (186, 146), 6)
    return p.final()


def mago():
    p = Pincel(*QUADRO)
    manto = (46, 60, 150)
    manto_esc = (26, 32, 92)
    ouro = (232, 186, 92)
    barba = (232, 232, 240)
    madeira = (120, 80, 48)
    arcano = (110, 210, 255)

    # manto
    p.poligono(manto_esc, [(96, 104), (116, 104), (90, 288), (66, 288)])
    p.poligono(manto, [(104, 98), (146, 98), (170, 288), (82, 288)])
    p.poligono(clarear(manto, 0.12), [(128, 104), (146, 104), (168, 286), (140, 286)])
    p.linha(ouro, (82, 284), (170, 284), 5)
    p.linha(ouro, (126, 110), (126, 284), 3)
    p.retangulo(ouro, (106, 168, 44, 8), 3)
    for y in (204, 236, 264):
        p.poligono(clarear(ouro, 0.3), [(126, y - 6), (132, y), (126, y + 6), (120, y)])

    # braço de trás
    p.linha(manto_esc, (104, 108), (92, 168), 15)
    p.circulo(PELE, (92, 172), 6)

    # cabeça e barba
    p.circulo(PELE, (126, 78), 18)
    p.poligono(barba, [(116, 82), (146, 82), (142, 118), (128, 142), (114, 112)])
    p.poligono((210, 210, 222), [(122, 96), (134, 96), (128, 132)])
    p.linha(barba, (130, 84), (146, 84), 4)
    p.circulo((30, 30, 50), (138, 75), 2.5)

    # chapéu pontudo
    p.elipse(manto_esc, (84, 56, 86, 18))
    p.poligono(manto, [(100, 64), (152, 62), (138, 34), (112, 2), (90, 20), (116, 32)])
    p.linha(ouro, (100, 62), (150, 60), 4)
    p.poligono(clarear(ouro, 0.4), [(124, 36), (128, 42), (124, 48), (120, 42)])

    # cajado
    p.linha(madeira, (180, 286), (190, 66), 8)
    p.linha(clarear(madeira, 0.25), (183, 270), (191, 80), 2)
    p.poligono(madeira, [(182, 66), (198, 66), (204, 46), (190, 56), (178, 46)])
    p.brilho(arcano, (192, 44), 42, 150)
    p.circulo(arcano, (192, 44), 13)
    p.circulo(clarear(arcano, 0.7), (188, 40), 6)

    # braço do cajado
    p.linha(manto, (146, 108), (166, 150), 16)
    p.linha(manto, (166, 150), (184, 140), 14)
    p.circulo(PELE, (188, 140), 7)
    return p.final()


def arqueiro():
    p = Pincel(*QUADRO)
    verde = (48, 112, 62)
    verde_esc = (24, 62, 36)
    couro = (124, 86, 50)
    couro_esc = (78, 52, 30)
    madeira = (150, 104, 56)

    # capa
    p.poligono(verde_esc, [(100, 96), (128, 92), (104, 226), (66, 236), (78, 160)])

    # aljava
    p.poligono(couro, [(84, 92), (100, 86), (112, 168), (96, 172)])
    for x, y in ((86, 86), (92, 82), (98, 80)):
        p.linha((230, 230, 230), (x, y), (x - 6, y - 16), 3)
        p.poligono((200, 60, 60), [(x - 6, y - 16), (x - 12, y - 24), (x - 2, y - 20)])

    # pernas
    p.linha(couro_esc, (112, 188), (98, 278), 16)
    p.linha((92, 70, 48), (130, 188), (150, 278), 16)
    _bota(p, escurecer(couro_esc, 0.8), 98, 290)
    _bota(p, couro_esc, 152, 290)

    # túnica
    p.poligono(verde, [(102, 100), (144, 100), (146, 204), (100, 204)])
    p.poligono(clarear(verde, 0.15), [(124, 104), (144, 104), (144, 200), (128, 200)])
    p.linha(couro, (104, 110), (142, 180), 6)
    p.retangulo(couro_esc, (100, 178, 48, 9), 3)

    # braço de trás puxando a corda
    p.linha(verde_esc, (106, 108), (130, 124), 13)
    p.linha(verde_esc, (130, 124), (152, 118), 11)
    p.circulo(PELE, (154, 118), 6)

    # cabeça com capuz
    p.poligono(verde_esc, [(108, 58), (82, 92), (116, 92)])
    p.circulo(verde, (124, 74), 21)
    p.poligono(PELE, [(126, 68), (144, 64), (146, 86), (132, 94), (124, 84)])
    p.poligono(verde, [(120, 54), (146, 60), (146, 66), (124, 66)])
    p.circulo((30, 40, 30), (138, 74), 2.5)
    p.poligono(verde_esc, [(118, 52), (104, 36), (112, 60)])

    # braço do arco
    p.linha(verde, (146, 108), (186, 118), 12)
    p.circulo(PELE, (190, 118), 6)

    # arco e flecha
    p.arco(madeira, (154, 40, 56, 156), -1.5708, 1.5708, 6)
    p.linha(clarear(madeira, 0.3), (182, 42), (182, 194), 1)
    p.linha((235, 235, 220), (182, 42), (154, 118), 1)
    p.linha((235, 235, 220), (182, 194), (154, 118), 1)
    p.linha((190, 150, 100), (154, 118), (222, 118), 3)
    p.poligono((220, 224, 236), [(222, 112), (234, 118), (222, 124)])
    return p.final()


def goblin():
    p = Pincel(*QUADRO)
    pele = (100, 156, 64)
    pele_esc = (56, 96, 38)
    trapo = (112, 80, 52)
    olho = (255, 226, 70)

    # pernas tortas
    p.linha(pele_esc, (110, 236), (96, 286), 12)
    p.linha(pele, (130, 236), (146, 286), 12)
    p.elipse(pele_esc, (82, 280, 30, 12))
    p.elipse(pele, (136, 280, 32, 12))

    # braço de trás com garras
    p.linha(pele_esc, (106, 184), (88, 224), 10)
    for dx in (-6, 0, 6):
        p.linha(pele_esc, (88, 224), (84 + dx, 236), 3)

    # corpo curvado com trapos
    p.poligono(trapo, [(96, 176), (142, 164), (150, 244), (98, 248)])
    p.poligono(escurecer(trapo, 0.7), [(96, 236), (108, 256), (118, 240), (130, 258), (140, 242), (150, 254), (150, 236), (98, 236)])
    p.linha((70, 46, 28), (98, 210), (148, 206), 5)

    # cabeça
    p.poligono(pele_esc, [(122, 140), (70, 112), (90, 136), (116, 160)])
    p.circulo(pele, (142, 150), 28)
    p.poligono(pele, [(154, 130), (196, 98), (176, 140)])
    p.poligono(clarear(pele, 0.25), [(160, 128), (188, 106), (174, 132)])
    p.poligono(pele, [(162, 148), (186, 160), (164, 166)])
    p.brilho(olho, (158, 144), 18, 120)
    p.circulo(olho, (158, 144), 6)
    p.circulo((20, 10, 0), (160, 144), 2.5)
    p.linha(pele_esc, (146, 134), (166, 138), 4)
    p.linha((40, 20, 10), (146, 170), (166, 168), 4)
    p.poligono((240, 236, 210), [(150, 168), (154, 176), (156, 168)])
    p.poligono((240, 236, 210), [(160, 168), (163, 175), (165, 167)])

    # braço com adaga
    p.linha(pele, (140, 182), (168, 204), 10)
    p.circulo(pele_esc, (170, 204), 6)
    p.poligono((200, 206, 214), [(170, 196), (214, 176), (176, 208)])
    p.linha((90, 60, 40), (162, 206), (172, 198), 5)
    return p.final()


def esqueleto():
    p = Pincel(*QUADRO)
    osso = (228, 222, 202)
    osso_esc = (150, 144, 128)
    olho = (110, 255, 170)
    trapo = (70, 62, 84)

    # braço de trás
    p.linha(osso_esc, (102, 110), (90, 150), 6)
    p.linha(osso_esc, (90, 150), (96, 190), 5)

    # pernas
    p.linha(osso_esc, (112, 196), (104, 240), 7)
    p.linha(osso_esc, (104, 240), (100, 282), 6)
    p.linha(osso, (130, 196), (140, 240), 7)
    p.linha(osso, (140, 240), (146, 282), 6)
    p.circulo(osso, (104, 240), 6)
    p.circulo(osso, (140, 240), 6)
    p.elipse(osso_esc, (88, 278, 26, 10))
    p.elipse(osso, (136, 278, 28, 10))

    # trapos na cintura
    p.poligono(trapo, [(100, 182), (144, 182), (150, 228), (138, 214), (128, 234), (118, 212), (106, 230), (96, 214)])

    # pelve e coluna
    p.poligono(osso, [(106, 184), (138, 184), (132, 200), (112, 200)])
    p.linha(osso, (122, 104), (122, 186), 6)
    for i in range(5):
        y = 114 + i * 13
        largura = 50 - i * 5
        p.elipse(osso, (122 - largura / 2, y, largura, 11), 3)

    # ombros
    p.linha(osso, (100, 106), (146, 106), 7)

    # crânio
    p.circulo(osso, (126, 78), 22)
    p.poligono(osso, [(112, 88), (146, 88), (142, 106), (116, 106)])
    for x in range(120, 144, 5):
        p.linha(osso_esc, (x, 96), (x, 104), 2)
    p.circulo((20, 24, 22), (130, 76), 6.5)
    p.circulo((20, 24, 22), (142, 77), 5)
    p.brilho(olho, (130, 76), 16, 160)
    p.brilho(olho, (142, 77), 12, 140)
    p.circulo(olho, (130, 76), 3)
    p.circulo(olho, (142, 77), 2.5)
    p.poligono((20, 24, 22), [(140, 84), (145, 90), (137, 90)])
    p.arco(osso_esc, (106, 58, 30, 30), 1.6, 3.0, 3)

    # braço da espada
    p.linha(osso, (144, 110), (164, 150), 6)
    p.linha(osso, (164, 150), (184, 140), 6)
    p.circulo(osso, (164, 150), 5)

    # espada enferrujada
    p.poligono((150, 118, 86), [(182, 134), (192, 140), (230, 66), (226, 56), (220, 62)])
    p.poligono((110, 80, 54), [(200, 104), (208, 108), (204, 116)])
    p.linha((90, 70, 50), (174, 130), (198, 148), 6)
    return p.final()


def guerreiro_sombrio():
    p = Pincel(*QUADRO)
    armadura = (44, 42, 52)
    armadura_esc = (22, 20, 28)
    detalhe = (90, 84, 100)
    olho = (255, 60, 40)
    capa = (36, 14, 20)

    # capa rasgada
    p.poligono(capa, [(98, 96), (132, 94), (122, 190), (82, 278), (70, 262), (58, 276), (46, 250), (64, 190), (78, 140)])

    # pernas
    p.linha(armadura_esc, (110, 190), (98, 278), 21)
    p.linha(armadura, (132, 190), (152, 278), 21)
    _bota(p, armadura_esc, 98, 290)
    _bota(p, armadura_esc, 154, 290)
    p.poligono(detalhe, [(146, 226), (160, 232), (146, 240)])

    # tronco
    p.poligono(armadura, [(94, 98), (154, 98), (146, 194), (102, 194)])
    p.poligono(detalhe, [(124, 106), (148, 106), (142, 150), (126, 152)], 2)
    p.linha((150, 30, 20), (110, 130), (138, 120), 3)
    p.linha((150, 30, 20), (112, 150), (140, 142), 2)
    p.retangulo(armadura_esc, (100, 178, 48, 12), 3)
    p.brilho(olho, (124, 184), 14, 120)
    p.circulo(olho, (124, 184), 4)

    # ombreiras com espinhos
    for cx, cor in ((100, armadura_esc), (150, armadura)):
        p.circulo(cor, (cx, 104), 20)
        p.poligono(cor, [(cx - 14, 96), (cx - 8, 66), (cx - 2, 92)])
        p.poligono(cor, [(cx, 92), (cx + 8, 62), (cx + 12, 94)])
    p.arco(detalhe, (130, 84, 40, 40), 0.3, 2.8, 2)

    # elmo com chifres
    p.poligono(armadura_esc, [(108, 60), (84, 32), (92, 60)])
    p.circulo(armadura, (124, 72), 23)
    p.poligono(armadura, [(110, 56), (98, 22), (120, 52)])
    p.poligono(armadura_esc, [(128, 64), (150, 62), (150, 90), (130, 92)])
    p.brilho(olho, (142, 74), 28, 200)
    p.linha(olho, (133, 74), (149, 73), 4)
    p.linha((255, 200, 160), (137, 74), (146, 73), 2)

    # braços e montante
    p.linha(armadura, (152, 110), (172, 154), 16)
    p.linha(armadura, (172, 154), (190, 142), 14)
    p.circulo(armadura_esc, (194, 140), 9)
    p.brilho((255, 70, 30), (214, 74), 26, 90)
    p.poligono((60, 56, 66), [(186, 132), (202, 140), (238, 16), (232, 4), (222, 12)])
    p.linha((255, 80, 40), (200, 134), (236, 12), 2)
    p.linha((120, 30, 20), (172, 124), (212, 150), 8)
    return p.final()


def mago_sombrio():
    p = Pincel(*QUADRO)
    manto = (52, 26, 76)
    manto_esc = (24, 10, 38)
    detalhe = (150, 70, 220)
    olho = (220, 120, 255)

    # manto flutuante com barra rasgada
    p.poligono(manto_esc, [(94, 98), (118, 98), (90, 262), (62, 250)])
    p.poligono(manto, [(100, 94), (150, 94), (176, 250), (162, 240), (150, 262), (136, 244), (122, 264), (108, 244), (92, 262), (84, 250)])
    p.poligono(clarear(manto, 0.08), [(128, 100), (150, 100), (172, 244), (152, 240)])
    for y in (150, 196, 232):
        p.linha(detalhe, (110 + (y - 150) * 0.05, y), (150 + (y - 150) * 0.12, y), 2)
    p.brilho(detalhe, (128, 172), 26, 70)
    p.poligono(detalhe, [(128, 162), (136, 172), (128, 182), (120, 172)])

    # braço de trás
    p.linha(manto_esc, (104, 106), (88, 160), 16)

    # capuz
    p.poligono(manto_esc, [(108, 50), (80, 104), (112, 100)])
    p.circulo(manto, (126, 74), 26)
    p.poligono(manto, [(118, 52), (96, 18), (134, 48)])
    p.poligono((6, 2, 12), [(124, 62), (152, 64), (150, 98), (128, 96)])
    p.brilho(olho, (140, 76), 26, 200)
    p.circulo(olho, (136, 76), 3)
    p.circulo(olho, (147, 76), 3)

    # cajado das runas
    p.linha((40, 30, 50), (184, 270), (192, 60), 7)
    p.poligono((70, 50, 90), [(176, 70), (192, 30), (208, 70), (192, 58)])
    p.brilho(olho, (192, 52), 46, 170)
    p.circulo(olho, (192, 52), 11)
    p.circulo((255, 230, 255), (190, 49), 5)

    # braço do cajado
    p.linha(manto, (148, 106), (170, 146), 16)
    p.linha(manto, (170, 146), (186, 138), 14)
    p.circulo((150, 140, 170), (190, 138), 6)
    return p.final()


def arqueiro_sombrio():
    p = Pincel(*QUADRO)
    cinza = (46, 48, 58)
    cinza_esc = (22, 22, 30)
    couro = (60, 40, 36)
    olho = (255, 70, 90)

    # capa esfarrapada
    p.poligono(cinza_esc, [(100, 94), (128, 90), (108, 220), (90, 210), (78, 236), (66, 200), (80, 150)])

    # aljava
    p.poligono(couro, [(84, 90), (100, 84), (112, 166), (96, 170)])
    for x, y in ((86, 84), (92, 80), (98, 78)):
        p.linha((90, 90, 100), (x, y), (x - 6, y - 16), 3)
        p.poligono((30, 30, 36), [(x - 6, y - 16), (x - 12, y - 24), (x - 2, y - 20)])

    # pernas
    p.linha(cinza_esc, (112, 188), (98, 278), 16)
    p.linha(cinza, (130, 188), (150, 278), 16)
    _bota(p, cinza_esc, 98, 290)
    _bota(p, cinza_esc, 152, 290)

    # túnica
    p.poligono(cinza, [(102, 98), (144, 98), (146, 204), (100, 204)])
    p.linha(couro, (104, 108), (142, 180), 6)
    p.retangulo(cinza_esc, (100, 178, 48, 9), 3)

    # braço de trás
    p.linha(cinza_esc, (106, 108), (130, 124), 13)
    p.linha(cinza_esc, (130, 124), (152, 118), 11)

    # capuz com máscara
    p.poligono(cinza_esc, [(108, 56), (80, 92), (116, 92)])
    p.circulo(cinza, (124, 74), 22)
    p.poligono((10, 10, 14), [(124, 62), (148, 64), (148, 92), (128, 92)])
    p.poligono(cinza, [(118, 50), (100, 24), (130, 50)])
    p.brilho(olho, (140, 74), 22, 190)
    p.linha(olho, (134, 74), (146, 72), 3)

    # braço do arco
    p.linha(cinza, (146, 108), (186, 118), 12)

    # arco negro com corda incandescente
    p.arco((30, 26, 30), (154, 36, 58, 164), -1.5708, 1.5708, 7)
    p.brilho(olho, (170, 118), 40, 60)
    p.linha(olho, (183, 38), (152, 118), 2)
    p.linha(olho, (183, 198), (152, 118), 2)
    p.linha((60, 50, 50), (152, 118), (222, 118), 3)
    p.poligono((200, 60, 80), [(222, 112), (234, 118), (222, 124)])
    return p.final()


def chefe_final():
    p = Pincel(*QUADRO)
    armadura = (30, 32, 48)
    armadura_esc = (14, 14, 24)
    runa = (110, 180, 255)
    capa = (18, 16, 36)
    ouro = (170, 150, 110)

    # capa imensa
    p.poligono(capa, [(96, 92), (140, 88), (130, 180), (96, 290), (30, 290), (20, 250), (52, 170), (74, 120)])
    p.poligono(clarear(capa, 0.08), [(96, 92), (116, 92), (88, 210), (40, 284), (34, 270), (66, 180)])
    p.poligono((60, 16, 30), [(98, 96), (124, 94), (100, 170), (70, 226), (80, 160)])

    # pernas
    p.linha(armadura_esc, (110, 192), (98, 278), 22)
    p.linha(armadura, (134, 192), (154, 278), 22)
    _bota(p, armadura_esc, 98, 290)
    _bota(p, armadura_esc, 156, 290)
    p.linha(runa, (146, 222), (152, 252), 2)

    # tronco
    p.poligono(armadura, [(92, 96), (158, 96), (150, 198), (100, 198)])
    p.poligono(armadura_esc, [(98, 100), (118, 100), (114, 192), (104, 192)])
    p.brilho(runa, (130, 136), 34, 110)
    p.poligono(runa, [(130, 118), (142, 136), (130, 154), (118, 136)], 2)
    p.circulo(clarear(runa, 0.5), (130, 136), 4)
    p.retangulo(armadura_esc, (98, 180, 54, 12), 3)
    p.linha(ouro, (100, 186), (150, 186), 2)

    # ombreiras
    for cx, cor in ((98, armadura_esc), (152, armadura)):
        p.circulo(cor, (cx, 102), 22)
        p.arco(ouro, (cx - 22, 80, 44, 44), 0.2, 2.9, 2)
        p.poligono(cor, [(cx - 6, 86), (cx + 4, 50), (cx + 10, 88)])

    # elmo com coroa e chifres
    p.poligono(armadura_esc, [(108, 62), (70, 22), (60, 40), (96, 70)])
    p.circulo(armadura, (126, 72), 24)
    p.poligono(armadura, [(136, 56), (176, 10), (184, 26), (148, 66)])
    p.poligono(ouro, [(108, 54), (112, 36), (120, 50), (126, 30), (132, 50), (140, 36), (144, 54)])
    p.poligono(armadura_esc, [(130, 64), (152, 62), (152, 92), (132, 94)])
    p.brilho(runa, (144, 76), 34, 220)
    p.circulo(clarear(runa, 0.6), (140, 75), 3)
    p.circulo(clarear(runa, 0.6), (150, 75), 3)

    # braço e foice
    p.linha(armadura, (156, 110), (176, 156), 18)
    p.linha(armadura, (176, 156), (192, 140), 16)
    p.circulo(armadura_esc, (196, 138), 10)
    p.linha((40, 34, 44), (204, 288), (196, 18), 8)
    p.brilho(runa, (178, 40), 38, 110)
    p.poligono((150, 170, 200), [(198, 22), (194, 34), (140, 46), (100, 76), (128, 40), (160, 22)])
    p.linha(clarear(runa, 0.4), (196, 24), (110, 70), 2)
    p.circulo(runa, (198, 24), 5)
    return p.final()


DESENHOS = {
    "guerreiro": guerreiro,
    "mago": mago,
    "arqueiro": arqueiro,
    "goblin": goblin,
    "esqueleto": esqueleto,
    "guerreirosombrio": guerreiro_sombrio,
    "magosombrio": mago_sombrio,
    "arqueirosombrio": arqueiro_sombrio,
    "chefefinal": chefe_final,
}


def sprite(chave, altura=None, espelhar=False):
    """Devolve a figura pronta, em cache, com a escala definida no tema."""
    chave = chave.lower()
    altura = altura or int(QUADRO[1] * tema.ESCALA_FIGURA.get(chave, 1.0))
    identificador = (chave, altura, espelhar)
    if identificador not in _cache:
        base = _cache.get((chave, None, False))
        if base is None:
            base = DESENHOS[chave]()
            _cache[(chave, None, False)] = base
        largura = int(base.get_width() * altura / base.get_height())
        imagem = pygame.transform.smoothscale(base, (largura, altura))
        if espelhar:
            imagem = pygame.transform.flip(imagem, True, False)
        _cache[identificador] = imagem
    return _cache[identificador]


# Centro do rosto de cada figura no quadro 240x300, usado nos retratos.
ROSTOS = {
    "guerreiro": (128, 76),
    "mago": (128, 82),
    "arqueiro": (128, 76),
    "goblin": (146, 152),
    "esqueleto": (128, 84),
    "guerreirosombrio": (128, 78),
    "magosombrio": (130, 78),
    "arqueirosombrio": (128, 76),
    "chefefinal": (130, 74),
}


def retrato(chave, espelhar=False, lado=120):
    """Recorte quadrado em volta do rosto da figura."""
    identificador = ("retrato", chave, espelhar, lado)
    if identificador not in _cache:
        base = sprite(chave, QUADRO[1])
        fx, fy = ROSTOS.get(chave, (124, 80))
        recorte = pygame.Rect(0, 0, 112, 112)
        recorte.center = (fx, fy + 18)
        recorte.clamp_ip(base.get_rect())
        imagem = pygame.transform.smoothscale(base.subsurface(recorte), (lado, lado))
        if espelhar:
            imagem = pygame.transform.flip(imagem, True, False)
        _cache[identificador] = imagem
    return _cache[identificador]


def silhueta(imagem, cor=(255, 255, 255)):
    branca = imagem.copy()
    branca.fill((*cor, 0), special_flags=pygame.BLEND_RGBA_MAX)
    branca.fill((*cor, 255), special_flags=pygame.BLEND_RGBA_MIN)
    return branca
