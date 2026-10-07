import math
import random

import pygame

from . import cenarios, figuras, graficos, tema, widgets
from .cenas_menu import Cena, CenaAbertura, CenaEscolhaHeroi
from .controlador import HEROIS, ControladorBatalha, chave_personagem, criar_heroi, criar_inimigo
from .efeitos import Agenda, Clarao, Corte, Onda, Particula, Particulas, Projetil, Raios, TextoFlutuante, Tremor
from .graficos import clarear, escurecer, sair_cubico, suavizar

L, A = tema.LARGURA, tema.ALTURA

# Ponto de onde saem projéteis, nas coordenadas do quadro 240x300 das figuras.
PONTAS = {
    "mago": (192, 44),
    "magosombrio": (192, 52),
    "arqueiro": (222, 118),
    "arqueirosombrio": (222, 118),
}

RETANGULO_REGISTRO = pygame.Rect(24, 540, 600, 164)
RETANGULO_ACOES = pygame.Rect(640, 540, 616, 164)
Y_FAIXA = 205


class Combatente:

    def __init__(self, personagem, x, lado):
        self.x0 = x
        self.y0 = tema.CHAO_Y
        self.lado = lado
        self.definir(personagem)

    def definir(self, personagem):
        self.personagem = personagem
        self.chave = chave_personagem(personagem)
        self.escala = tema.ESCALA_FIGURA.get(self.chave, 1.0)
        self.sprite = figuras.sprite(self.chave, espelhar=self.lado < 0)
        self.sprite_virado = pygame.transform.flip(self.sprite, True, False)
        self.branco = figuras.silhueta(self.sprite)
        if self.chave in tema.HEROIS:
            self.cor = tema.HEROIS[self.chave]["cor"]
        else:
            self.cor = tema.VILOES[type(personagem).__name__]["cor"]
        self.vida_alvo = personagem.vida
        self.vida_mostrada = float(personagem.vida)
        self.fantasma = float(personagem.vida)
        self.espera_fantasma = 0.0
        self.mana_mostrada = float(getattr(personagem, "mana", 0))
        self.dx = 0.0
        self.dy = 0.0
        self.movimento = None
        self.flash = 0.0
        self.fase = random.uniform(0, 6)
        self.virado = False
        self.morrendo = None
        self.alfa = 255

    @property
    def altura(self):
        return self.sprite.get_height()

    @property
    def x(self):
        return self.x0 + self.dx

    @property
    def y(self):
        return self.y0 + self.dy

    def centro(self):
        return (self.x, self.y - self.altura * 0.48)

    def ponta(self):
        fx, fy = PONTAS.get(self.chave, (200, 130))
        return (self.x + (fx - 120) * self.escala * self.lado, self.y - (300 - fy) * self.escala)

    def mover(self, duracao, funcao):
        self.movimento = [0.0, duracao, funcao]

    def investir(self, distancia=190, duracao=0.6):
        lado = self.lado

        def funcao(p):
            if p < 0.28:
                q = sair_cubico(p / 0.28)
                return distancia * q * lado, -math.sin(q * math.pi) * 22
            if p < 0.45:
                return distancia * lado, 0
            return distancia * (1 - suavizar((p - 0.45) / 0.55)) * lado, 0

        self.mover(duracao, funcao)

    def recuar(self, forca=26, duracao=0.35):
        self.mover(duracao, lambda p: (-self.lado * forca * math.sin(math.pi * p) * (1 - p * 0.5), 0))

    def conjurar(self, duracao=0.7):
        self.mover(duracao, lambda p: (-self.lado * 10 * math.sin(math.pi * p), -18 * math.sin(math.pi * p)))

    def entrar(self, duracao=0.8):
        self.virado = False
        self.dx = -self.lado * 700
        self.mover(duracao, lambda p: (-self.lado * 700 * (1 - sair_cubico(p)), 0))

    def sair(self, duracao=0.4):
        self.mover(duracao, lambda p: (-self.lado * 700 * suavizar(p), 0))

    def fugir(self, duracao=1.1):
        self.virado = True
        self.mover(duracao, lambda p: (-self.lado * 900 * p ** 1.6, -abs(math.sin(p * 22)) * 12))

    def atingir(self):
        self.flash = 0.2
        self.recuar()

    def morrer(self):
        self.morrendo = 0.0

    def definir_vida(self, valor):
        if valor < self.vida_alvo:
            self.espera_fantasma = 0.45
        self.vida_alvo = valor

    def atualizar(self, dt):
        self.fase += dt
        self.flash = max(0.0, self.flash - dt)
        if self.movimento:
            self.movimento[0] += dt
            p = min(1.0, self.movimento[0] / self.movimento[1])
            self.dx, self.dy = self.movimento[2](p)
            if p >= 1.0:
                self.movimento = None

        self.vida_mostrada += (self.vida_alvo - self.vida_mostrada) * min(1.0, dt * 12)
        if self.fantasma > self.vida_mostrada:
            if self.espera_fantasma > 0:
                self.espera_fantasma -= dt
            else:
                self.fantasma = max(self.vida_mostrada, self.fantasma - max(25 * dt, (self.fantasma - self.vida_mostrada) * dt * 3))
        else:
            self.fantasma = self.vida_mostrada
        mana = getattr(self.personagem, "mana", 0)
        self.mana_mostrada += (mana - self.mana_mostrada) * min(1.0, dt * 8)

        if self.morrendo is not None:
            self.morrendo += dt
            self.alfa = int(255 * max(0.0, 1 - self.morrendo / 1.3))

    def desenhar(self, tela, deslocamento, aura=None):
        if self.alfa <= 0:
            return
        flutua = self.chave == "magosombrio"
        parado = self.movimento is None and self.morrendo is None
        balanco = math.sin(self.fase * 2.2) * (7 if flutua else 3) if parado else 0
        x = self.x + deslocamento[0]
        y = self.y + deslocamento[1] + balanco - (14 if flutua else 0)

        sombra_largura = int(self.sprite.get_width() * 0.5 * (1 - max(0, -self.dy) / 160))
        sombra = pygame.Surface((max(10, sombra_largura), 26), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, int(140 * self.alfa / 255)), sombra.get_rect())
        tela.blit(sombra, sombra.get_rect(center=(self.x + deslocamento[0], self.y0 + deslocamento[1] - 2)))

        if aura:
            cor, intensidade = aura
            graficos.desenhar_brilho(tela, (x, y - self.altura * 0.5), int(self.altura * 0.62), cor, intensidade)

        imagem = self.sprite_virado if self.virado else self.sprite
        rect = imagem.get_rect(midbottom=(int(x), int(y)))
        if self.morrendo is not None:
            p = min(1.0, self.morrendo / 1.3)
            imagem = pygame.transform.rotozoom(imagem, self.lado * 10 * p, 1.0)
            rect = imagem.get_rect(midbottom=(int(x), int(y + 30 * p)))
            imagem = graficos.com_alfa(imagem, self.alfa)
        tela.blit(imagem, rect)
        if self.flash > 0 and self.morrendo is None:
            tela.blit(graficos.com_alfa(self.branco, 255 * min(1.0, self.flash / 0.12)), rect)


class Registro:
    """Crônica da batalha, com efeito de máquina de escrever."""

    def __init__(self, largura):
        self.largura = largura
        self.linhas = []

    def adicionar(self, texto, cor=tema.TEXTO):
        fonte = graficos.fonte(16)
        palavras = texto.split()
        atual = ""
        for palavra in palavras:
            teste = f"{atual} {palavra}".strip()
            if fonte.size(teste)[0] > self.largura and atual:
                self.linhas.append([atual, cor, 0.0])
                atual = palavra
            else:
                atual = teste
        if atual:
            self.linhas.append([atual, cor, 0.0])
        self.linhas = self.linhas[-30:]

    def atualizar(self, dt):
        for linha in self.linhas[-5:]:
            linha[2] += dt

    def desenhar(self, tela, rect):
        visiveis = self.linhas[-5:]
        y = rect.bottom - 16 - len(visiveis) * 21
        for i, (texto, cor, t) in enumerate(visiveis):
            caracteres = int(t * 140)
            if caracteres <= 0:
                continue
            idade = len(visiveis) - 1 - i
            alfa = 255 if idade == 0 else max(80, 235 - idade * 34)
            imagem = graficos.texto(texto[:caracteres], 16, cor)
            tela.blit(graficos.com_alfa(imagem, alfa), (rect.x + 20, y + i * 21))


class Faixa:
    """Faixa dramática atravessando a tela (nome de golpe especial)."""

    def __init__(self, texto, cor, duracao=1.6):
        self.imagem = graficos.texto_dourado(texto, 64, [clarear(cor, 0.7), cor, escurecer(cor, 0.4)], espacamento=1)
        self.cor = cor
        self.duracao = duracao
        self.t = 0.0

    @property
    def viva(self):
        return self.t < self.duracao

    def desenhar(self, tela):
        p = self.t / self.duracao
        entrada = sair_cubico(min(1.0, p / 0.15))
        saida = 1 - suavizar(max(0.0, (p - 0.8) / 0.2))
        altura = int(110 * entrada * saida)
        if altura <= 2:
            return
        faixa = pygame.Surface((L, altura), pygame.SRCALPHA)
        faixa.fill((4, 4, 10, 210))
        tela.blit(faixa, (0, Y_FAIXA - altura // 2))
        pygame.draw.line(tela, self.cor, (0, Y_FAIXA - altura // 2), (L, Y_FAIXA - altura // 2), 2)
        pygame.draw.line(tela, self.cor, (0, Y_FAIXA + altura // 2), (L, Y_FAIXA + altura // 2), 2)
        x = L // 2 + (1 - entrada) * 500 - p * 60
        graficos.centralizar(tela, graficos.com_alfa(self.imagem, 255 * saida), (x, Y_FAIXA))


class CenaBatalha(Cena):

    def __init__(self, app, chave_heroi, classe_inimigo):
        super().__init__(app)
        self.classe_inimigo = classe_inimigo
        self.ctrl = ControladorBatalha(criar_heroi(chave_heroi), criar_inimigo(classe_inimigo))
        info = tema.VILOES[classe_inimigo.__name__]
        self.info_vilao = info
        self.cenario = cenarios.Cenario(info["cenario"])
        self.heroi = Combatente(self.ctrl.jogador, tema.HEROI_X, 1)
        self.vilao = Combatente(self.ctrl.inimigo, tema.VILAO_X, -1)
        if self.vilao.chave == "chefefinal":
            self.vilao.y0 += 12
        self.heroi.entrar(1.0)
        self.vilao.entrar(1.0)

        self.ambiente = Particulas(350)
        self.particulas = Particulas(900)
        self.efeitos = []
        self.projeteis = []
        self.textos = []
        self.tremor = Tremor()
        self.clarao = Clarao()
        self.agenda = Agenda()
        self.registro = Registro(RETANGULO_REGISTRO.w - 44)
        self.faixa = None
        self.escuridao = 0.0
        self.congelar = 0.0
        self.carregando = None
        self.pop_rodada = 0.0

        self.estado = "intro"
        self.vez = "jogador"
        self.submenu = None
        self.grupo = None
        self.fim = None
        self.t_fim = 0.0
        self.raios = None
        self.vinheta_dano = graficos.vinheta((L, A), 255, (150, 0, 10))
        self.alerta_vida = 0.0
        self.letreiro = 1.0

        self.fala = self.ctrl.inimigo.fala
        self.registro.adicionar(self.ctrl.inimigo.local, (170, 160, 150))
        self.sons.tocar("fuga")

    # ------------------------------------------------------------ menus

    def _abrir_menu(self, submenu=None):
        self.estado = "escolha"
        self.submenu = submenu
        jogador = self.ctrl.jogador
        area = RETANGULO_ACOES.inflate(-24, -24)
        botoes = []
        if submenu is None:
            ataque = int(jogador.ataque * getattr(jogador, "dano_bonus_rodada", 1.0))
            detalhe = f"{ataque} de dano"
            if hasattr(jogador, "flechas"):
                detalhe = f"{jogador.flechas} flechas"
            opcoes = [("Atacar", widgets.icone_espada, self.acao_atacar, detalhe, tema.OURO, True)]
            if self.ctrl.pode_usar_magia:
                cor_custo = tema.MANA if jogador.mana >= 20 else tema.DANO
                opcoes.append(("Magia", widgets.icone_magia, self.acao_magia, "custa 20 de mana", cor_custo, True))
            quantidade = len(jogador.inventario)
            opcoes.append(("Itens", widgets.icone_pocao, lambda: self._abrir_menu("itens"), f"{quantidade} na bolsa" if quantidade else "bolsa vazia", tema.CURA, quantidade > 0))
            opcoes.append(("Trocar", widgets.icone_troca, lambda: self._abrir_menu("troca"), "não gasta a vez", (190, 170, 255), True))
            opcoes.append(("Fugir", widgets.icone_fuga, self.acao_fugir, "abandona a luta", (190, 180, 170), True))
            largura = (area.w - (len(opcoes) - 1) * 10) / len(opcoes)
            for i, (rotulo, icone, acao, detalhe, cor, ativo) in enumerate(opcoes):
                rect = (area.x + i * (largura + 10), area.y, largura, area.h)
                botao = widgets.Botao(rect, rotulo, str(i + 1), icone, cor if rotulo != "Magia" else tema.MANA, detalhe, acao, ativo)
                if rotulo == "Magia":
                    botao.cor_detalhe = cor
                botoes.append(botao)
            self.grupo = widgets.GrupoBotoes(botoes, self.sons, horizontal=True)
        elif submenu == "itens":
            altura = (area.h - 2 * 6) / 3
            for i, item in enumerate(jogador.inventario[:3]):
                descricao, cor = widgets.descricao_item(item)
                rect = (area.x, area.y + i * (altura + 6), area.w, altura)
                botao = widgets.Botao(rect, item.nome, str(i + 1), lambda tela, c, t, cor_icone, item=item: widgets.icone_item(tela, item, c, t), cor, descricao, lambda i=i: self.acao_item(i))
                botao.cor_detalhe = cor
                botoes.append(botao)
            self.grupo = widgets.GrupoBotoes(botoes, self.sons, horizontal=False)
        elif submenu == "troca":
            altura = (area.h - 2 * 6) / 3
            for i, chave in enumerate(HEROIS):
                classe, nome = HEROIS[chave]
                info = tema.HEROIS[chave]
                modelo = classe(nome)
                em_campo = isinstance(jogador, classe)
                detalhe = f"Vida {modelo.vida}  •  Ataque {modelo.ataque}  •  Defesa {modelo.defesa}"
                if em_campo:
                    detalhe += "   (em campo)"
                rect = (area.x, area.y + i * (altura + 6), area.w, altura)
                icone = lambda tela, c, t, cor, chave=chave: widgets.medalhao(tela, chave, c, int(t * 1.2), tema.HEROIS[chave]["cor"])
                botoes.append(widgets.Botao(rect, f"{nome}, {info['classe'].lower()}", str(i + 1), icone, info["cor"], detalhe, lambda chave=chave: self.acao_troca(chave)))
            self.grupo = widgets.GrupoBotoes(botoes, self.sons, horizontal=False)

    def _abrir_pausa(self):
        self.estado = "pausa"
        centro = L // 2
        botoes = [
            widgets.Botao((centro - 170, 300, 340, 56), "Continuar", "Esc"),
            widgets.Botao((centro - 170, 368, 340, 56), "Abandonar batalha", "", cor=(200, 150, 130)),
            widgets.Botao((centro - 170, 436, 340, 56), "Sair do jogo", "", cor=(170, 160, 150)),
        ]
        self.grupo_pausa = widgets.GrupoBotoes(botoes, self.sons, horizontal=False)

    def tratar_evento(self, evento):
        if self.estado == "intro":
            if self.t > 1.0 and evento.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                self.sons.tocar("clique")
                self.pop_rodada = 0.0
                self._abrir_menu()
            return

        if self.estado == "pausa":
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self._abrir_menu()
                return
            botao = self.grupo_pausa.tratar_evento(evento)
            if botao is self.grupo_pausa.botoes[0]:
                self._abrir_menu()
            elif botao is self.grupo_pausa.botoes[1]:
                self.app.ir_para(CenaAbertura(self.app))
            elif botao is self.grupo_pausa.botoes[2]:
                self.app.encerrar()
            return

        if self.estado == "fim":
            if self.t_fim < 1.0:
                return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.grupo.botoes[-1].acao()
                return
            botao = self.grupo.tratar_evento(evento)
            if botao and botao.acao:
                botao.acao()
            return

        if self.estado != "escolha":
            return

        if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
            if self.submenu:
                self.sons.tocar("clique")
                self._abrir_menu()
            elif evento.key == pygame.K_ESCAPE:
                self._abrir_pausa()
            return
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3 and self.submenu:
            self._abrir_menu()
            return
        botao = self.grupo.tratar_evento(evento)
        if botao and botao.acao:
            botao.acao()

    # ------------------------------------------------------------ utilidades

    def _registrar(self, mensagens):
        heroi = self.ctrl.jogador.nome
        vilao = self.ctrl.inimigo.nome
        for mensagem in mensagens:
            cor = tema.TEXTO
            if "crítico" in mensagem:
                cor = tema.CRITICO
            elif "recupera" in mensagem or "recebe" in mensagem or "ativou" in mensagem:
                cor = tema.CURA
            elif "bloqueia" in mensagem:
                cor = tema.BLOQUEIO
            elif mensagem.startswith(f"{heroi} sofre"):
                cor = tema.DANO
            elif mensagem.startswith(f"{vilao} sofre"):
                cor = tema.OURO_CLARO
            elif "falha" in mensagem or "não há" in mensagem or "não tem" in mensagem:
                cor = (160, 160, 170)
            elif mensagem.startswith(vilao):
                cor = (255, 180, 170)
            self.registro.adicionar(mensagem, cor)

    @staticmethod
    def _separar(resultado):
        antes, depois = [], []
        for mensagem in resultado.mensagens:
            if " sofre " in mensagem or "bloqueia o golpe" in mensagem:
                depois.append(mensagem)
            else:
                antes.append(mensagem)
        return antes, depois

    def _texto_sobre(self, combatente, texto, cor, tamanho=40, atraso=0.0):
        x = combatente.centro()[0]
        y = combatente.y - combatente.altura + 40
        self.textos.append(TextoFlutuante(texto, x, y, cor, tamanho, atraso=atraso))

    def _iniciar_acao(self):
        self.vez = "jogador"
        self.estado = "animando"
        self.grupo = None
        self.submenu = None

    # ------------------------------------------------------------ impacto

    def _impacto(self, alvo, resultado, estilo, cor, mensagens):
        self._registrar(mensagens)
        alvo.definir_vida(alvo.personagem.vida)
        cx, cy = alvo.centro()
        atacante = self.heroi if alvo is self.vilao else self.vilao
        if resultado.dano > 0:
            alvo.atingir()
            forca = min(24, 5 + resultado.dano * 0.35) + (10 if resultado.critico or resultado.especial else 0)
            self.tremor.agitar(forca)
            self.congelar = 0.06 + (0.12 if resultado.critico or resultado.especial else 0)
            if resultado.critico:
                self.textos.append(TextoFlutuante(f"-{resultado.dano}", cx, cy - 30, tema.CRITICO, 72, 1.5))
                self.textos.append(TextoFlutuante("CRÍTICO!", cx, cy - 120, (255, 240, 200), 40, 1.5, atraso=0.05))
                self.clarao.disparar((255, 240, 200), 170, 0.45)
                self.sons.tocar("critico")
            else:
                self.textos.append(TextoFlutuante(f"-{resultado.dano}", cx, cy - 30, tema.DANO if alvo is self.heroi else (255, 236, 200), 54))
            faiscas = graficos.clarear(cor, 0.4)
            if estilo == "corte":
                self.efeitos.append(Corte(cx - 90 * atacante.lado, cy - 10, atacante.lado, cor, raio=105))
                self.particulas.explosao(cx, cy, 34, faiscas, velocidade=(160, 520), angulo=(-60, 60) if atacante.lado > 0 else (120, 240), vida=(0.25, 0.6), tamanho=(2, 4), gravidade=900, arrasto=1.0)
                self.sons.tocar("golpe")
            elif estilo == "flecha":
                self.particulas.explosao(cx, cy, 22, faiscas, velocidade=(120, 380), vida=(0.2, 0.5), tamanho=(1.5, 3.5), gravidade=700)
                self.sons.tocar("golpe", 0.8)
            else:
                self.particulas.explosao(cx, cy, 70, cor, velocidade=(80, 460), vida=(0.4, 1.0), tamanho=(3, 7), arrasto=2.5)
                self.particulas.explosao(cx, cy, 30, (255, 230, 170), velocidade=(40, 200), vida=(0.3, 0.6), tamanho=(2, 4))
                self.efeitos.append(Onda(cx, cy, cor, 200, 0.5, 14))
                self.clarao.disparar(clarear(cor, 0.5), 50, 0.3)
                self.sons.tocar("explosao")
            self.efeitos.append(Onda(alvo.x, alvo.y0 - 4, cor, 170, 0.5, 6))
            self.particulas.explosao(alvo.x, alvo.y0 - 4, 14, (120, 110, 100, 160), velocidade=(40, 160), angulo=(10, 170), vida=(0.4, 0.8), tamanho=(4, 9), gravidade=200, brilha=False)
        else:
            self.textos.append(TextoFlutuante("BLOQUEADO!", cx, cy - 40, tema.BLOQUEIO, 40))
            self.efeitos.append(Onda(cx, cy, tema.BLOQUEIO, 110, 0.35, 8))
            self.particulas.explosao(cx - 30 * atacante.lado * -1, cy, 20, tema.BLOQUEIO, velocidade=(120, 300), vida=(0.2, 0.4), tamanho=(1.5, 3))
            self.tremor.agitar(5)
            self.sons.tocar("bloqueio")

    def _disparar(self, origem_comb, alvo, duracao, cor, estilo, tamanho=16, arco=0.0):
        origem = origem_comb.ponta()
        destino = alvo.centro()
        self.projeteis.append(Projetil(origem, destino, duracao, cor, estilo, tamanho, arco))

    # ------------------------------------------------------------ ações do jogador

    def acao_atacar(self):
        self._iniciar_acao()
        resultado = self.ctrl.atacar()
        antes, depois = self._separar(resultado)
        self._registrar(antes)
        heroi, vilao = self.heroi, self.vilao

        if not resultado.sucesso:
            self._texto_sobre(heroi, "SEM FLECHAS!", (200, 200, 210), 38)
            self.sons.tocar("falha")
            self.agenda.depois(1.0, self._depois_do_jogador)
            return

        if heroi.chave == "guerreiro":
            heroi.investir()
            self.sons.tocar("corte")
            self.agenda.depois(0.17, lambda: self._impacto(vilao, resultado, "corte", heroi.cor, depois))
            self.agenda.depois(1.0, self._depois_do_jogador)
        elif heroi.chave == "arqueiro":
            heroi.recuar(10, 0.25)
            self.sons.tocar("flecha")
            self._disparar(heroi, vilao, 0.26, (255, 236, 170), "flecha")
            self.agenda.depois(0.26, lambda: self._impacto(vilao, resultado, "flecha", (255, 236, 170), depois))
            self.agenda.depois(1.0, self._depois_do_jogador)
        else:
            heroi.conjurar(0.4)
            bonus = resultado.dano > heroi.personagem.ataque
            cor = tema.CRITICO if bonus else heroi.cor
            self.sons.tocar("flecha")
            self._disparar(heroi, vilao, 0.34, cor, "orbe", 13, 30)
            self.agenda.depois(0.34, lambda: self._impacto(vilao, resultado, "orbe", cor, depois))
            self.agenda.depois(1.05, self._depois_do_jogador)

    def acao_magia(self):
        self._iniciar_acao()
        resultado = self.ctrl.usar_magia()
        antes, depois = self._separar(resultado)
        heroi, vilao = self.heroi, self.vilao
        heroi.conjurar(0.9)
        self.carregando = 0.55
        self.sons.tocar("carregar")

        if not resultado.sucesso:
            sem_mana = resultado.mana == 0

            def falhar():
                self._registrar(antes)
                x, y = heroi.ponta()
                self.particulas.explosao(x, y, 30, (110, 110, 120, 180), velocidade=(30, 120), vida=(0.5, 1.0), tamanho=(4, 10), gravidade=-60, brilha=False)
                self.particulas.explosao(x, y, 14, (160, 160, 200), velocidade=(60, 200), vida=(0.2, 0.4), tamanho=(1.5, 3))
                self._texto_sobre(heroi, "SEM MANA!" if sem_mana else "A MAGIA FALHOU!", (180, 180, 200), 38)
                self.sons.tocar("falha")

            self.agenda.depois(0.55, falhar)
            self.agenda.depois(1.4, self._depois_do_jogador)
            return

        cor = (255, 150, 60) if not resultado.critico else (255, 220, 120)

        def lancar():
            self._registrar(antes)
            self.sons.tocar("flecha")
            self._disparar(heroi, vilao, 0.38, cor, "orbe", 26, 50)

        self.agenda.depois(0.55, lancar)
        self.agenda.depois(0.93, lambda: self._impacto(vilao, resultado, "magia", cor, depois))
        self.agenda.depois(1.8, self._depois_do_jogador)

    def acao_item(self, indice):
        self._iniciar_acao()
        resultado = self.ctrl.usar_item(indice)
        self._registrar(resultado.mensagens)
        heroi = self.heroi
        heroi.definir_vida(heroi.personagem.vida)
        item = resultado.item
        if item.nome == "Pergaminho arcano" and resultado.cura == 0:
            cor, texto = tema.CRITICO, "PODER 1.5x"
        elif resultado.mana:
            cor, texto = tema.MANA, f"+{resultado.mana} MANA"
        elif resultado.flechas:
            cor, texto = (230, 200, 150), f"+{resultado.flechas} FLECHAS"
        else:
            cor, texto = tema.CURA, f"+{resultado.cura}"
        x = heroi.x
        for i in range(36):
            self.particulas.adicionar(Particula(x + random.uniform(-60, 60), heroi.y0 - random.uniform(0, 30), random.uniform(-10, 10), -random.uniform(80, 220), random.uniform(0.6, 1.2), cor, random.uniform(2, 4), arrasto=0.5, oscila=30))
        self.efeitos.append(Onda(x, heroi.y0 - 4, cor, 150, 0.6, 8))
        self._texto_sobre(heroi, texto, cor, 46)
        self.sons.tocar("cura")
        self.agenda.depois(1.0, self._depois_do_jogador)

    def acao_troca(self, chave):
        self._iniciar_acao()
        resultado = self.ctrl.trocar_personagem(chave)
        self._registrar(resultado.mensagens)
        heroi = self.heroi
        x, y = heroi.centro()
        self.particulas.explosao(x, y, 40, (90, 80, 100, 170), velocidade=(30, 160), vida=(0.5, 1.0), tamanho=(6, 14), brilha=False, espalhar=40)
        heroi.sair(0.35)
        self.sons.tocar("fuga")

        def entrar():
            heroi.definir(self.ctrl.jogador)
            heroi.entrar(0.6)
            self.sons.tocar("troca")
            self.clarao.disparar(heroi.cor, 70, 0.4)

        def pousar():
            x, y = heroi.x, heroi.y0
            self.efeitos.append(Onda(x, y - 4, heroi.cor, 180, 0.6, 10))
            self.particulas.explosao(x, y - 6, 26, heroi.cor, velocidade=(80, 260), angulo=(10, 170), vida=(0.3, 0.7), tamanho=(2, 4), gravidade=400)

        self.agenda.depois(0.4, entrar)
        self.agenda.depois(0.95, pousar)
        self.agenda.depois(1.2, self._abrir_menu)

    def acao_fugir(self):
        self._iniciar_acao()
        heroi = self.heroi
        self.registro.adicionar(f"{heroi.personagem.nome} tenta escapar da batalha e some entre as sombras!", (190, 190, 200))
        heroi.fugir()
        self.sons.tocar("fuga")
        for atraso in (0.0, 0.2, 0.4, 0.6):
            self.agenda.depois(atraso, lambda: self.particulas.explosao(heroi.x, heroi.y0 - 6, 10, (110, 100, 90, 170), velocidade=(30, 120), angulo=(20, 160), vida=(0.4, 0.8), tamanho=(5, 10), brilha=False))
        self.agenda.depois(1.2, lambda: self._encerrar("fuga"))

    # ------------------------------------------------------------ fluxo

    def _depois_do_jogador(self):
        estado = self.ctrl.estado()
        if estado == "vitoria":
            self._vitoria()
        elif estado in ("derrota", "empate"):
            self._derrota(estado)
        else:
            self.agenda.depois(0.1, self._turno_inimigo)

    def _turno_inimigo(self):
        self.vez = "inimigo"
        resultado = self.ctrl.turno_inimigo()
        antes, depois = self._separar(resultado)
        vilao = self.vilao
        atraso = 0.0
        if resultado.furia:
            self._registrar([m for m in antes if "fúria" in m])
            antes = [m for m in antes if "fúria" not in m]
            self._texto_sobre(vilao, "FÚRIA!", (255, 90, 60), 50)
            vilao.flash = 0.3
            self.tremor.agitar(10)
            self.clarao.disparar((140, 0, 0), 90, 0.5)
            self.particulas.explosao(*vilao.centro(), 40, (255, 70, 40), velocidade=(100, 300), vida=(0.4, 0.8), tamanho=(2, 5), espalhar=40)
            self.sons.tocar("furia")
            atraso = 0.6
        self.agenda.depois(atraso, lambda: self._ataque_inimigo(resultado, antes, depois))

    def _ataque_inimigo(self, resultado, antes, depois):
        vilao, heroi = self.vilao, self.heroi
        self._registrar(antes)
        cor = vilao.cor
        if resultado.especial:
            self.faixa = Faixa("GOLPE DO CREPÚSCULO", (130, 180, 255))
            self.escuridao = 1.0
            self.sons.tocar("carregar")
            for i in range(10):
                self.agenda.depois(i * 0.05, lambda: self.particulas.explosao(*vilao.centro(), 12, (130, 180, 255), velocidade=(200, 400), vida=(0.25, 0.4), tamanho=(2, 4), espalhar=120))
            self.agenda.depois(0.7, lambda: (vilao.investir(260, 0.7), self.sons.tocar("corte")))
            self.agenda.depois(0.9, lambda: (self._impacto(heroi, resultado, "magia", (130, 180, 255), depois), self.sons.tocar("especial")))
            self.agenda.depois(2.0, self._fim_da_rodada)
        elif vilao.chave == "magosombrio":
            vilao.conjurar(0.6)
            self.sons.tocar("carregar")
            self.agenda.depois(0.35, lambda: self._disparar(vilao, heroi, 0.36, cor, "orbe", 20, 40))
            self.agenda.depois(0.71, lambda: self._impacto(heroi, resultado, "magia", cor, depois))
            self.agenda.depois(1.5, self._fim_da_rodada)
        elif vilao.chave == "arqueirosombrio":
            vilao.recuar(10, 0.25)
            self.sons.tocar("flecha")
            self._disparar(vilao, heroi, 0.26, cor, "flecha")
            self.agenda.depois(0.26, lambda: self._impacto(heroi, resultado, "flecha", cor, depois))
            self.agenda.depois(1.1, self._fim_da_rodada)
        else:
            vilao.investir(210 if vilao.chave != "chefefinal" else 240)
            self.sons.tocar("corte")
            self.agenda.depois(0.17, lambda: self._impacto(heroi, resultado, "corte", cor, depois))
            self.agenda.depois(1.1, self._fim_da_rodada)

    def _fim_da_rodada(self):
        estado = self.ctrl.estado()
        if estado == "vitoria":
            self._vitoria()
        elif estado in ("derrota", "empate"):
            self._derrota(estado)
        else:
            self.ctrl.proxima_rodada()
            self.pop_rodada = 0.0
            self._abrir_menu()

    def _vitoria(self):
        self.estado = "animando"
        vilao = self.vilao
        self.registro.adicionar(f"{vilao.personagem.nome} cai no chão, derrotado!", tema.OURO_CLARO)
        self.congelar = 0.25
        self.clarao.disparar((255, 255, 255), 200, 0.6)
        self.tremor.agitar(16)
        self.agenda.depois(0.3, vilao.morrer)
        self.agenda.depois(1.5, lambda: self._encerrar("vitoria"))

    def _derrota(self, estado):
        self.estado = "animando"
        heroi = self.heroi
        self.registro.adicionar(f"{heroi.personagem.nome} sucumbe ao combate.", tema.DANO)
        self.congelar = 0.25
        self.clarao.disparar((120, 0, 0), 200, 0.8)
        self.agenda.depois(0.3, heroi.morrer)
        if estado == "empate":
            self.agenda.depois(0.3, self.vilao.morrer)
        self.agenda.depois(1.7, lambda: self._encerrar(estado))

    def _encerrar(self, tipo):
        self.estado = "fim"
        self.fim = tipo
        self.t_fim = 0.0
        if tipo == "vitoria":
            self.raios = Raios((L // 2, 250), tema.OURO)
            self.sons.tocar("vitoria")
        elif tipo in ("derrota", "empate"):
            self.sons.tocar("derrota")
        chave = chave_personagem(self.ctrl.jogador)
        botoes = [
            widgets.Botao((L // 2 - 370, 500, 230, 60), "Revanche", "R", acao=lambda: self.app.ir_para(CenaBatalha(self.app, chave, self.classe_inimigo))),
            widgets.Botao((L // 2 - 115, 500, 230, 60), "Nova jornada", "N", acao=lambda: self.app.ir_para(CenaEscolhaHeroi(self.app))),
            widgets.Botao((L // 2 + 140, 500, 230, 60), "Menu principal", "Esc", cor=(180, 170, 160), acao=lambda: self.app.ir_para(CenaAbertura(self.app))),
        ]
        self.grupo = widgets.GrupoBotoes(botoes, self.sons, horizontal=True)

    # ------------------------------------------------------------ atualização

    def atualizar(self, dt):
        super().atualizar(dt)
        mundo = dt
        if self.congelar > 0:
            self.congelar -= dt
            mundo = dt * 0.05

        self.agenda.atualizar(mundo)
        self.cenario.atualizar(mundo, self.ambiente)
        self.ambiente.atualizar(mundo)
        self.particulas.atualizar(mundo)
        self.heroi.atualizar(mundo)
        self.vilao.atualizar(mundo)
        for colecao in (self.efeitos, self.textos):
            for efeito in colecao:
                efeito.atualizar(mundo)
        for projetil in self.projeteis:
            projetil.atualizar(mundo, self.particulas)
        self.efeitos = [e for e in self.efeitos if e.vivo]
        self.textos = [t for t in self.textos if t.vivo]
        self.projeteis = [p for p in self.projeteis if p.vivo]
        self.tremor.atualizar(dt)
        self.clarao.atualizar(dt)
        self.registro.atualizar(dt)
        self.pop_rodada += dt
        self.escuridao = max(0.0, self.escuridao - dt * 0.6)
        if self.faixa:
            self.faixa.t += dt
            if not self.faixa.viva:
                self.faixa = None

        if self.carregando:
            self.carregando -= mundo
            x, y = self.heroi.ponta()
            for _ in range(3):
                angulo = random.uniform(0, math.tau)
                distancia = random.uniform(50, 110)
                self.particulas.adicionar(Particula(x + math.cos(angulo) * distancia, y + math.sin(angulo) * distancia, -math.cos(angulo) * distancia * 3.2, -math.sin(angulo) * distancia * 3.2, 0.3, self.heroi.cor, 2.5))
            if self.carregando <= 0:
                self.carregando = None

        for combatente in (self.heroi, self.vilao):
            if combatente.morrendo is not None and combatente.alfa > 0:
                rect = combatente.sprite.get_rect(midbottom=(combatente.x, combatente.y))
                for _ in range(4):
                    self.particulas.adicionar(Particula(random.uniform(rect.left + 30, rect.right - 30), random.uniform(rect.top + 20, rect.bottom), random.uniform(-20, 20), -random.uniform(40, 140), random.uniform(0.6, 1.2), combatente.cor, random.uniform(2, 4), oscila=20))

        jogador = self.ctrl.jogador
        self.alerta_vida = 0.0
        if jogador.esta_vivo() and jogador.vida <= jogador.vida_maxima * 0.3:
            self.alerta_vida = 0.35 + 0.25 * math.sin(self.t * 5)

        if self.estado == "intro":
            self.letreiro = 1.0
        else:
            self.letreiro = max(0.0, self.letreiro - dt * 2.5)

        if self.grupo:
            self.grupo.atualizar(dt)
        if self.estado == "pausa":
            self.grupo_pausa.atualizar(dt)
        if self.estado == "fim":
            self.t_fim += dt
            if self.raios:
                self.raios.atualizar(dt)

    # ------------------------------------------------------------ desenho

    def _aura(self, combatente):
        personagem = combatente.personagem
        if combatente.morrendo is not None:
            return None
        if combatente is self.heroi and getattr(personagem, "dano_bonus_rodada", 1.0) > 1.0:
            return (tema.CRITICO, 0.55 + 0.25 * math.sin(self.t * 6))
        if combatente is self.vilao:
            if personagem.vida <= personagem.vida_maxima * 0.3 and personagem.esta_vivo():
                return ((255, 50, 30), 0.5 + 0.3 * math.sin(self.t * 7))
            if combatente.chave == "chefefinal":
                return ((60, 110, 220), 0.45 + 0.1 * math.sin(self.t * 2))
        if combatente.chave == "mago":
            return ((60, 120, 200), 0.25)
        return None

    def desenhar(self, tela):
        deslocamento = self.tremor.deslocamento()
        self.cenario.desenhar_fundo(tela, deslocamento)
        self.ambiente.desenhar(tela, deslocamento)
        self.cenario.desenhar_nevoa(tela)

        if self.escuridao > 0:
            sombra = pygame.Surface((L, A), pygame.SRCALPHA)
            sombra.fill((0, 0, 8, int(170 * min(1.0, self.escuridao * 1.5))))
            tela.blit(sombra, (0, 0))

        self.vilao.desenhar(tela, deslocamento, self._aura(self.vilao))
        self.heroi.desenhar(tela, deslocamento, self._aura(self.heroi))

        for efeito in self.efeitos:
            efeito.desenhar(tela, deslocamento)
        for projetil in self.projeteis:
            projetil.desenhar(tela, deslocamento)
        self.particulas.desenhar(tela, deslocamento)
        for texto in self.textos:
            texto.desenhar(tela, deslocamento)

        self.cenario.desenhar_vinheta(tela)
        if self.alerta_vida > 0:
            tela.blit(graficos.com_alfa(self.vinheta_dano, 255 * self.alerta_vida), (0, 0))
        self.clarao.desenhar(tela)
        if self.faixa:
            self.faixa.desenhar(tela)

        if self.estado == "intro":
            self._desenhar_intro(tela)
            return

        self._desenhar_hud(tela)
        if self.estado == "pausa":
            self._desenhar_pausa(tela)
        elif self.estado == "fim":
            self._desenhar_fim(tela)

    def _desenhar_hud(self, tela):
        ocultar = 1.0 if self.estado != "fim" else max(0.0, 1 - self.t_fim * 2)
        if ocultar <= 0:
            return
        self._painel_combatente(tela, self.heroi, pygame.Rect(24, 18, 450, 122), True)
        self._painel_combatente(tela, self.vilao, pygame.Rect(L - 24 - 450, 18, 450, 122), False)
        self._desenhar_rodada(tela)

        graficos.painel(tela, RETANGULO_REGISTRO, 215)
        tela.blit(graficos.texto("CRÔNICA DA BATALHA", 13, tema.OURO, titulo=True, negrito=True), (RETANGULO_REGISTRO.x + 20, RETANGULO_REGISTRO.y + 12))
        self.registro.desenhar(tela, RETANGULO_REGISTRO)

        graficos.painel(tela, RETANGULO_ACOES, 215)
        if self.estado == "escolha" and self.grupo:
            if self.submenu:
                aba = pygame.Rect(RETANGULO_ACOES.x + 16, RETANGULO_ACOES.y - 32, 300, 30)
                graficos.painel(tela, aba, 230, raio=8)
                nome = "BOLSA DE ITENS" if self.submenu == "itens" else "TROCAR DE HERÓI"
                tela.blit(graficos.texto(nome, 14, tema.OURO, titulo=True, negrito=True), (aba.x + 14, aba.y + 6))
                dica = graficos.texto("Esc voltar", 13, tema.TEXTO_FRACO)
                tela.blit(dica, dica.get_rect(midright=(aba.right - 14, aba.centery + 1)))
            self.grupo.desenhar(tela, self.t)
        elif self.estado in ("animando", "pausa"):
            nome = self.ctrl.inimigo.nome if self._vez_do_inimigo() else self.ctrl.jogador.nome
            pontos = "." * (1 + int(self.t * 3) % 3)
            texto = graficos.texto(f"{nome} age{pontos}", 22, tema.TEXTO_FRACO, titulo=True)
            tela.blit(texto, texto.get_rect(midleft=(RETANGULO_ACOES.x + 40, RETANGULO_ACOES.centery)))

    def _vez_do_inimigo(self):
        return self.vez == "inimigo"

    def _desenhar_rodada(self, tela):
        escala = 1.0 + 0.35 * max(0.0, 1 - self.pop_rodada / 0.25)
        imagem = graficos.texto_dourado(f"RODADA {self.ctrl.rodada}", 26, espacamento=0)
        if escala > 1.01:
            imagem = pygame.transform.smoothscale(imagem, (int(imagem.get_width() * escala), int(imagem.get_height() * escala)))
        caixa = pygame.Rect(0, 0, 200, 46)
        caixa.center = (L // 2, 44)
        graficos.painel(tela, caixa, 220, raio=10)
        graficos.centralizar(tela, imagem, caixa.center)
        if self.estado == "escolha":
            texto, cor = "SUA VEZ", tema.OURO_CLARO
        elif self._vez_do_inimigo():
            texto, cor = f"TURNO DE {self.ctrl.inimigo.nome.upper()}", (255, 140, 130)
        else:
            texto, cor = "", tema.TEXTO
        if texto:
            imagem = graficos.texto_contorno(texto, 14, cor, espessura=2, titulo=True, negrito=True)
            graficos.centralizar(tela, imagem, (L // 2, 84))

    def _painel_combatente(self, tela, combatente, rect, esquerda):
        personagem = combatente.personagem
        graficos.painel(tela, rect, 215)
        centro_medalhao = (rect.x + 64, rect.centery) if esquerda else (rect.right - 64, rect.centery)
        widgets.medalhao(tela, combatente.chave, centro_medalhao, 86, combatente.cor, espelhar=not esquerda)

        x = rect.x + 128 if esquerda else rect.x + 22
        largura = rect.w - 152
        nome = graficos.texto_dourado(personagem.nome, 26, contorno=2)
        tela.blit(nome, (x - 2, rect.y + 4))
        if combatente.chave in tema.HEROIS:
            subtitulo = tema.HEROIS[combatente.chave]["classe"]
        else:
            subtitulo = tema.VILOES[type(personagem).__name__]["titulo"]
        sub = graficos.texto(subtitulo.upper(), 12, clarear(combatente.cor, 0.3), titulo=True, negrito=True)
        tela.blit(sub, (x, rect.y + 38))

        barra = pygame.Rect(x, rect.y + 58, largura, 20)
        critica = personagem.vida <= personagem.vida_maxima * 0.3
        widgets.barra(tela, barra, combatente.vida_mostrada, combatente.fantasma, personagem.vida_maxima, tema.VIDA, tema.VIDA_ESCURA, 0.35 if critica else 0.0)
        valor = graficos.texto_contorno(f"{max(0, round(combatente.vida_mostrada))} / {personagem.vida_maxima}", 14, tema.TEXTO, espessura=1, negrito=True)
        tela.blit(valor, valor.get_rect(midright=(barra.right - 6, barra.centery)))

        linha_y = rect.y + 93
        if hasattr(personagem, "mana"):
            caixa = pygame.Rect(x, linha_y, largura - 110, 10)
            widgets.barra(tela, caixa, combatente.mana_mostrada, combatente.mana_mostrada, personagem.mana_maxima, tema.MANA, tema.MANA_ESCURA, segmentos=5)
            texto = graficos.texto(f"MANA {personagem.mana}/{personagem.mana_maxima}", 13, (150, 190, 255), negrito=True)
            tela.blit(texto, texto.get_rect(midleft=(caixa.right + 10, caixa.centery)))
        elif hasattr(personagem, "flechas"):
            for i in range(min(personagem.flechas, 15)):
                widgets.icone_flecha(tela, (x + 10 + i * 16, linha_y + 5), 18, (230, 230, 240))
            cor = tema.TEXTO if personagem.flechas > 0 else tema.DANO
            texto = graficos.texto(f"{personagem.flechas} FLECHAS", 13, cor, negrito=True)
            tela.blit(texto, texto.get_rect(midright=(x + largura, linha_y + 5)))
        else:
            texto = graficos.texto(f"ATAQUE {personagem.ataque}   •   DEFESA {personagem.defesa}", 13, tema.TEXTO_FRACO, negrito=True)
            tela.blit(texto, (x, linha_y - 3))

        if getattr(personagem, "dano_bonus_rodada", 1.0) > 1.0:
            selo = pygame.Rect(0, 0, 88, 22)
            selo.topright = (rect.right - 10, rect.bottom + 6)
            pulso = 0.6 + 0.4 * math.sin(self.t * 6)
            graficos.desenhar_brilho(tela, selo.center, 50, tema.CRITICO, 0.4 * pulso)
            pygame.draw.rect(tela, (40, 28, 6), selo, border_radius=11)
            pygame.draw.rect(tela, tema.CRITICO, selo, 2, border_radius=11)
            graficos.centralizar(tela, graficos.texto(f"PODER {personagem.dano_bonus_rodada}x", 12, tema.CRITICO, negrito=True), selo.center)
        if combatente is self.vilao and critica and personagem.esta_vivo():
            selo = pygame.Rect(0, 0, 80, 22)
            selo.topleft = (rect.x + 10, rect.bottom + 6)
            pulso = 0.6 + 0.4 * math.sin(self.t * 7)
            graficos.desenhar_brilho(tela, selo.center, 50, (255, 40, 30), 0.5 * pulso)
            pygame.draw.rect(tela, (50, 6, 6), selo, border_radius=11)
            pygame.draw.rect(tela, (255, 80, 60), selo, 2, border_radius=11)
            graficos.centralizar(tela, graficos.texto("FÚRIA", 12, (255, 150, 130), negrito=True), selo.center)

    def _desenhar_intro(self, tela):
        entrada = sair_cubico(min(1.0, self.t / 0.6))
        barra = int(84 * entrada)
        pygame.draw.rect(tela, (0, 0, 0), (0, 0, L, barra))
        pygame.draw.rect(tela, (0, 0, 0), (0, A - barra, L, barra))

        cor = self.info_vilao["cor"]
        aparecer = max(0.0, min(1.0, (self.t - 0.5) / 0.6))
        if aparecer > 0:
            faixa = pygame.Surface((L, 250), pygame.SRCALPHA)
            faixa.blit(graficos.gradiente_vertical((L, 250), [(0, 0, 0, 0), (0, 0, 0, 190), (0, 0, 0, 190), (0, 0, 0, 0)], alfa=True), (0, 0))
            faixa.set_alpha(int(255 * aparecer))
            tela.blit(faixa, (0, 170))
            nome = graficos.texto_dourado(self.ctrl.inimigo.nome.upper(), 78, [clarear(cor, 0.75), clarear(cor, 0.2), escurecer(cor, 0.5)], contorno=3, espacamento=1)
            escala = 1.0 + 0.25 * (1 - sair_cubico(aparecer))
            nome = pygame.transform.smoothscale(nome, (int(nome.get_width() * escala), int(nome.get_height() * escala)))
            graficos.desenhar_brilho(tela, (L // 2, 236), 300, escurecer(cor, 0.4), aparecer * 0.8)
            graficos.centralizar(tela, graficos.com_alfa(nome, 255 * aparecer), (L // 2, 236))
            titulo = graficos.texto(self.info_vilao["titulo"].upper(), 18, clarear(cor, 0.4), titulo=True, negrito=True)
            graficos.centralizar(tela, graficos.com_alfa(titulo, 255 * aparecer), (L // 2, 290))
            graficos.divisor(tela, (L // 2, 312), int(380 * aparecer), cor)

        caracteres = int(max(0.0, self.t - 1.0) * 45)
        if caracteres > 0:
            fala = f"“{self.fala}”"
            imagem = graficos.texto_contorno(fala[:caracteres], 24, (240, 232, 220), (0, 0, 0), 2, titulo=True)
            graficos.centralizar(tela, imagem, (L // 2, 350))
        if self.t > 1.2:
            alfa = 0.5 + 0.5 * math.sin(self.t * 4)
            dica = graficos.texto("Pressione qualquer tecla para lutar", 18, tema.OURO_CLARO, titulo=True)
            graficos.centralizar(tela, graficos.com_alfa(dica, 255 * alfa), (L // 2, A - 42))
        local = graficos.texto(self.ctrl.inimigo.local, 16, (200, 190, 176))
        graficos.centralizar(tela, graficos.com_alfa(local, 255 * entrada), (L // 2, 42))

    def _desenhar_pausa(self, tela):
        camada = pygame.Surface((L, A), pygame.SRCALPHA)
        camada.fill((4, 2, 10, 190))
        tela.blit(camada, (0, 0))
        graficos.centralizar(tela, graficos.texto_dourado("PAUSA", 72, espacamento=1), (L // 2, 220))
        self.grupo_pausa.desenhar(tela, self.t)

    def _desenhar_fim(self, tela):
        p = min(1.0, self.t_fim / 0.8)
        camada = pygame.Surface((L, A), pygame.SRCALPHA)
        camada.fill((4, 2, 8, int(175 * p)))
        tela.blit(camada, (0, 0))

        heroi = self.ctrl.jogador
        vilao = self.ctrl.inimigo
        if self.fim == "vitoria":
            if self.raios:
                self.raios.desenhar(tela, p)
            cores = None
            titulo = "VITÓRIA"
            linhas = [
                f"{heroi.nome} sobrevive ao combate e segue sua jornada como um verdadeiro herói.",
                f"Rodadas: {self.ctrl.rodada}   •   Vida restante: {heroi.vida}/{heroi.vida_maxima}",
            ]
        elif self.fim == "fuga":
            cores = [(240, 240, 250), (170, 176, 190), (70, 74, 90)]
            titulo = "FUGA"
            linhas = ["Você fugiu da batalha! Viva para lutar outro dia.", f"{vilao.nome} ainda espreita nas sombras..."]
        elif self.fim == "empate":
            cores = [(230, 220, 255), (150, 130, 200), (60, 40, 90)]
            titulo = "EMPATE"
            linhas = ["Herói e vilão caem ao mesmo tempo.", "Eldoria chora por ambos."]
        else:
            cores = [(255, 180, 160), (210, 40, 40), (80, 8, 12)]
            titulo = "DERROTA"
            linhas = [f"A visão de {heroi.nome} escurece... {vilao.nome} vence desta vez.", "Mas lendas também nascem das quedas."]

        escala = graficos.sair_volta(p)
        imagem = graficos.texto_dourado(titulo, 120, cores, contorno=3, espacamento=1)
        imagem = pygame.transform.smoothscale(imagem, (max(1, int(imagem.get_width() * escala)), max(1, int(imagem.get_height() * escala))))
        cor_brilho = tema.OURO if self.fim == "vitoria" else (cores[1] if cores else tema.OURO)
        graficos.desenhar_brilho(tela, (L // 2, 260), 360, escurecer(cor_brilho, 0.35), p)
        graficos.centralizar(tela, imagem, (L // 2, 250))
        graficos.divisor(tela, (L // 2, 330), int(460 * p), cor_brilho)
        for i, linha in enumerate(linhas):
            alfa = max(0.0, min(1.0, (self.t_fim - 0.4 - i * 0.25) / 0.5))
            texto = graficos.texto(linha, 20 if i == 0 else 17, tema.TEXTO if i == 0 else tema.TEXTO_FRACO, titulo=(i == 0))
            graficos.centralizar(tela, graficos.com_alfa(texto, 255 * alfa), (L // 2, 372 + i * 36))
        if self.t_fim > 0.9 and self.grupo:
            camada = pygame.Surface((L, A), pygame.SRCALPHA)
            self.grupo.desenhar(camada, self.t)
            camada.set_alpha(int(255 * min(1.0, (self.t_fim - 0.9) / 0.4)))
            tela.blit(camada, (0, 0))
