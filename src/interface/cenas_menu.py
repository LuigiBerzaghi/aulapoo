import math
import random

import pygame

from . import cenarios, figuras, graficos, tema, widgets
from .controlador import criar_heroi, criar_inimigo, inimigos_disponiveis
from .efeitos import Particula, Particulas
from .graficos import clarear, escurecer

L, A = tema.LARGURA, tema.ALTURA
MAXIMOS = {"vida": 200, "ataque": 35, "defesa": 12}

_paisagem = None


class Cena:

    def __init__(self, app):
        self.app = app
        self.t = 0.0

    @property
    def sons(self):
        return self.app.sons

    def tratar_evento(self, evento):
        pass

    def atualizar(self, dt):
        self.t += dt

    def desenhar(self, tela):
        pass


def paisagem():
    """Céu noturno com o Castelo da Noite ao longe, usado nos menus."""
    global _paisagem
    if _paisagem is None:
        s = pygame.Surface((L, A))
        s.blit(graficos.gradiente_vertical((L, 520), [(3, 3, 12), (16, 10, 36), (56, 22, 52), (120, 52, 42)]), (0, 0))
        rng = random.Random(42)
        for _ in range(260):
            x, y = rng.randrange(L), rng.randrange(380)
            brilho = rng.randint(80, 230)
            s.set_at((x, y), (brilho, brilho, min(255, brilho + 25)))
        graficos.desenhar_brilho(s, (900, 170), 380, (90, 60, 70), 0.9)
        pygame.draw.circle(s, (242, 232, 214), (900, 170), 70)
        pygame.draw.circle(s, (220, 210, 196), (880, 150), 14)
        pygame.draw.circle(s, (224, 214, 198), (925, 195), 10)
        cenarios._montanhas(s, (40, 22, 44), 480, 170, 101, 70)
        cenarios._montanhas(s, (24, 12, 28), 520, 120, 102, 55)
        pygame.draw.polygon(s, (12, 6, 16), [(700, A), (760, 470), (860, 440), (1000, 436), (1120, 470), (1200, A)])
        cenarios._castelo(s, (10, 5, 14), 940, 446, 0.75, (120, 170, 255), semente=12)
        s.blit(graficos.gradiente_vertical((L, A - 560), [(14, 8, 16), (4, 2, 6)]), (0, 560))
        pygame.draw.polygon(s, (6, 3, 8), [(0, A), (0, 560), (200, 590), (420, 610), (640, 640), (900, 620), (1280, 580), (1280, A)])
        for x, altura in ((40, 420), (120, 330), (190, 260), (1240, 380)):
            cenarios._pinheiro(s, (3, 2, 5), x, A + 30, altura)
        _paisagem = s
    return _paisagem


class FundoMenu:
    """Paisagem animada com brasas subindo e névoa, compartilhada entre os menus."""

    def __init__(self, escurecer_fundo=0):
        self.particulas = Particulas(400)
        self.vinheta = graficos.vinheta((L, A), 230)
        self.escuro = None
        if escurecer_fundo:
            self.escuro = pygame.Surface((L, A), pygame.SRCALPHA)
            self.escuro.fill((4, 2, 8, escurecer_fundo))
        self.t = 0.0
        self.acumulado = 0.0
        for _ in range(60):
            self._emitir(random.uniform(0, A))

    def _emitir(self, y=None):
        r = random.random
        cor = random.choice([(255, 150, 60), (255, 110, 40), (255, 210, 120)])
        self.particulas.adicionar(Particula(r() * L, A + 10 if y is None else y, (r() - 0.4) * 30, -30 - r() * 60, 5 + r() * 5, cor, 1 + r() * 2, encolhe=False, oscila=30))

    def atualizar(self, dt):
        self.t += dt
        self.acumulado += dt * 14
        while self.acumulado >= 1:
            self.acumulado -= 1
            self._emitir()
        self.particulas.atualizar(dt)

    def desenhar(self, tela):
        tela.blit(paisagem(), (0, 0))
        graficos.desenhar_brilho(tela, (900, 170), 160, (60, 50, 40), 0.35 + 0.1 * math.sin(self.t * 0.8))
        self.particulas.desenhar(tela)
        if self.escuro:
            tela.blit(self.escuro, (0, 0))
        tela.blit(self.vinheta, (0, 0))


_veus = {}


def escurecer_carta(tela, rect, raio, intensidade):
    """Escurece cartas sem foco (sem deixá-las transparentes)."""
    nivel = round(max(0.0, min(1.0, intensidade)) * 10)
    if nivel == 0:
        return
    chave = (rect.size, raio, nivel)
    if chave not in _veus:
        veu = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(veu, (4, 2, 8, int(120 * nivel / 10)), veu.get_rect(), border_radius=raio)
        _veus[chave] = veu
    tela.blit(_veus[chave], rect)


def rodape(tela, texto):
    imagem = graficos.texto(texto, 15, tema.TEXTO_FRACO)
    graficos.centralizar(tela, imagem, (L // 2, A - 24))


def titulo_secao(tela, texto, y=62):
    imagem = graficos.texto_dourado(texto, 46, espacamento=1)
    graficos.centralizar(tela, imagem, (L // 2, y))
    graficos.divisor(tela, (L // 2, y + 36), 420)


# ---------------------------------------------------------------- abertura

class CenaAbertura(Cena):

    HISTORIA = [
        "O Reino de Eldoria vive dias sombrios.",
        "Criaturas da noite atacam os vilarejos e o Mestre da Noite espera em seu castelo.",
        "Um herói precisa se levantar. Será você?",
    ]

    def __init__(self, app):
        super().__init__(app)
        self.fundo = FundoMenu()
        self.titulo = graficos.texto_dourado("ELDORIA", 150, contorno=3, espacamento=1)
        self.brilho_titulo = self._halo(self.titulo)
        self.subtitulo = graficos.texto("AS  SOMBRAS  DO  MESTRE  DA  NOITE", 22, (220, 200, 170), titulo=True)
        self.sobretitulo = graficos.texto("J O G O   D E   B A T A L H A   R P G", 16, tema.OURO, titulo=True)
        self.historia = [graficos.texto(linha, 19, (214, 206, 190)) for linha in self.HISTORIA]
        self.botoes = widgets.GrupoBotoes([
            widgets.Botao((L // 2 - 160, 520, 320, 54), "Iniciar Jornada", "Enter"),
            widgets.Botao((L // 2 - 160, 586, 320, 54), "Sair", "Esc", cor=(180, 160, 150)),
        ], self.sons, horizontal=False)

    @staticmethod
    def _halo(imagem):
        base = pygame.Surface((imagem.get_width() + 120, imagem.get_height() + 120))
        base.fill((0, 0, 0))
        base.blit(imagem, (60, 60))
        base.fill((255, 150, 60), special_flags=pygame.BLEND_RGB_MULT)
        return graficos.desfocar(graficos.desfocar(base, 8), 4)

    def tratar_evento(self, evento):
        if self.t < 1.2:
            if evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.t = 1.2
            return
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            self.app.encerrar()
            return
        botao = self.botoes.tratar_evento(evento)
        if botao is self.botoes.botoes[0]:
            self.app.ir_para(CenaEscolhaHeroi(self.app))
        elif botao is self.botoes.botoes[1]:
            self.app.encerrar()

    def atualizar(self, dt):
        super().atualizar(dt)
        self.fundo.atualizar(dt)
        self.botoes.atualizar(dt)

    def desenhar(self, tela):
        self.fundo.desenhar(tela)
        entrada = graficos.sair_cubico(min(1.0, self.t / 1.4))

        y_titulo = 190 + (1 - entrada) * 30
        pulso = 0.75 + 0.25 * math.sin(self.t * 1.6)
        halo = self.brilho_titulo.copy()
        halo.set_alpha(int(255 * entrada * pulso))
        tela.blit(halo, halo.get_rect(center=(L // 2, y_titulo)), special_flags=pygame.BLEND_RGB_ADD)
        graficos.centralizar(tela, graficos.com_alfa(self.titulo, 255 * entrada), (L // 2, y_titulo))
        graficos.centralizar(tela, graficos.com_alfa(self.sobretitulo, 255 * entrada), (L // 2, y_titulo - 100))
        graficos.centralizar(tela, graficos.com_alfa(self.subtitulo, 255 * entrada), (L // 2, y_titulo + 92))
        if entrada > 0.5:
            graficos.divisor(tela, (L // 2, int(y_titulo + 124)), int(520 * entrada))

        for i, linha in enumerate(self.historia):
            alfa = max(0.0, min(1.0, (self.t - 1.0 - i * 0.6) / 0.8))
            if alfa > 0:
                graficos.centralizar(tela, graficos.com_alfa(linha, 255 * alfa), (L // 2, 360 + i * 32 + (1 - alfa) * 8))

        if self.t > 1.2:
            alfa = min(1.0, (self.t - 1.2) / 0.6)
            camada = pygame.Surface((L, A), pygame.SRCALPHA)
            self.botoes.desenhar(camada, self.t)
            camada.set_alpha(int(255 * alfa))
            tela.blit(camada, (0, 0))
            rodape(tela, "Setas / mouse para navegar   •   Enter para confirmar   •   M liga/desliga o som   •   F11 tela cheia")


# ---------------------------------------------------------------- herói

def _barra_atributo(tela, x, y, largura, rotulo, valor, maximo, cor):
    tela.blit(graficos.texto(rotulo, 13, tema.TEXTO_FRACO, negrito=True), (x, y))
    numero = graficos.texto(str(valor), 15, tema.TEXTO, negrito=True)
    tela.blit(numero, numero.get_rect(topright=(x + largura, y - 1)))
    caixa = pygame.Rect(x, y + 19, largura, 7)
    pygame.draw.rect(tela, (10, 8, 14), caixa.inflate(4, 4), border_radius=4)
    preenchido = int(largura * min(1.0, valor / maximo))
    if preenchido:
        tela.blit(graficos.gradiente_horizontal((preenchido, 7), [escurecer(cor, 0.6), clarear(cor, 0.3)]), caixa.topleft)


class CenaEscolhaHeroi(Cena):

    LARGURA_CARTA = 340
    ALTURA_CARTA = 486

    def __init__(self, app):
        super().__init__(app)
        self.fundo = FundoMenu(150)
        self.chaves = list(tema.HEROIS)
        self.herois = {chave: criar_heroi(chave) for chave in self.chaves}
        self.indice = 0
        self.foco = [0.0] * len(self.chaves)
        self.escolhido = None
        self.cartas = [self._carta(chave) for chave in self.chaves]

    def _rect(self, i):
        x = L // 2 + (i - 1) * (self.LARGURA_CARTA + 40) - self.LARGURA_CARTA // 2
        return pygame.Rect(x, 132, self.LARGURA_CARTA, self.ALTURA_CARTA)

    def _carta(self, chave):
        info = tema.HEROIS[chave]
        heroi = self.herois[chave]
        largura, altura = self.LARGURA_CARTA, self.ALTURA_CARTA
        carta = pygame.Surface((largura, altura), pygame.SRCALPHA)
        fundo = graficos.gradiente_vertical((largura, altura), [escurecer(info["cor"], 0.32), (18, 14, 24), (10, 8, 14)])
        mascara = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 240), mascara.get_rect(), border_radius=16)
        fundo = fundo.convert_alpha()
        fundo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        carta.blit(fundo, (0, 0))

        nome = graficos.texto_dourado(heroi.nome.upper(), 36, espacamento=1)
        graficos.centralizar(carta, nome, (largura // 2, 316))
        classe = graficos.texto(f"{info['classe']}  •  {info['titulo']}", 16, clarear(info["cor"], 0.3), titulo=True)
        graficos.centralizar(carta, classe, (largura // 2, 352))
        graficos.divisor(carta, (largura // 2, 372), 240, info["cor"])

        x = 40
        _barra_atributo(carta, x, 384, largura - 80, "VIDA", heroi.vida, MAXIMOS["vida"], tema.VIDA)
        _barra_atributo(carta, x, 414, largura - 80, "ATAQUE", heroi.ataque, MAXIMOS["ataque"], (255, 170, 70))
        _barra_atributo(carta, x, 444, largura - 80, "DEFESA", heroi.defesa, MAXIMOS["defesa"], (120, 170, 255))
        return carta

    def tratar_evento(self, evento):
        if self.escolhido is not None:
            return
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self._focar(self.indice - 1)
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self._focar(self.indice + 1)
            elif evento.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                self._focar(evento.key - pygame.K_1)
                self._confirmar()
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self._confirmar()
            elif evento.key == pygame.K_ESCAPE:
                self.app.ir_para(CenaAbertura(self.app))
        elif evento.type == pygame.MOUSEMOTION:
            for i in range(len(self.chaves)):
                if self._rect(i).collidepoint(evento.pos) and i != self.indice:
                    self._focar(i)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(self.chaves)):
                if self._rect(i).collidepoint(evento.pos):
                    self._focar(i)
                    self._confirmar()

    def _focar(self, indice):
        indice %= len(self.chaves)
        if indice != self.indice:
            self.indice = indice
            self.sons.tocar("passar")

    def _confirmar(self):
        self.escolhido = self.chaves[self.indice]
        self.sons.tocar("troca")
        self.app.ir_para(CenaEscolhaVilao(self.app, self.escolhido), duracao=0.45)

    def atualizar(self, dt):
        super().atualizar(dt)
        self.fundo.atualizar(dt)
        for i in range(len(self.foco)):
            alvo = 1.0 if i == self.indice else 0.0
            self.foco[i] += (alvo - self.foco[i]) * min(1.0, dt * 10)

    def desenhar(self, tela):
        self.fundo.desenhar(tela)
        titulo_secao(tela, "ESCOLHA SEU HERÓI")
        for i, chave in enumerate(self.chaves):
            info = tema.HEROIS[chave]
            foco = self.foco[i]
            entrada = graficos.sair_volta(max(0.0, min(1.0, (self.t - i * 0.08) / 0.5)))
            rect = self._rect(i).move(0, int(-16 * foco + (1 - entrada) * 120))
            if foco > 0.05:
                graficos.desenhar_brilho(tela, rect.center, 330, escurecer(info["cor"], 0.45), foco)
            tela.blit(self.cartas[i], rect)

            graficos.desenhar_brilho(tela, (rect.centerx, rect.top + 170), 150, escurecer(info["cor"], 0.5), 0.45 + 0.4 * foco)
            imagem = figuras.sprite(chave, 270)
            balanco = math.sin(self.t * 2.4 + i) * 4 * foco
            sombra = pygame.Rect(0, 0, 150, 26)
            sombra.center = (rect.centerx, rect.top + 286)
            pygame.draw.ellipse(tela, (6, 4, 8), sombra)
            tela.blit(imagem, imagem.get_rect(midbottom=(rect.centerx, rect.top + 290 + balanco)))
            escurecer_carta(tela, rect, 16, 1 - foco)

            cor_borda = graficos.misturar(tema.OURO_ESCURO, clarear(info["cor"], 0.2), foco)
            pygame.draw.rect(tela, cor_borda, rect, 2 + int(foco * 1.5), border_radius=16)
            if foco > 0.5:
                descricao_y = rect.bottom + 18
                for j, linha in enumerate(info["descricao"]):
                    texto = graficos.texto(linha, 16, graficos.misturar(tema.TEXTO_FRACO, tema.TEXTO, foco))
                    graficos.centralizar(tela, graficos.com_alfa(texto, 255 * (foco - 0.5) * 2), (rect.centerx, descricao_y + j * 22))
            tecla = graficos.texto(str(i + 1), 15, tema.TEXTO, negrito=True)
            caixa = pygame.Rect(rect.right - 36, rect.top + 12, 24, 24)
            pygame.draw.rect(tela, (8, 6, 12), caixa, border_radius=5)
            pygame.draw.rect(tela, cor_borda, caixa, 1, border_radius=5)
            tela.blit(tecla, tecla.get_rect(center=caixa.center))
        rodape(tela, "← → escolher   •   Enter ou clique para confirmar   •   Esc voltar")


# ---------------------------------------------------------------- vilão

class CenaEscolhaVilao(Cena):

    LARGURA_CARTA = 226
    ALTURA_CARTA = 452

    def __init__(self, app, chave_heroi):
        super().__init__(app)
        self.fundo = FundoMenu(150)
        self.chave_heroi = chave_heroi
        self.heroi = criar_heroi(chave_heroi)
        self.classes = inimigos_disponiveis(self.heroi)
        self.viloes = [criar_inimigo(classe) for classe in self.classes]
        self.indice = 0
        self.foco = [0.0] * len(self.classes)
        self.escolhido = False
        self.cartas = [self._carta(vilao) for vilao in self.viloes]

    def _rect(self, i):
        quantidade = len(self.classes)
        espaco = 16
        total = quantidade * self.LARGURA_CARTA + (quantidade - 1) * espaco
        x = (L - total) // 2 + i * (self.LARGURA_CARTA + espaco)
        return pygame.Rect(x, 150, self.LARGURA_CARTA, self.ALTURA_CARTA)

    def _carta(self, vilao):
        nome_classe = type(vilao).__name__
        info = tema.VILOES[nome_classe]
        largura, altura = self.LARGURA_CARTA, self.ALTURA_CARTA
        carta = pygame.Surface((largura, altura), pygame.SRCALPHA)
        fundo = cenarios.miniatura(info["cenario"], (largura, altura)).convert_alpha()
        sombra = graficos.gradiente_vertical((largura, altura), [(0, 0, 0, 40), (0, 0, 0, 60), (6, 4, 10, 245), (6, 4, 10, 250)], alfa=True)
        fundo.blit(sombra, (0, 0))
        mascara = pygame.Surface((largura, altura), pygame.SRCALPHA)
        pygame.draw.rect(mascara, (255, 255, 255, 255), mascara.get_rect(), border_radius=14)
        fundo.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        carta.blit(fundo, (0, 0))

        nome = graficos.texto_dourado(vilao.nome.upper(), 24)
        if nome.get_width() > largura - 20:
            proporcao = (largura - 20) / nome.get_width()
            nome = pygame.transform.smoothscale(nome, (largura - 20, int(nome.get_height() * proporcao)))
        graficos.centralizar(carta, nome, (largura // 2, 300))
        subtitulo = graficos.texto(info["titulo"], 14, clarear(info["cor"], 0.3), titulo=True)
        graficos.centralizar(carta, subtitulo, (largura // 2, 328))
        graficos.divisor(carta, (largura // 2, 346), 160, info["cor"])
        _barra_atributo(carta, 22, 358, largura - 44, "VIDA", vilao.vida, MAXIMOS["vida"], tema.VIDA)
        _barra_atributo(carta, 22, 388, largura - 44, "ATAQUE", vilao.ataque, MAXIMOS["ataque"], (255, 170, 70))
        _barra_atributo(carta, 22, 418, largura - 44, "DEFESA", vilao.defesa, MAXIMOS["defesa"], (120, 170, 255))
        return carta

    def tratar_evento(self, evento):
        if self.escolhido:
            return
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_LEFT, pygame.K_a):
                self._focar(self.indice - 1)
            elif evento.key in (pygame.K_RIGHT, pygame.K_d):
                self._focar(self.indice + 1)
            elif pygame.K_1 <= evento.key <= pygame.K_9 and evento.key - pygame.K_1 < len(self.classes):
                self._focar(evento.key - pygame.K_1)
                self._confirmar()
            elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                self._confirmar()
            elif evento.key == pygame.K_ESCAPE:
                self.app.ir_para(CenaEscolhaHeroi(self.app))
        elif evento.type == pygame.MOUSEMOTION:
            for i in range(len(self.classes)):
                if self._rect(i).collidepoint(evento.pos) and i != self.indice:
                    self._focar(i)
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            for i in range(len(self.classes)):
                if self._rect(i).collidepoint(evento.pos):
                    self._focar(i)
                    self._confirmar()

    def _focar(self, indice):
        indice %= len(self.classes)
        if indice != self.indice:
            self.indice = indice
            self.sons.tocar("passar")

    def _confirmar(self):
        from .cena_batalha import CenaBatalha

        self.escolhido = True
        self.sons.tocar("furia")
        self.app.ir_para(CenaBatalha(self.app, self.chave_heroi, self.classes[self.indice]), duracao=0.6)

    def atualizar(self, dt):
        super().atualizar(dt)
        self.fundo.atualizar(dt)
        for i in range(len(self.foco)):
            alvo = 1.0 if i == self.indice else 0.0
            self.foco[i] += (alvo - self.foco[i]) * min(1.0, dt * 10)

    def desenhar(self, tela):
        self.fundo.desenhar(tela)
        titulo_secao(tela, "ESCOLHA SEU OPONENTE")
        info_heroi = tema.HEROIS[self.chave_heroi]
        titulo_heroi = info_heroi["titulo"][0].lower() + info_heroi["titulo"][1:]
        legenda = graficos.texto(f"{self.heroi.nome}, {titulo_heroi}, se prepara para o combate.", 17, (210, 200, 186))
        graficos.centralizar(tela, legenda, (L // 2, 122))

        for i, vilao in enumerate(self.viloes):
            info = tema.VILOES[type(vilao).__name__]
            foco = self.foco[i]
            entrada = graficos.sair_volta(max(0.0, min(1.0, (self.t - i * 0.06) / 0.5)))
            rect = self._rect(i).move(0, int(-14 * foco + (1 - entrada) * 140))
            if foco > 0.05:
                graficos.desenhar_brilho(tela, rect.center, 260, escurecer(info["cor"], 0.45), foco)
            tela.blit(self.cartas[i], rect)

            chave = type(vilao).__name__.lower()
            altura = 230 if chave != "chefefinal" else 262
            if chave == "goblin":
                altura = 210
            imagem = figuras.sprite(chave, altura, espelhar=True)
            balanco = math.sin(self.t * 2.2 + i) * 4 * foco
            graficos.desenhar_brilho(tela, (rect.centerx, rect.top + 160), 110, escurecer(info["cor"], 0.5), 0.3 + 0.5 * foco)
            sombra = pygame.Rect(0, 0, 120, 20)
            sombra.center = (rect.centerx, rect.top + 270)
            pygame.draw.ellipse(tela, (6, 4, 8), sombra)
            tela.blit(imagem, imagem.get_rect(midbottom=(rect.centerx, rect.top + 274 + balanco)))
            escurecer_carta(tela, rect, 14, 1 - foco)

            cor_borda = graficos.misturar(tema.OURO_ESCURO, clarear(info["cor"], 0.2), foco)
            if chave == "chefefinal":
                pulso = 0.6 + 0.4 * math.sin(self.t * 3)
                cor_borda = graficos.misturar(cor_borda, (140, 190, 255), pulso * 0.6)
                faixa = pygame.Rect(0, 0, 124, 26)
                faixa.midtop = (rect.centerx, rect.top - 13)
                pygame.draw.rect(tela, (12, 16, 34), faixa, border_radius=6)
                pygame.draw.rect(tela, (140, 190, 255), faixa, 2, border_radius=6)
                graficos.centralizar(tela, graficos.texto("CHEFE FINAL", 13, (200, 220, 255), titulo=True, negrito=True), faixa.center)
            pygame.draw.rect(tela, cor_borda, rect, 2 + int(foco * 1.5), border_radius=14)
            tecla = graficos.texto(str(i + 1), 14, tema.TEXTO, negrito=True)
            caixa = pygame.Rect(rect.right - 32, rect.top + 10, 22, 22)
            pygame.draw.rect(tela, (8, 6, 12), caixa, border_radius=5)
            pygame.draw.rect(tela, cor_borda, caixa, 1, border_radius=5)
            tela.blit(tecla, tecla.get_rect(center=caixa.center))

        vilao = self.viloes[self.indice]
        local = graficos.texto(vilao.local, 17, (200, 190, 176))
        graficos.centralizar(tela, local, (L // 2, 640))
        rodape(tela, "← → escolher   •   Enter ou clique para lutar   •   Esc voltar")
