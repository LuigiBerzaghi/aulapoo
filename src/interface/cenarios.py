"""Cenários de batalha gerados por código, um para cada vilão."""

import math
import random

import pygame

from . import graficos, tema
from .efeitos import Particula

L, A = tema.LARGURA, tema.ALTURA
HORIZONTE = 445

_fundos = {}


def _montanhas(surf, cor, base, amplitude, semente, suavidade=60):
    rng = random.Random(semente)
    pontos = [(0, A)]
    y = base - rng.uniform(0, amplitude)
    for x in range(0, L + suavidade, suavidade):
        y = max(base - amplitude, min(base - 10, y + rng.uniform(-amplitude * 0.45, amplitude * 0.45)))
        pontos.append((x, y))
    pontos.append((L, A))
    pygame.draw.polygon(surf, cor, pontos)


def _pinheiro(surf, cor, x, base, altura):
    largura = altura * 0.36
    camadas = 4
    for i in range(camadas):
        topo = base - altura + i * altura * 0.18
        baixo = topo + altura * 0.42
        meia = largura * (0.45 + i * 0.2) / 2
        pygame.draw.polygon(surf, cor, [(x, topo), (x + meia, baixo), (x - meia, baixo)])
    pygame.draw.rect(surf, cor, (x - altura * 0.025, base - altura * 0.2, altura * 0.05, altura * 0.2))


def _estrelas(surf, quantidade, limite_y, semente):
    rng = random.Random(semente)
    for _ in range(quantidade):
        x, y = rng.randrange(L), rng.randrange(int(limite_y))
        brilho = rng.randint(90, 230)
        surf.set_at((x, y), (brilho, brilho, min(255, brilho + 20)))
        if rng.random() < 0.08:
            graficos.desenhar_brilho(surf, (x, y), 6, (brilho, brilho, brilho), 0.6)


def _lua(surf, centro, raio, cor, halo):
    graficos.desenhar_brilho(surf, centro, raio * 5, halo, 0.9)
    pygame.draw.circle(surf, cor, centro, raio)
    sombra = graficos.escurecer(cor, 0.88)
    rng = random.Random(7)
    for _ in range(6):
        ang = rng.uniform(0, math.tau)
        dist = rng.uniform(0, raio * 0.6)
        pygame.draw.circle(surf, sombra, (int(centro[0] + math.cos(ang) * dist), int(centro[1] + math.sin(ang) * dist)), rng.randint(3, raio // 4))


def _chao(surf, cores, inicio=HORIZONTE):
    surf.blit(graficos.gradiente_vertical((L, A - inicio), cores), (0, inicio))


def _castelo(surf, cor, x, base, escala, janela=None, quebrado=False, semente=3):
    rng = random.Random(semente)
    torres = [(-170, 120, 260), (-90, 70, 190), (-20, 90, 330), (70, 70, 230), (150, 110, 280)]
    for dx, largura, altura in torres:
        largura *= escala * 0.5
        altura *= escala
        esquerda = x + dx * escala
        topo = base - altura
        pygame.draw.rect(surf, cor, (esquerda, topo, largura, altura))
        if quebrado:
            pontos = [(esquerda, topo)]
            passos = 5
            for i in range(1, passos):
                pontos.append((esquerda + largura * i / passos, topo - rng.uniform(-10, 34) * escala))
            pontos.append((esquerda + largura, topo))
            pontos.append((esquerda + largura, topo + 2))
            pontos.append((esquerda, topo + 2))
            pygame.draw.polygon(surf, cor, pontos)
        else:
            for i in range(int(largura // (14 * escala))):
                if i % 2 == 0:
                    pygame.draw.rect(surf, cor, (esquerda + i * 14 * escala, topo - 12 * escala, 10 * escala, 12 * escala))
            pygame.draw.polygon(surf, cor, [(esquerda - 4, topo), (esquerda + largura / 2, topo - altura * 0.28), (esquerda + largura + 4, topo)])
        if janela:
            for _ in range(2):
                jx = esquerda + rng.uniform(0.25, 0.65) * largura
                jy = topo + rng.uniform(0.2, 0.6) * altura
                graficos.desenhar_brilho(surf, (jx + 3, jy + 6), int(16 * escala), janela, 0.5)
                pygame.draw.rect(surf, janela, (jx, jy, 6 * escala, 12 * escala))
    pygame.draw.rect(surf, cor, (x - 180 * escala, base - 90 * escala, 400 * escala, 90 * escala))


def _pilar(surf, x, topo, base, largura, cor, borda):
    pygame.draw.rect(surf, cor, (x - largura // 2, topo, largura, base - topo))
    pygame.draw.rect(surf, borda, (x - largura // 2 - 8, topo, largura + 16, 22))
    pygame.draw.rect(surf, borda, (x - largura // 2 - 8, base - 26, largura + 16, 26))
    pygame.draw.line(surf, graficos.clarear(cor, 0.06), (x - largura // 2 + 8, topo + 22), (x - largura // 2 + 8, base - 26), 3)
    pygame.draw.line(surf, graficos.escurecer(cor, 0.7), (x + largura // 2 - 8, topo + 22), (x + largura // 2 - 8, base - 26), 4)


def _floresta():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(4, 10, 18), (10, 30, 36), (28, 66, 60)]), (0, 0))
    _estrelas(s, 140, 300, 11)
    _lua(s, (1000, 130), 44, (224, 240, 214), (60, 90, 70))
    _montanhas(s, (16, 40, 42), HORIZONTE, 120, 4)
    rng = random.Random(5)
    for _ in range(46):
        _pinheiro(s, (12, 30, 32), rng.uniform(0, L), HORIZONTE + 10, rng.uniform(110, 200))
    _chao(s, [(24, 40, 30), (14, 24, 18), (6, 10, 8)])
    for _ in range(28):
        _pinheiro(s, (8, 20, 20), rng.uniform(0, L), HORIZONTE + 28, rng.uniform(150, 230))
    for x in (40, 150, 1130, 1240):
        _pinheiro(s, (3, 8, 8), x + rng.uniform(-20, 20), A + 40, rng.uniform(560, 700))
    for _ in range(140):
        x, y = rng.uniform(0, L), rng.uniform(HORIZONTE + 30, A)
        pygame.draw.line(s, (12, 26, 16), (x, y), (x + rng.uniform(-4, 4), y - rng.uniform(6, 16)), 2)
    return s


def _cripta():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(8, 10, 14), (22, 26, 32), (34, 38, 44)]), (0, 0))
    rng = random.Random(9)
    for linha in range(0, HORIZONTE, 26):
        desloc = 0 if (linha // 26) % 2 == 0 else 40
        pygame.draw.line(s, (18, 20, 26), (0, linha), (L, linha), 2)
        for x in range(-desloc, L, 80):
            pygame.draw.line(s, (18, 20, 26), (x, linha), (x, linha + 26), 2)
    for cx in (270, 640, 1010):
        pygame.draw.rect(s, (5, 6, 9), (cx - 110, 170, 220, HORIZONTE - 170))
        pygame.draw.ellipse(s, (5, 6, 9), (cx - 110, 60, 220, 220))
        pygame.draw.arc(s, (44, 48, 56), (cx - 118, 52, 236, 236), 0, math.pi, 8)
    _chao(s, [(30, 32, 38), (16, 18, 22), (6, 7, 9)])
    for i in range(1, 9):
        y = HORIZONTE + (A - HORIZONTE) * (i / 9) ** 1.6
        pygame.draw.line(s, (12, 13, 16), (0, y), (L, y), 2)
    for i in range(-8, 9):
        pygame.draw.line(s, (12, 13, 16), (640 + i * 60, HORIZONTE), (640 + i * 260, A), 2)
    for x in (90, 455, 825, 1190):
        _pilar(s, x, 0, HORIZONTE + 20, 64, (34, 36, 44), (46, 48, 58))
    for _ in range(18):
        x, y = rng.uniform(0, L), rng.uniform(HORIZONTE + 60, A - 20)
        pygame.draw.circle(s, (70, 68, 60), (int(x), int(y)), rng.randint(3, 6))
    return s


def _ruinas():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(14, 2, 4), (60, 12, 10), (150, 50, 18), (226, 110, 40)]), (0, 0))
    graficos.desenhar_brilho(s, (640, HORIZONTE), 520, (120, 40, 10), 1.0)
    rng = random.Random(13)
    for _ in range(26):
        x, y = rng.uniform(0, L), rng.uniform(0, 240)
        pygame.draw.ellipse(s, (30, 8, 8), (x - 120, y - 30, 240, 60))
    _montanhas(s, (40, 10, 8), HORIZONTE, 70, 2, 80)
    _castelo(s, (22, 6, 6), 640, HORIZONTE + 6, 1.2, (255, 140, 40), quebrado=True)
    _castelo(s, (14, 4, 4), 140, HORIZONTE + 10, 0.7, (255, 120, 30), quebrado=True, semente=8)
    _castelo(s, (14, 4, 4), 1150, HORIZONTE + 10, 0.8, (255, 120, 30), quebrado=True, semente=21)
    _chao(s, [(46, 14, 8), (20, 6, 4), (6, 2, 2)])
    for _ in range(24):
        x, y = rng.uniform(0, L), rng.uniform(HORIZONTE + 30, A)
        largura = rng.uniform(20, 70)
        pygame.draw.polygon(s, (14, 4, 4), [(x, y), (x + largura, y + 4), (x + largura * 0.7, y - largura * 0.3), (x + 10, y - largura * 0.25)])
    return s


def _torre():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(6, 2, 14), (24, 8, 44), (66, 22, 92)]), (0, 0))
    _estrelas(s, 220, 380, 17)
    _lua(s, (250, 120), 60, (230, 200, 255), (70, 30, 100))
    rng = random.Random(19)
    for _ in range(7):
        x, y, r = rng.uniform(80, 1200), rng.uniform(120, 340), rng.uniform(20, 50)
        pygame.draw.polygon(s, (20, 8, 32), [(x - r, y), (x + r, y), (x + r * 0.5, y + r * 0.9), (x, y + r * 1.4), (x - r * 0.6, y + r * 0.8)])
        pygame.draw.line(s, (60, 28, 90), (x - r, y), (x + r, y), 2)
    _montanhas(s, (22, 8, 34), HORIZONTE, 90, 6)
    torre_x = 980
    pygame.draw.polygon(s, (12, 4, 20), [(torre_x - 70, HORIZONTE), (torre_x - 46, 90), (torre_x + 46, 90), (torre_x + 70, HORIZONTE)])
    pygame.draw.polygon(s, (12, 4, 20), [(torre_x - 70, 96), (torre_x, -20), (torre_x + 70, 96)])
    for jy in (140, 220, 300, 370):
        graficos.desenhar_brilho(s, (torre_x, jy + 10), 30, (190, 90, 255), 0.7)
        pygame.draw.rect(s, (220, 150, 255), (torre_x - 5, jy, 10, 20))
    _chao(s, [(34, 14, 48), (18, 6, 26), (6, 2, 10)])
    centro = (640, tema.CHAO_Y + 10)
    for i, raio in enumerate((430, 380, 300)):
        pygame.draw.ellipse(s, (70 - i * 8, 30, 110 - i * 10), (centro[0] - raio, centro[1] - raio * 0.22, raio * 2, raio * 0.44), 2)
    for i in range(24):
        ang = i / 24 * math.tau
        x = centro[0] + math.cos(ang) * 405
        y = centro[1] + math.sin(ang) * 405 * 0.22
        pygame.draw.line(s, (90, 40, 140), (x - 6, y), (x + 6, y - 6), 2)
    return s


def _desfiladeiro():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(18, 22, 32), (48, 58, 72), (96, 104, 112)]), (0, 0))
    _montanhas(s, (70, 78, 90), HORIZONTE - 40, 110, 31, 40)
    _montanhas(s, (50, 58, 70), HORIZONTE, 80, 32, 50)
    rng = random.Random(23)
    for lado, inicio in ((-1, 0), (1, L)):
        for camada, (cor, largura) in enumerate((((40, 46, 58), 330), ((22, 26, 34), 250), ((10, 12, 16), 170))):
            pontos = [(inicio, -10)]
            y = -10
            while y < A + 40:
                x = inicio - lado * (largura + rng.uniform(-50, 40))
                pontos.append((x, y))
                y += rng.uniform(40, 90)
            pontos.append((inicio, A + 40))
            pygame.draw.polygon(s, cor, pontos)
    _chao(s, [(46, 50, 56), (24, 26, 30), (10, 11, 14)], HORIZONTE + 10)
    for _ in range(30):
        x, y = rng.uniform(220, 1060), rng.uniform(HORIZONTE + 40, A)
        pygame.draw.ellipse(s, (20, 22, 26), (x, y, rng.uniform(10, 40), rng.uniform(5, 12)))
    return s


def _trono():
    s = pygame.Surface((L, A))
    s.blit(graficos.gradiente_vertical((L, HORIZONTE), [(3, 3, 8), (8, 10, 22), (16, 18, 36)]), (0, 0))
    janela = pygame.Rect(540, 40, 200, 300)
    pygame.draw.rect(s, (24, 40, 78), (janela.x, janela.y + 100, janela.w, janela.h - 100))
    pygame.draw.ellipse(s, (24, 40, 78), (janela.x, janela.y, janela.w, 200))
    graficos.desenhar_brilho(s, janela.center, 260, (30, 60, 120), 0.9)
    pygame.draw.circle(s, (200, 220, 255), (640, 150), 34)
    pygame.draw.line(s, (6, 6, 12), (640, 40), (640, 340), 6)
    pygame.draw.line(s, (6, 6, 12), (540, 200), (740, 200), 6)
    pygame.draw.arc(s, (40, 44, 70), (janela.x - 10, janela.y - 10, janela.w + 20, 220), 0, math.pi, 8)
    for bx in (300, 980):
        pygame.draw.polygon(s, (70, 12, 24), [(bx - 40, 40), (bx + 40, 40), (bx + 40, 300), (bx, 340), (bx - 40, 300)])
        pygame.draw.polygon(s, (130, 110, 70), [(bx - 40, 40), (bx + 40, 40), (bx + 40, 300), (bx, 340), (bx - 40, 300)], 3)
        pygame.draw.polygon(s, (130, 110, 70), [(bx, 150), (bx + 16, 180), (bx, 210), (bx - 16, 180)])
    _chao(s, [(22, 22, 36), (12, 12, 22), (4, 4, 8)])
    pygame.draw.polygon(s, (60, 10, 20), [(600, HORIZONTE - 10), (680, HORIZONTE - 10), (930, A), (350, A)])
    pygame.draw.polygon(s, (110, 90, 50), [(600, HORIZONTE - 10), (680, HORIZONTE - 10), (930, A), (350, A)], 3)
    for degrau in range(3):
        pygame.draw.rect(s, (30, 30, 46), (520 - degrau * 30, HORIZONTE - 30 + degrau * 12, 240 + degrau * 60, 14))
    pygame.draw.polygon(s, (8, 8, 14), [(590, HORIZONTE - 30), (600, 280), (620, 250), (640, 220), (660, 250), (680, 280), (690, HORIZONTE - 30)])
    for x in (120, 360, 920, 1160):
        _pilar(s, x, 0, HORIZONTE + 30, 72, (20, 20, 32), (34, 34, 52))
    return s


_CENARIOS = {
    "floresta": (_floresta, (190, 255, 110)),
    "cripta": (_cripta, (110, 255, 160)),
    "ruinas": (_ruinas, (255, 140, 40)),
    "torre": (_torre, (200, 110, 255)),
    "desfiladeiro": (_desfiladeiro, (200, 210, 230)),
    "trono": (_trono, (110, 170, 255)),
}

TOCHAS = {
    "cripta": [(90, 200), (455, 200), (825, 200), (1190, 200)],
    "trono": [(120, 230), (360, 230), (920, 230), (1160, 230)],
}


def fundo(nome):
    if nome not in _fundos:
        _fundos[nome] = _CENARIOS[nome][0]()
    return _fundos[nome]


def miniatura(nome, tamanho):
    imagem = fundo(nome)
    largura, altura = tamanho
    proporcao = altura / A
    recorte_largura = int(largura / proporcao)
    recorte = pygame.Rect(0, 0, recorte_largura, A)
    recorte.centerx = 640
    return pygame.transform.smoothscale(imagem.subsurface(recorte), tamanho)


def _nevoa(cor, semente):
    rng = random.Random(semente)
    camada = pygame.Surface((L * 2, 260), pygame.SRCALPHA)
    for _ in range(60):
        x = rng.uniform(0, L * 2 - 420)
        y = rng.uniform(60, 200)
        largura = int(rng.uniform(180, 420))
        altura = int(rng.uniform(40, 90))
        bolha = pygame.Surface((largura, altura), pygame.SRCALPHA)
        for k in range(4, 0, -1):
            caixa = pygame.Rect(0, 0, largura * k // 4, altura * k // 4)
            caixa.center = (largura // 2, altura // 2)
            pygame.draw.ellipse(bolha, (*cor, 7 * (5 - k)), caixa)
        camada.blit(bolha, (x, y - altura // 2))
    return graficos.desfocar(camada, 6)


class Cenario:

    def __init__(self, nome):
        self.nome = nome
        self.fundo = fundo(nome)
        self.cor = _CENARIOS[nome][1]
        self.t = 0.0
        self.acumulado = 0.0
        self.vinheta = graficos.vinheta((L, A), 210)
        cores_nevoa = {
            "floresta": (150, 200, 180),
            "cripta": (120, 160, 140),
            "desfiladeiro": (210, 220, 230),
            "trono": (90, 110, 170),
            "torre": (170, 110, 220),
            "ruinas": (90, 40, 30),
        }
        self.nevoa = _nevoa(cores_nevoa[nome], len(nome))
        self.forca_nevoa = 255 if nome == "desfiladeiro" else 150

    def atualizar(self, dt, particulas):
        self.t += dt
        taxas = {"floresta": 7, "cripta": 6, "ruinas": 30, "torre": 12, "desfiladeiro": 10, "trono": 14}
        self.acumulado += dt * taxas[self.nome]
        while self.acumulado >= 1:
            self.acumulado -= 1
            self._emitir(particulas)

    def _emitir(self, particulas):
        r = random.random
        if self.nome == "floresta":
            particulas.adicionar(Particula(r() * L, 200 + r() * 420, (r() - 0.5) * 24, -6 - r() * 14, 3 + r() * 3, (190, 255, 110), 1.6 + r() * 1.6, encolhe=False, oscila=24))
        elif self.nome == "cripta":
            if r() < 0.7:
                particulas.adicionar(Particula(r() * L, r() * A, 4 + r() * 8, 4 + r() * 6, 4 + r() * 3, (170, 170, 160, 90), 1 + r() * 1.5, brilha=False, encolhe=False))
            else:
                x, y = random.choice(TOCHAS["cripta"])
                particulas.adicionar(Particula(x + (r() - 0.5) * 10, y, (r() - 0.5) * 10, -30 - r() * 30, 0.6 + r() * 0.5, (110, 255, 160), 3 + r() * 2))
        elif self.nome == "ruinas":
            if r() < 0.85:
                particulas.adicionar(Particula(r() * L, A + 10, (r() - 0.3) * 40, -60 - r() * 110, 3 + r() * 3, random.choice([(255, 140, 40), (255, 90, 20), (255, 200, 90)]), 1.2 + r() * 2, encolhe=True, oscila=40))
            else:
                particulas.adicionar(Particula(r() * L, -10, 10 + r() * 20, 30 + r() * 30, 8, (60, 50, 50, 140), 1.5 + r() * 2, brilha=False, encolhe=False))
        elif self.nome == "torre":
            particulas.adicionar(Particula(640 + (r() - 0.5) * 820, tema.CHAO_Y + 10 + (r() - 0.5) * 120, (r() - 0.5) * 10, -20 - r() * 40, 2 + r() * 2.5, random.choice([(200, 110, 255), (150, 90, 255), (255, 160, 255)]), 1.5 + r() * 2, oscila=16))
        elif self.nome == "desfiladeiro":
            particulas.adicionar(Particula(r() * L, r() * A, 20 + r() * 20, 2 + r() * 4, 5 + r() * 3, (210, 220, 235, 26), 30 + r() * 40, brilha=False, encolhe=False))
        elif self.nome == "trono":
            if r() < 0.6:
                x, y = random.choice(TOCHAS["trono"])
                particulas.adicionar(Particula(x + (r() - 0.5) * 12, y, (r() - 0.5) * 12, -40 - r() * 40, 0.5 + r() * 0.5, (110, 170, 255), 3 + r() * 2.5))
            else:
                particulas.adicionar(Particula(r() * L, -10, (r() - 0.5) * 10, 20 + r() * 25, 9, (120, 120, 140, 120), 1 + r() * 1.5, brilha=False, encolhe=False, oscila=20))

    def desenhar_fundo(self, tela, deslocamento=(0, 0)):
        tela.blit(self.fundo, (deslocamento[0] * 0.4 - 0, deslocamento[1] * 0.4))
        for x, y in TOCHAS.get(self.nome, []):
            tremula = 0.75 + 0.25 * math.sin(self.t * 11 + x) * math.sin(self.t * 7.3 + y)
            graficos.desenhar_brilho(tela, (x, y), 110, self.cor, 0.55 * tremula)
            pygame.draw.polygon(tela, (40, 36, 40), [(x - 12, y + 6), (x + 12, y + 6), (x + 6, y + 30), (x - 6, y + 30)])
            chama = 14 + 4 * tremula
            pygame.draw.polygon(tela, self.cor, [(x - 8, y + 6), (x, y + 6 - chama * 1.6), (x + 8, y + 6)])
            pygame.draw.polygon(tela, (240, 250, 255), [(x - 4, y + 6), (x, y + 6 - chama * 0.8), (x + 4, y + 6)])
        if self.nome == "torre":
            pulso = 0.35 + 0.2 * math.sin(self.t * 2)
            graficos.desenhar_brilho(tela, (640, tema.CHAO_Y + 10), 360, (90, 30, 140), pulso)
        if self.nome == "ruinas":
            pulso = 0.5 + 0.15 * math.sin(self.t * 3.1) * math.sin(self.t * 1.7)
            graficos.desenhar_brilho(tela, (640, HORIZONTE + 20), 420, (110, 34, 6), pulso)

    def desenhar_nevoa(self, tela):
        largura = self.nevoa.get_width()
        x = -(self.t * 18) % (largura // 2)
        camada = graficos.com_alfa(self.nevoa, self.forca_nevoa)
        tela.blit(camada, (x - largura // 2, HORIZONTE - 70))
        tela.blit(camada, (x, HORIZONTE - 70))

    def desenhar_vinheta(self, tela):
        tela.blit(self.vinheta, (0, 0))
