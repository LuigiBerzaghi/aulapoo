import math
import random

import pygame

from . import graficos, tema


class Particula:
    __slots__ = ("x", "y", "vx", "vy", "vida", "total", "cor", "tamanho", "gravidade", "arrasto", "brilha", "encolhe", "oscila")

    def __init__(self, x, y, vx, vy, vida, cor, tamanho, gravidade=0.0, arrasto=0.0, brilha=True, encolhe=True, oscila=0.0):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.vida = self.total = vida
        self.cor = cor
        self.tamanho = tamanho
        self.gravidade = gravidade
        self.arrasto = arrasto
        self.brilha = brilha
        self.encolhe = encolhe
        self.oscila = oscila


class Particulas:

    def __init__(self, limite=900):
        self.lista = []
        self.limite = limite
        self.camada = pygame.Surface((tema.LARGURA, tema.ALTURA), pygame.SRCALPHA)

    def adicionar(self, particula):
        if len(self.lista) < self.limite:
            self.lista.append(particula)

    def explosao(self, x, y, quantidade, cor, velocidade=(80, 260), angulo=(0, 360), vida=(0.4, 0.9),
                 tamanho=(2, 5), gravidade=0.0, arrasto=2.0, brilha=True, espalhar=0, encolhe=True):
        for _ in range(quantidade):
            a = math.radians(random.uniform(*angulo))
            v = random.uniform(*velocidade)
            self.adicionar(Particula(
                x + random.uniform(-espalhar, espalhar),
                y + random.uniform(-espalhar, espalhar),
                math.cos(a) * v,
                -math.sin(a) * v,
                random.uniform(*vida),
                cor if not callable(cor) else cor(),
                random.uniform(*tamanho),
                gravidade,
                arrasto,
                brilha,
                encolhe,
            ))

    def atualizar(self, dt):
        vivas = []
        for p in self.lista:
            p.vida -= dt
            if p.vida <= 0:
                continue
            p.vy += p.gravidade * dt
            if p.arrasto:
                fator = max(0.0, 1 - p.arrasto * dt)
                p.vx *= fator
                p.vy *= fator
            p.x += p.vx * dt
            if p.oscila:
                p.x += math.sin(p.vida * 3 + p.y * 0.05) * p.oscila * dt
            p.y += p.vy * dt
            vivas.append(p)
        self.lista = vivas

    def desenhar(self, tela, deslocamento=(0, 0)):
        ox, oy = deslocamento
        usou_camada = False
        for p in self.lista:
            fracao = p.vida / p.total
            entrada = min(1.0, (p.total - p.vida) / 0.08) if p.total > 0.3 else 1.0
            tamanho = p.tamanho * (fracao if p.encolhe else 1.0)
            x, y = int(p.x + ox), int(p.y + oy)
            if p.brilha:
                intensidade = fracao * entrada
                graficos.desenhar_brilho(tela, (x, y), int(tamanho * 4 + 3), p.cor, intensidade * 0.9)
                if tamanho >= 1.2:
                    pygame.draw.circle(tela, graficos.misturar(p.cor, (255, 255, 255), 0.6 * intensidade), (x, y), max(1, int(tamanho * 0.7)))
            else:
                if not usou_camada:
                    self.camada.fill((0, 0, 0, 0))
                    usou_camada = True
                alfa = int(255 * min(1.0, fracao * 1.4) * entrada * (p.cor[3] / 255 if len(p.cor) > 3 else 1))
                pygame.draw.circle(self.camada, (*p.cor[:3], alfa), (x, y), max(1, int(tamanho)))
        if usou_camada:
            tela.blit(self.camada, (0, 0))


class TextoFlutuante:

    def __init__(self, conteudo, x, y, cor, tamanho=44, duracao=1.3, subida=70, atraso=0.0):
        self.imagem = graficos.texto_contorno(conteudo, tamanho, cor, (12, 6, 4), 3, titulo=True, negrito=True)
        self.x, self.y = x, y
        self.duracao = duracao
        self.subida = subida
        self.t = -atraso
        self.deriva = random.uniform(-18, 18)

    @property
    def vivo(self):
        return self.t < self.duracao

    def atualizar(self, dt):
        self.t += dt

    def desenhar(self, tela, deslocamento=(0, 0)):
        if self.t < 0:
            return
        p = self.t / self.duracao
        escala = 1.0 + 0.7 * max(0.0, 1 - self.t / 0.14) ** 2
        alfa = 255 if p < 0.65 else int(255 * (1 - (p - 0.65) / 0.35))
        imagem = self.imagem
        if escala > 1.01:
            largura, altura = imagem.get_size()
            imagem = pygame.transform.smoothscale(imagem, (int(largura * escala), int(altura * escala)))
        imagem = graficos.com_alfa(imagem, alfa)
        y = self.y - self.subida * graficos.sair_cubico(min(1.0, p * 1.4))
        x = self.x + self.deriva * p
        graficos.centralizar(tela, imagem, (x + deslocamento[0], y + deslocamento[1]))


class Corte:
    """Rastro em forma de meia-lua de um golpe de lâmina."""

    def __init__(self, x, y, direcao, cor, raio=110, duracao=0.28, inclinacao=0.0):
        self.x, self.y = x, y
        self.direcao = direcao
        self.cor = cor
        self.raio = raio
        self.duracao = duracao
        self.inclinacao = inclinacao
        self.t = 0.0
        self.camada = pygame.Surface((tema.LARGURA, tema.ALTURA), pygame.SRCALPHA)

    @property
    def vivo(self):
        return self.t < self.duracao

    def atualizar(self, dt):
        self.t += dt

    def desenhar(self, tela, deslocamento=(0, 0)):
        p = min(1.0, self.t / self.duracao)
        varredura = graficos.sair_cubico(min(1.0, p * 2.2))
        alfa = int(255 * (1 - p) ** 1.2)
        inicio = -100 + self.inclinacao
        fim = inicio + 200 * varredura
        externos, internos = [], []
        passos = 18
        for i in range(passos + 1):
            angulo = math.radians(inicio + (fim - inicio) * i / passos)
            espessura = math.sin(math.pi * i / passos) * 26 * (1 - p * 0.5)
            cx = self.x + deslocamento[0]
            cy = self.y + deslocamento[1]
            externos.append((cx + math.cos(angulo) * self.raio * self.direcao, cy + math.sin(angulo) * self.raio))
            internos.append((cx + math.cos(angulo) * (self.raio - espessura) * self.direcao, cy + math.sin(angulo) * (self.raio - espessura)))
        if len(externos) < 3:
            return
        self.camada.fill((0, 0, 0, 0))
        pontos = externos + internos[::-1]
        pygame.draw.polygon(self.camada, (*self.cor, alfa // 2), pontos)
        pygame.draw.lines(self.camada, (255, 255, 255, alfa), False, externos, 3)
        tela.blit(self.camada, (0, 0))


class Onda:
    """Anel de choque que se expande a partir do impacto."""

    def __init__(self, x, y, cor, raio_final=140, duracao=0.45, espessura=10):
        self.x, self.y = x, y
        self.cor = cor
        self.raio_final = raio_final
        self.duracao = duracao
        self.espessura = espessura
        self.t = 0.0

    @property
    def vivo(self):
        return self.t < self.duracao

    def atualizar(self, dt):
        self.t += dt

    def desenhar(self, tela, deslocamento=(0, 0)):
        p = min(1.0, self.t / self.duracao)
        raio = int(10 + (self.raio_final - 10) * graficos.sair_cubico(p))
        espessura = max(1, int(self.espessura * (1 - p)))
        intensidade = (1 - p) ** 1.5
        cor = tuple(int(c * intensidade) for c in self.cor)
        centro = (int(self.x + deslocamento[0]), int(self.y + deslocamento[1]))
        caixa = pygame.Rect(0, 0, raio * 2, int(raio * 0.7))
        caixa.center = centro
        camada = pygame.Surface(caixa.inflate(4, 4).size)
        pygame.draw.ellipse(camada, cor, camada.get_rect().inflate(-4, -4), espessura)
        tela.blit(camada, caixa.inflate(4, 4).topleft, special_flags=pygame.BLEND_RGB_ADD)


class Projetil:

    def __init__(self, origem, destino, duracao, cor, estilo="orbe", tamanho=16, arco=0.0):
        self.origem = origem
        self.destino = destino
        self.duracao = duracao
        self.cor = cor
        self.estilo = estilo
        self.tamanho = tamanho
        self.arco = arco
        self.t = 0.0
        self.anterior = origem

    @property
    def vivo(self):
        return self.t < self.duracao

    def posicao(self):
        p = min(1.0, self.t / self.duracao)
        if self.estilo != "flecha":
            p = p * p * 0.35 + p * 0.65
        x = self.origem[0] + (self.destino[0] - self.origem[0]) * p
        y = self.origem[1] + (self.destino[1] - self.origem[1]) * p - math.sin(math.pi * p) * self.arco
        return x, y

    def atualizar(self, dt, particulas):
        self.anterior = self.posicao()
        self.t += dt
        x, y = self.posicao()
        if self.estilo == "orbe":
            particulas.explosao(x, y, 3, self.cor, velocidade=(10, 60), vida=(0.25, 0.5), tamanho=(2, self.tamanho * 0.35), espalhar=self.tamanho * 0.4)
        elif self.estilo == "flecha":
            particulas.explosao(x, y, 1, self.cor, velocidade=(0, 20), vida=(0.15, 0.3), tamanho=(1.5, 2.5))

    def desenhar(self, tela, deslocamento=(0, 0)):
        x, y = self.posicao()
        x += deslocamento[0]
        y += deslocamento[1]
        if self.estilo == "orbe":
            graficos.desenhar_brilho(tela, (x, y), int(self.tamanho * 4), self.cor, 1.0)
            pygame.draw.circle(tela, graficos.clarear(self.cor, 0.6), (int(x), int(y)), int(self.tamanho * 0.75))
            pygame.draw.circle(tela, (255, 255, 255), (int(x), int(y)), int(self.tamanho * 0.4))
        else:
            ax, ay = self.anterior
            ax += deslocamento[0]
            ay += deslocamento[1]
            angulo = math.atan2(y - ay, x - ax) if (x, y) != (ax, ay) else (0 if self.destino[0] > self.origem[0] else math.pi)
            cx, cy = math.cos(angulo), math.sin(angulo)
            cauda = (x - cx * 46, y - cy * 46)
            graficos.desenhar_brilho(tela, (x, y), 26, self.cor, 0.6)
            pygame.draw.line(tela, (150, 110, 70), cauda, (x, y), 3)
            ponta = [(x + cx * 12, y + cy * 12), (x - cy * 5, y + cx * 5), (x + cy * 5, y - cx * 5)]
            pygame.draw.polygon(tela, (230, 230, 240), ponta)
            for lado in (-1, 1):
                pena = (cauda[0] - cx * 8 + lado * -cy * 6, cauda[1] - cy * 8 + lado * cx * 6)
                pygame.draw.line(tela, graficos.clarear(self.cor, 0.3), cauda, pena, 3)


class Tremor:

    def __init__(self):
        self.intensidade = 0.0

    def agitar(self, forca):
        self.intensidade = max(self.intensidade, forca)

    def atualizar(self, dt):
        self.intensidade = max(0.0, self.intensidade - dt * max(30.0, self.intensidade * 5))

    def deslocamento(self):
        if self.intensidade <= 0.3:
            return (0, 0)
        return (random.uniform(-1, 1) * self.intensidade, random.uniform(-1, 1) * self.intensidade * 0.7)


class Clarao:

    def __init__(self):
        self.cor = (255, 255, 255)
        self.alfa = 0.0
        self.velocidade = 600.0
        self.camada = pygame.Surface((tema.LARGURA, tema.ALTURA))

    def disparar(self, cor=(255, 255, 255), alfa=180, duracao=0.35):
        self.cor = cor
        self.alfa = alfa
        self.velocidade = alfa / max(0.01, duracao)

    def atualizar(self, dt):
        self.alfa = max(0.0, self.alfa - self.velocidade * dt)

    def desenhar(self, tela):
        if self.alfa <= 1:
            return
        self.camada.fill(self.cor)
        self.camada.set_alpha(int(self.alfa))
        tela.blit(self.camada, (0, 0))


class Agenda:
    """Executa funções depois de um atraso, respeitando a pausa de impacto."""

    def __init__(self):
        self.tarefas = []

    def depois(self, atraso, funcao):
        self.tarefas.append([atraso, len(self.tarefas), funcao])

    def limpar(self):
        self.tarefas = []

    @property
    def vazia(self):
        return not self.tarefas

    def atualizar(self, dt):
        for tarefa in self.tarefas:
            tarefa[0] -= dt
        prontas = sorted((t for t in self.tarefas if t[0] <= 0), key=lambda t: (t[0], t[1]))
        self.tarefas = [t for t in self.tarefas if t[0] > 0]
        for _, _, funcao in prontas:
            funcao()


class Raios:
    """Feixes de luz girando atrás de um título (tela de vitória)."""

    def __init__(self, centro, cor, quantidade=14, alcance=900):
        self.centro = centro
        self.cor = cor
        self.quantidade = quantidade
        self.alcance = alcance
        self.angulo = 0.0
        self.camada = pygame.Surface((tema.LARGURA, tema.ALTURA))

    def atualizar(self, dt):
        self.angulo += dt * 9

    def desenhar(self, tela, intensidade=1.0):
        self.camada.fill((0, 0, 0))
        cx, cy = self.centro
        # Raios mais curtos e mais claros por cima dos longos criam um degradê radial.
        for alcance, forca in ((self.alcance, 0.022), (self.alcance * 0.55, 0.06), (self.alcance * 0.3, 0.11)):
            cor = tuple(int(c * forca * intensidade) for c in self.cor)
            for i in range(self.quantidade):
                base = math.radians(self.angulo + i * 360 / self.quantidade)
                abertura = math.radians(3.2)
                pontos = [
                    (cx, cy),
                    (cx + math.cos(base - abertura) * alcance, cy + math.sin(base - abertura) * alcance),
                    (cx + math.cos(base + abertura) * alcance, cy + math.sin(base + abertura) * alcance),
                ]
                pygame.draw.polygon(self.camada, cor, pontos)
        tela.blit(self.camada, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
