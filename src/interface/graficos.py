import math

import pygame

from . import tema

_fontes = {}
_brilhos = {}
_paineis = {}


def fonte(tamanho, titulo=False, negrito=False):
    chave = (tamanho, titulo, negrito)
    if chave not in _fontes:
        nomes = tema.FONTES_TITULO if titulo else tema.FONTES_TEXTO
        _fontes[chave] = pygame.font.SysFont(nomes, tamanho, bold=negrito)
    return _fontes[chave]


def misturar(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(len(a)))


def escurecer(cor, fator=0.6):
    return tuple(int(c * fator) for c in cor[:3])


def clarear(cor, fator=0.4):
    return tuple(int(c + (255 - c) * fator) for c in cor[:3])


def suavizar(t):
    return t * t * (3 - 2 * t)


def sair_cubico(t):
    return 1 - (1 - t) ** 3


def sair_volta(t, forca=1.70158):
    t -= 1
    return t * t * ((forca + 1) * t + forca) + 1


def gradiente_vertical(tamanho, cores, alfa=False):
    """Cria um degradê vertical passando por todas as ``cores`` em ordem."""
    largura, altura = tamanho
    coluna = pygame.Surface((1, altura), pygame.SRCALPHA if alfa else 0)
    trechos = len(cores) - 1
    for y in range(altura):
        posicao = y / max(1, altura - 1) * trechos
        indice = min(int(posicao), trechos - 1)
        coluna.set_at((0, y), misturar(cores[indice], cores[indice + 1], posicao - indice))
    return pygame.transform.scale(coluna, (largura, altura))


def gradiente_horizontal(tamanho, cores, alfa=False):
    largura, altura = tamanho
    girado = gradiente_vertical((altura, largura), cores, alfa)
    return pygame.transform.rotate(girado, 90)


def brilho(raio, cor):
    """Halo radial para ser desenhado com ``pygame.BLEND_RGB_ADD``."""
    raio = max(2, int(raio))
    cor = tuple(int(c) for c in cor[:3])
    chave = (raio, cor)
    if chave not in _brilhos:
        superficie = pygame.Surface((raio * 2, raio * 2))
        passos = min(raio, 48)
        for i in range(passos, 0, -1):
            t = i / passos
            intensidade = (1 - t) ** 2.2
            pygame.draw.circle(
                superficie,
                tuple(int(c * intensidade) for c in cor),
                (raio, raio),
                max(1, int(raio * t)),
            )
        if len(_brilhos) > 600:
            _brilhos.clear()
        _brilhos[chave] = superficie
    return _brilhos[chave]


def desenhar_brilho(tela, centro, raio, cor, intensidade=1.0):
    if intensidade <= 0.02:
        return
    nivel = max(1, min(8, round(intensidade * 8))) / 8
    halo = brilho(raio, tuple(c * nivel for c in cor[:3]))
    tela.blit(halo, (centro[0] - raio, centro[1] - raio), special_flags=pygame.BLEND_RGB_ADD)


def desfocar(superficie, fator=4):
    largura, altura = superficie.get_size()
    pequeno = pygame.transform.smoothscale(superficie, (max(1, largura // fator), max(1, altura // fator)))
    return pygame.transform.smoothscale(pequeno, (largura, altura))


def vinheta(tamanho, forca=200, cor=(0, 0, 0)):
    pequeno = pygame.Surface((64, 36), pygame.SRCALPHA)
    for y in range(36):
        for x in range(64):
            dx = (x - 31.5) / 32
            dy = (y - 17.5) / 18
            distancia = min(1.0, math.hypot(dx, dy) / 1.25)
            alfa = int(forca * distancia ** 2.4)
            pequeno.set_at((x, y), (*cor, alfa))
    return pygame.transform.smoothscale(pequeno, tamanho)


_textos = {}


def _memorizar(funcao):
    """Guarda superfícies de texto já renderizadas (o resultado não deve ser alterado)."""

    def envolvida(*argumentos, **nomeados):
        chave = (funcao.__name__, argumentos, tuple(sorted(nomeados.items())))
        if chave not in _textos:
            if len(_textos) > 900:
                _textos.clear()
            _textos[chave] = funcao(*argumentos, **nomeados)
        return _textos[chave]

    return envolvida


@_memorizar
def texto(conteudo, tamanho, cor=tema.TEXTO, titulo=False, negrito=False):
    return fonte(tamanho, titulo, negrito).render(conteudo, True, cor)


@_memorizar
def texto_contorno(conteudo, tamanho, cor=tema.TEXTO, contorno=(0, 0, 0), espessura=2, titulo=False, negrito=False):
    letra = fonte(tamanho, titulo, negrito)
    base = letra.render(conteudo, True, cor)
    borda = letra.render(conteudo, True, contorno)
    largura, altura = base.get_size()
    superficie = pygame.Surface((largura + espessura * 2, altura + espessura * 2), pygame.SRCALPHA)
    for dx in range(-espessura, espessura + 1):
        for dy in range(-espessura, espessura + 1):
            if dx * dx + dy * dy <= espessura * espessura + 1:
                superficie.blit(borda, (espessura + dx, espessura + dy))
    superficie.blit(base, (espessura, espessura))
    return superficie


def texto_dourado(conteudo, tamanho, cores=None, titulo=True, contorno=2, espacamento=0):
    """Texto com degradê metálico e contorno escuro."""
    cores = tuple(tuple(c) for c in cores) if cores else None
    return _texto_dourado(conteudo, tamanho, cores, titulo, contorno, espacamento)


@_memorizar
def _texto_dourado(conteudo, tamanho, cores, titulo, contorno, espacamento):
    cores = cores or [tema.OURO_CLARO, tema.OURO, tema.OURO_ESCURO]
    letra = fonte(tamanho, titulo, True)
    if espacamento:
        conteudo = (" " * espacamento).join(conteudo)
    branco = letra.render(conteudo, True, (255, 255, 255))
    degrade = gradiente_vertical(branco.get_size(), cores)
    colorido = branco.copy()
    colorido.blit(degrade, (0, 0), special_flags=pygame.BLEND_RGB_MULT)

    sombra = letra.render(conteudo, True, (10, 6, 2))
    largura, altura = branco.get_size()
    superficie = pygame.Surface((largura + contorno * 2, altura + contorno * 2 + 3), pygame.SRCALPHA)
    for dx in range(-contorno, contorno + 1):
        for dy in range(-contorno, contorno + 4):
            superficie.blit(sombra, (contorno + dx, contorno + dy))
    superficie.blit(colorido, (contorno, contorno))
    return superficie


def centralizar(tela, superficie, centro):
    rect = superficie.get_rect(center=(int(centro[0]), int(centro[1])))
    tela.blit(superficie, rect)
    return rect


def com_alfa(superficie, alfa):
    if alfa >= 255:
        return superficie
    copia = superficie.copy()
    copia.set_alpha(max(0, int(alfa)))
    return copia


def painel(tela, rect, alfa=210, cor=tema.PAINEL, borda=tema.OURO_ESCURO, destaque=None, raio=12):
    """Painel translúcido com moldura dupla e ornamentos nos cantos."""
    rect = pygame.Rect(rect)
    cor_borda = tuple(destaque or borda)
    chave = ("painel", rect.size, int(alfa), tuple(cor), cor_borda, raio)
    camada = _paineis.get(chave)
    if camada is None:
        camada = pygame.Surface(rect.size, pygame.SRCALPHA)
        fundo = gradiente_vertical(rect.size, [(*clarear(cor, 0.06), alfa), (*cor, alfa)], alfa=True)
        mascara = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=raio)
        fundo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        camada.blit(fundo, (0, 0))
        pygame.draw.rect(camada, (*cor_borda, 255), camada.get_rect(), 2, border_radius=raio)
        pygame.draw.rect(camada, (*clarear(cor_borda, 0.3), 70), camada.get_rect().inflate(-8, -8), 1, border_radius=max(2, raio - 4))
        if len(_paineis) > 200:
            _paineis.clear()
        _paineis[chave] = camada
    tela.blit(camada, rect)

    for canto in (rect.topleft, rect.topright, rect.bottomleft, rect.bottomright):
        x, y = canto
        x += 4 if canto[0] == rect.left else -5
        y += 4 if canto[1] == rect.top else -5
        losango = [(x, y - 6), (x + 6, y), (x, y + 6), (x - 6, y)]
        pygame.draw.polygon(tela, clarear(cor_borda, 0.35), losango)
        pygame.draw.polygon(tela, escurecer(cor_borda, 0.5), losango, 1)


def divisor(tela, centro, largura, cor=tema.OURO):
    x, y = centro
    meio = largura // 2
    pygame.draw.line(tela, escurecer(cor, 0.7), (x - meio, y), (x - 10, y), 1)
    pygame.draw.line(tela, escurecer(cor, 0.7), (x + 10, y), (x + meio, y), 1)
    pygame.draw.polygon(tela, cor, [(x, y - 5), (x + 5, y), (x, y + 5), (x - 5, y)])


def mascara_circular(superficie, diametro):
    imagem = pygame.transform.smoothscale(superficie, (diametro, diametro)).convert_alpha()
    mascara = pygame.Surface((diametro, diametro), pygame.SRCALPHA)
    pygame.draw.circle(mascara, (255, 255, 255, 255), (diametro // 2, diametro // 2), diametro // 2)
    imagem.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    return imagem


class Pincel:
    """Desenha em resolução dobrada para depois reduzir com suavização."""

    def __init__(self, largura, altura, escala=2):
        self.largura = largura
        self.altura = altura
        self.s = escala
        self.surf = pygame.Surface((largura * escala, altura * escala), pygame.SRCALPHA)

    def _p(self, ponto):
        return (round(ponto[0] * self.s), round(ponto[1] * self.s))

    def poligono(self, cor, pontos, largura=0):
        pygame.draw.polygon(self.surf, cor, [self._p(p) for p in pontos], round(largura * self.s))

    def circulo(self, cor, centro, raio, largura=0):
        pygame.draw.circle(self.surf, cor, self._p(centro), max(1, round(raio * self.s)), round(largura * self.s))

    def elipse(self, cor, rect, largura=0):
        x, y, w, h = rect
        pygame.draw.ellipse(self.surf, cor, (x * self.s, y * self.s, w * self.s, h * self.s), round(largura * self.s))

    def retangulo(self, cor, rect, raio=0):
        x, y, w, h = rect
        pygame.draw.rect(self.surf, cor, (x * self.s, y * self.s, w * self.s, h * self.s), border_radius=round(raio * self.s))

    def linha(self, cor, a, b, largura=2):
        largura_real = max(1, round(largura * self.s))
        pa, pb = self._p(a), self._p(b)
        pygame.draw.line(self.surf, cor, pa, pb, largura_real)
        if largura_real > 3:
            pygame.draw.circle(self.surf, cor, pa, largura_real // 2)
            pygame.draw.circle(self.surf, cor, pb, largura_real // 2)

    def arco(self, cor, rect, inicio, fim, largura=2):
        x, y, w, h = rect
        pygame.draw.arc(self.surf, cor, (x * self.s, y * self.s, w * self.s, h * self.s), inicio, fim, round(largura * self.s))

    def brilho(self, cor, centro, raio, alfa=90):
        raio_real = max(1, round(raio * self.s))
        camada = pygame.Surface((raio_real * 2, raio_real * 2), pygame.SRCALPHA)
        passos = 12
        for i in range(passos, 0, -1):
            t = i / passos
            camada_alfa = int(alfa * (1 - t) ** 1.5)
            if camada_alfa > 0:
                pygame.draw.circle(camada, (*cor[:3], camada_alfa), (raio_real, raio_real), max(1, round(raio_real * t)))
        x, y = self._p(centro)
        self.surf.blit(camada, (x - raio_real, y - raio_real))

    def final(self, tamanho=None):
        tamanho = tamanho or (self.largura, self.altura)
        return pygame.transform.smoothscale(self.surf, tamanho)
