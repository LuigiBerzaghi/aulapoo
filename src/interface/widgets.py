import math

import pygame

from . import graficos, tema
from .graficos import clarear, escurecer


# ---------- ícones ----------

def icone_espada(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    lamina = [(x - t * 0.55, y + t * 0.45), (x - t * 0.4, y + t * 0.6), (x + t * 0.9, y - t * 0.7), (x + t * 0.95, y - t * 0.95), (x + t * 0.7, y - t * 0.9)]
    pygame.draw.polygon(tela, cor, lamina)
    pygame.draw.line(tela, clarear(cor, 0.6), (x - t * 0.45, y + t * 0.5), (x + t * 0.85, y - t * 0.85), 1)
    pygame.draw.line(tela, escurecer(cor, 0.8), (x - t * 0.85, y + t * 0.15), (x - t * 0.15, y + t * 0.85), max(3, int(t * 0.18)))
    pygame.draw.line(tela, escurecer(cor, 0.6), (x - t * 0.55, y + t * 0.55), (x - t * 0.9, y + t * 0.9), max(3, int(t * 0.16)))


def icone_magia(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    pontos = []
    for i in range(8):
        raio = t if i % 2 == 0 else t * 0.32
        angulo = i * math.pi / 4 - math.pi / 2
        pontos.append((x + math.cos(angulo) * raio, y + math.sin(angulo) * raio))
    graficos.desenhar_brilho(tela, (x, y), int(t * 1.4), cor, 0.5)
    pygame.draw.polygon(tela, cor, pontos)
    pygame.draw.circle(tela, (255, 255, 255), (int(x), int(y)), max(2, int(t * 0.18)))
    for dx, dy, r in ((-0.8, -0.7, 0.12), (0.75, 0.6, 0.1), (0.85, -0.8, 0.08)):
        pygame.draw.circle(tela, clarear(cor, 0.5), (int(x + dx * t), int(y + dy * t)), max(1, int(r * t)))


def icone_pocao(tela, centro, tamanho, cor, liquido=(220, 50, 80)):
    x, y = centro
    t = tamanho / 2
    pygame.draw.circle(tela, cor, (int(x), int(y + t * 0.25)), int(t * 0.68))
    pygame.draw.circle(tela, liquido, (int(x), int(y + t * 0.28)), int(t * 0.56))
    pygame.draw.rect(tela, cor, (x - t * 0.22, y - t * 0.75, t * 0.44, t * 0.5))
    pygame.draw.rect(tela, (150, 100, 60), (x - t * 0.28, y - t * 0.95, t * 0.56, t * 0.25), border_radius=2)
    pygame.draw.circle(tela, clarear(liquido, 0.6), (int(x - t * 0.22), int(y + t * 0.08)), max(1, int(t * 0.14)))


def icone_troca(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    largura = max(3, int(t * 0.18))
    for sentido, altura in ((1, -0.35), (-1, 0.35)):
        yy = y + altura * t
        inicio = x - sentido * t * 0.8
        fim = x + sentido * t * 0.45
        pygame.draw.line(tela, cor, (inicio, yy), (fim, yy), largura)
        pygame.draw.polygon(tela, cor, [(x + sentido * t * 0.95, yy), (fim, yy - t * 0.32), (fim, yy + t * 0.32)])


def icone_fuga(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    pygame.draw.rect(tela, escurecer(cor, 0.5), (x - t * 0.1, y - t * 0.9, t * 0.9, t * 1.8), max(2, int(t * 0.12)), border_radius=3)
    pygame.draw.line(tela, cor, (x + t * 0.35, y), (x - t * 0.85, y), max(3, int(t * 0.2)))
    pygame.draw.polygon(tela, cor, [(x - t * 1.0, y), (x - t * 0.5, y - t * 0.45), (x - t * 0.5, y + t * 0.45)])


def icone_flecha(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    pygame.draw.line(tela, (170, 130, 80), (x - t, y + t * 0.3), (x + t * 0.6, y - t * 0.1), 2)
    pygame.draw.polygon(tela, cor, [(x + t, y - t * 0.2), (x + t * 0.5, y - t * 0.35), (x + t * 0.55, y + t * 0.05)])


def icone_pergaminho(tela, centro, tamanho, cor):
    x, y = centro
    t = tamanho / 2
    pygame.draw.rect(tela, (230, 210, 160), (x - t * 0.6, y - t * 0.6, t * 1.2, t * 1.2))
    pygame.draw.circle(tela, (190, 160, 110), (int(x - t * 0.6), int(y)), int(t * 0.62), 0)
    pygame.draw.circle(tela, (190, 160, 110), (int(x + t * 0.6), int(y)), int(t * 0.62), 0)
    pygame.draw.rect(tela, (240, 222, 175), (x - t * 0.55, y - t * 0.55, t * 1.1, t * 1.1))
    for i in range(3):
        pygame.draw.line(tela, (120, 90, 60), (x - t * 0.35, y - t * 0.3 + i * t * 0.3), (x + t * 0.35, y - t * 0.3 + i * t * 0.3), 1)
    graficos.desenhar_brilho(tela, (x, y), int(t * 1.3), cor, 0.4)


def icone_item(tela, item, centro, tamanho):
    if item.nome == "Pergaminho arcano":
        icone_pergaminho(tela, centro, tamanho, tema.CRITICO)
    elif item.tipo == "mana":
        icone_pocao(tela, centro, tamanho, (200, 210, 230), (60, 120, 255))
    elif item.tipo == "flecha":
        icone_flecha(tela, centro, tamanho * 1.2, (230, 230, 240))
    elif "Elixir" in item.nome:
        icone_pocao(tela, centro, tamanho, (200, 210, 230), (240, 170, 40))
    elif item.nome == "Bandagem":
        x, y = centro
        t = tamanho / 2
        pygame.draw.rect(tela, (236, 230, 214), (x - t * 0.8, y - t * 0.35, t * 1.6, t * 0.7), border_radius=4)
        pygame.draw.rect(tela, (200, 40, 50), (x - t * 0.12, y - t * 0.3, t * 0.24, t * 0.6))
        pygame.draw.rect(tela, (200, 40, 50), (x - t * 0.3, y - t * 0.12, t * 0.6, t * 0.24))
    else:
        icone_pocao(tela, centro, tamanho, (200, 210, 230))


def descricao_item(item):
    if item.nome == "Pergaminho arcano":
        return "Próximo golpe causa 1.5x de dano", tema.CRITICO
    if item.tipo == "mana":
        return f"Recupera {item.valor} de mana", tema.MANA
    if item.tipo == "flecha":
        return f"Concede {item.valor} flechas extras", (220, 190, 140)
    return f"Recupera {item.valor} de vida", tema.CURA


# ---------- botão ----------

_fundos_botao = {}

class Botao:

    def __init__(self, rect, rotulo, tecla="", icone=None, cor=tema.OURO, detalhe="", acao=None, ativo=True):
        self.rect = pygame.Rect(rect)
        self.rotulo = rotulo
        self.tecla = tecla
        self.icone = icone
        self.cor = cor
        self.detalhe = detalhe
        self.cor_detalhe = tema.TEXTO_FRACO
        self.acao = acao
        self.ativo = ativo
        self.foco = 0.0
        self.selecionado = False
        self.pressionado = 0.0

    def _fundo(self, tamanho, cor, foco):
        chave = (tamanho, cor, foco)
        if chave not in _fundos_botao:
            topo = graficos.misturar((30, 26, 38), escurecer(cor, 0.35), foco)
            base = graficos.misturar((14, 12, 20), escurecer(cor, 0.15), foco)
            superficie = graficos.gradiente_vertical(tamanho, [topo, base]).convert_alpha()
            mascara = pygame.Surface(tamanho, pygame.SRCALPHA)
            pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=10)
            superficie.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            if len(_fundos_botao) > 300:
                _fundos_botao.clear()
            _fundos_botao[chave] = superficie
        return _fundos_botao[chave]

    def sob_mouse(self, posicao):
        return self.ativo and self.rect.collidepoint(posicao)

    def atualizar(self, dt, focado):
        alvo = 1.0 if focado and self.ativo else 0.0
        self.foco += (alvo - self.foco) * min(1.0, dt * 14)
        self.pressionado = max(0.0, self.pressionado - dt * 4)

    def desenhar(self, tela, t=0.0):
        foco = self.foco
        rect = self.rect.move(0, -int(4 * foco) + int(3 * self.pressionado))
        cor = self.cor if self.ativo else (90, 84, 76)
        if foco > 0.05:
            graficos.desenhar_brilho(tela, rect.center, int(min(rect.w * 0.75, rect.h * 1.8)), escurecer(cor, 0.5), foco * 0.8)
        tela.blit(self._fundo(rect.size, cor, round(foco * 8) / 8), rect)
        borda = graficos.misturar(escurecer(cor, 0.55), clarear(cor, 0.3), foco)
        pygame.draw.rect(tela, borda, rect, 2, border_radius=10)
        if foco > 0.05:
            brilho_linha = int(rect.w * 0.6 * foco)
            pygame.draw.line(tela, clarear(cor, 0.6), (rect.centerx - brilho_linha // 2, rect.top + 1), (rect.centerx + brilho_linha // 2, rect.top + 1), 2)

        alfa = 255 if self.ativo else 110
        if self.icone and rect.h >= 80:
            self.icone(tela, (rect.centerx, rect.top + rect.h * 0.38), min(rect.w, rect.h) * 0.36, cor if self.ativo else (110, 104, 96))
            rotulo = graficos.texto(self.rotulo, 19, graficos.misturar(tema.TEXTO, clarear(cor, 0.5), foco), titulo=True, negrito=True)
            tela.blit(graficos.com_alfa(rotulo, alfa), rotulo.get_rect(center=(rect.centerx, rect.bottom - 30)))
            if self.detalhe:
                detalhe = graficos.texto(self.detalhe, 13, self.cor_detalhe)
                tela.blit(graficos.com_alfa(detalhe, alfa), detalhe.get_rect(center=(rect.centerx, rect.bottom - 12)))
        else:
            deslocamento = 0
            if self.icone:
                self.icone(tela, (rect.left + 30, rect.centery), rect.h * 0.55, cor if self.ativo else (110, 104, 96))
                deslocamento = 48
            compacto = rect.h < 58
            rotulo = graficos.texto(self.rotulo, 18 if compacto else 20, graficos.misturar(tema.TEXTO, clarear(cor, 0.5), foco), titulo=True, negrito=True)
            y_rotulo = rect.centery - (9 if self.detalhe and not compacto else 0)
            tela.blit(graficos.com_alfa(rotulo, alfa), rotulo.get_rect(midleft=(rect.left + 18 + deslocamento, y_rotulo)))
            if self.detalhe:
                detalhe = graficos.texto(self.detalhe, 14, self.cor_detalhe)
                if compacto:
                    posicao = detalhe.get_rect(midright=(rect.right - (44 if self.tecla else 16), rect.centery))
                else:
                    posicao = detalhe.get_rect(midleft=(rect.left + 18 + deslocamento, rect.centery + 13))
                tela.blit(graficos.com_alfa(detalhe, alfa), posicao)

        if self.tecla:
            tecla = graficos.texto(self.tecla, 14, tema.TEXTO, negrito=True)
            caixa = pygame.Rect(0, 0, max(22, tecla.get_width() + 10), 22)
            caixa.topright = (rect.right - 7, rect.top + 7)
            if rect.h < 58:
                caixa.centery = rect.centery
            pygame.draw.rect(tela, (8, 6, 12), caixa, border_radius=5)
            pygame.draw.rect(tela, escurecer(cor, 0.7) if self.ativo else (70, 66, 60), caixa, 1, border_radius=5)
            tela.blit(graficos.com_alfa(tecla, alfa), tecla.get_rect(center=caixa.center))


class GrupoBotoes:
    """Controla foco por teclado e mouse em uma lista de botões."""

    def __init__(self, botoes, sons=None, horizontal=True):
        self.botoes = botoes
        self.indice = next((i for i, b in enumerate(botoes) if b.ativo), 0)
        self.sons = sons
        self.horizontal = horizontal
        self.usando_mouse = False

    def _mover(self, passo):
        if not self.botoes:
            return
        for _ in range(len(self.botoes)):
            self.indice = (self.indice + passo) % len(self.botoes)
            if self.botoes[self.indice].ativo:
                break
        if self.sons:
            self.sons.tocar("passar")

    def tratar_evento(self, evento):
        """Devolve o botão acionado, se houver."""
        if evento.type == pygame.MOUSEMOTION:
            for i, botao in enumerate(self.botoes):
                if botao.sob_mouse(evento.pos):
                    if i != self.indice and self.sons:
                        self.sons.tocar("passar")
                    self.indice = i
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i, botao in enumerate(self.botoes):
                if botao.sob_mouse(evento.pos):
                    self.indice = i
                    return self._acionar(botao)
        elif evento.type == pygame.KEYDOWN:
            anterior = pygame.K_LEFT if self.horizontal else pygame.K_UP
            proximo = pygame.K_RIGHT if self.horizontal else pygame.K_DOWN
            if evento.key in (anterior, pygame.K_a if self.horizontal else pygame.K_w):
                self._mover(-1)
            elif evento.key in (proximo, pygame.K_d if self.horizontal else pygame.K_s):
                self._mover(1)
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if self.botoes and self.botoes[self.indice].ativo:
                    return self._acionar(self.botoes[self.indice])
            else:
                for botao in self.botoes:
                    if botao.ativo and botao.tecla and evento.unicode and evento.unicode.upper() == botao.tecla.upper():
                        self.indice = self.botoes.index(botao)
                        return self._acionar(botao)
        return None

    def _acionar(self, botao):
        botao.pressionado = 1.0
        if self.sons:
            self.sons.tocar("clique")
        return botao

    def atualizar(self, dt):
        for i, botao in enumerate(self.botoes):
            botao.atualizar(dt, i == self.indice)

    def desenhar(self, tela, t=0.0):
        for botao in self.botoes:
            botao.desenhar(tela, t)


# ---------- barras ----------

def barra(tela, rect, valor, fantasma, maximo, cor, cor_escura, brilho_extra=0.0, segmentos=10):
    rect = pygame.Rect(rect)
    pygame.draw.rect(tela, (6, 4, 8), rect.inflate(6, 6), border_radius=6)
    pygame.draw.rect(tela, cor_escura, rect, border_radius=4)
    maximo = max(1, maximo)
    if fantasma > valor:
        largura = int(rect.w * min(1.0, fantasma / maximo))
        pygame.draw.rect(tela, tema.FANTASMA, (rect.x, rect.y, largura, rect.h), border_radius=4)
    largura = int(rect.w * max(0.0, min(1.0, valor / maximo)))
    if largura > 0:
        preenchido = graficos.gradiente_vertical((largura, rect.h), [clarear(cor, 0.45), cor, escurecer(cor, 0.6)])
        tela.blit(preenchido, rect.topleft)
        pygame.draw.line(tela, clarear(cor, 0.7), (rect.x + 2, rect.y + 2), (rect.x + largura - 3, rect.y + 2), 1)
        if brilho_extra > 0:
            graficos.desenhar_brilho(tela, (rect.x + largura, rect.centery), rect.h * 2, cor, brilho_extra)
    for i in range(1, segmentos):
        x = rect.x + rect.w * i // segmentos
        pygame.draw.line(tela, (0, 0, 0), (x, rect.y + rect.h * 0.55), (x, rect.bottom - 1), 1)
    pygame.draw.rect(tela, tema.OURO_ESCURO, rect.inflate(4, 4), 1, border_radius=5)


_medalhoes = {}


def medalhao(tela, chave, centro, diametro, cor, espelhar=False):
    from . import figuras

    x, y = int(centro[0]), int(centro[1])
    diametro = max(8, int(diametro))
    identificador = (chave, espelhar, diametro, tuple(cor))
    if identificador not in _medalhoes:
        fundo = graficos.gradiente_vertical((diametro, diametro), [escurecer(cor, 0.5), (10, 8, 16)])
        fundo.blit(figuras.retrato(chave, espelhar, diametro), (0, 0))
        _medalhoes[identificador] = graficos.mascara_circular(fundo, diametro)
    graficos.desenhar_brilho(tela, (x, y), int(diametro * 0.9), escurecer(cor, 0.5), 0.6)
    pygame.draw.circle(tela, (8, 6, 12), (x, y), diametro // 2 + 6)
    tela.blit(_medalhoes[identificador], (x - diametro // 2, y - diametro // 2))
    pygame.draw.circle(tela, tema.OURO, (x, y), diametro // 2 + 3, max(2, diametro // 30))
    pygame.draw.circle(tela, tema.OURO_ESCURO, (x, y), diametro // 2 + 7, 2)
