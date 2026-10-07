import pygame

from . import graficos, tema, widgets
from .sons import Sons


class Jogo:

    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 512)
        pygame.init()
        pygame.display.set_caption(tema.TITULO_JANELA)
        pygame.display.set_icon(self._icone())
        self.tela = pygame.display.set_mode((tema.LARGURA, tema.ALTURA), pygame.SCALED | pygame.RESIZABLE)
        self.relogio = pygame.time.Clock()
        self.rodando = True
        self._carregando()
        self.sons = Sons()
        self.sons.iniciar_musica()

        self.cena = None
        self.proxima = None
        self.fade = 1.0
        self.saindo = False
        self.duracao_fade = 0.6
        self.cortina = pygame.Surface((tema.LARGURA, tema.ALTURA))
        self.aviso_som = 0.0

        from .cenas_menu import CenaAbertura

        self.cena = CenaAbertura(self)

    @staticmethod
    def _icone():
        icone = pygame.Surface((32, 32), pygame.SRCALPHA)
        widgets.icone_espada(icone, (16, 16), 30, tema.OURO)
        return icone

    def _carregando(self):
        self.tela.fill(tema.FUNDO)
        texto = graficos.texto_dourado("Forjando o reino de Eldoria...", 30)
        graficos.centralizar(self.tela, texto, (tema.LARGURA // 2, tema.ALTURA // 2))
        pygame.display.flip()
        pygame.event.pump()

    def ir_para(self, cena, duracao=0.35):
        if self.proxima is None:
            self.proxima = cena
            self.saindo = True
            self.duracao_fade = duracao

    def encerrar(self):
        self.rodando = False

    def passo(self, dt, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.encerrar()
                continue
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()
                    continue
                if evento.key == pygame.K_m:
                    mudo = self.sons.alternar_mudo()
                    self.aviso_som = 1.6 if self.sons.ativo else 0.0
                    self.texto_som = "Som desligado" if mudo else "Som ligado"
                    continue
            if self.proxima is None and self.fade < 0.5:
                self.cena.tratar_evento(evento)

        self.cena.atualizar(dt)

        if self.saindo:
            self.fade = min(1.0, self.fade + dt / self.duracao_fade)
            if self.fade >= 1.0:
                self.cena = self.proxima
                self.proxima = None
                self.saindo = False
        else:
            self.fade = max(0.0, self.fade - dt / self.duracao_fade)

        self.cena.desenhar(self.tela)
        if self.fade > 0:
            self.cortina.fill((0, 0, 0))
            self.cortina.set_alpha(int(255 * self.fade))
            self.tela.blit(self.cortina, (0, 0))
        if self.aviso_som > 0:
            self.aviso_som -= dt
            aviso = graficos.texto_contorno(self.texto_som, 18, tema.OURO_CLARO, espessura=2, titulo=True)
            self.tela.blit(graficos.com_alfa(aviso, 255 * min(1.0, self.aviso_som * 2)), (tema.LARGURA - aviso.get_width() - 20, tema.ALTURA - 44))

    def executar(self):
        while self.rodando:
            dt = min(self.relogio.tick(tema.FPS) / 1000, 1 / 20)
            self.passo(dt, pygame.event.get())
            pygame.display.flip()
        pygame.quit()
