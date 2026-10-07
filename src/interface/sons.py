"""Efeitos sonoros e trilha ambiente sintetizados na hora, sem arquivos externos."""

import array
import math
import random

import pygame

TAU = math.tau


def _ruido_filtrado(n, suavidade):
    valor = 0.0
    saida = []
    for _ in range(n):
        valor += (random.uniform(-1, 1) - valor) * suavidade
        saida.append(valor)
    return saida


class Sons:

    def __init__(self):
        self.ativo = False
        self.mudo = False
        self.sons = {}
        self.musica = None
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(22050, -16, 2, 512)
            frequencia, tamanho, canais = pygame.mixer.get_init()
            if tamanho != -16:
                return
            self.taxa = frequencia
            self.canais = canais
            pygame.mixer.set_num_channels(24)
            pygame.mixer.set_reserved(1)
            self._criar()
            self.ativo = True
        except (pygame.error, OSError):
            self.ativo = False

    def _som(self, amostras, volume=0.5):
        dados = array.array("h")
        for valor in amostras:
            inteiro = int(max(-1.0, min(1.0, valor)) * 32767 * volume)
            dados.append(inteiro)
            if self.canais == 2:
                dados.append(inteiro)
        return pygame.mixer.Sound(buffer=dados.tobytes())

    def _gerar(self, duracao, funcao):
        n = int(duracao * self.taxa)
        return [funcao(i / self.taxa, i / n) for i in range(n)]

    def _criar(self):
        taxa = self.taxa

        def golpe():
            n = int(0.28 * taxa)
            ruido = _ruido_filtrado(n, 0.35)
            return [ruido[i] * math.exp(-i / taxa * 26) * 1.4 + math.sin(TAU * (130 - 260 * i / taxa) * i / taxa) * math.exp(-i / taxa * 14) for i in range(n)]

        def zunido(duracao, suavidade):
            n = int(duracao * taxa)
            ruido = _ruido_filtrado(n, suavidade)
            return [ruido[i] * math.sin(math.pi * i / n) ** 2 * 2.2 for i in range(n)]

        def explosao(duracao, grave=55):
            n = int(duracao * taxa)
            ruido = _ruido_filtrado(n, 0.12)
            return [ruido[i] * 2.5 * math.exp(-i / taxa * 5) + math.sin(TAU * grave * i / taxa) * math.exp(-i / taxa * 4) * 0.8 for i in range(n)]

        def metal(t, p):
            return sum(math.sin(TAU * f * t) for f in (523, 1307, 2091, 3011)) * 0.25 * math.exp(-t * 9)

        def carregar(t, p):
            frequencia = 260 + 700 * p * p
            return (math.sin(TAU * frequencia * t) * 0.5 + math.sin(TAU * frequencia * 1.5 * t + math.sin(t * 40)) * 0.3) * p

        def notas(sequencia, duracao_nota, total, timbre=1.0):
            def funcao(t, p):
                valor = 0.0
                for indice, frequencia in enumerate(sequencia):
                    inicio = indice * duracao_nota
                    if t >= inicio:
                        local = t - inicio
                        envelope = min(1.0, local * 60) * math.exp(-local * (3.0 / timbre))
                        valor += (math.sin(TAU * frequencia * t) + 0.3 * math.sin(TAU * frequencia * 2 * t) + 0.12 * math.sin(TAU * frequencia * 3 * t)) * envelope
                return valor * 0.35
            return self._gerar(total, funcao)

        def falha(t, p):
            frequencia = 420 - 300 * p
            onda = 1.0 if math.sin(TAU * frequencia * t) > 0 else -1.0
            return onda * 0.25 * (1 - p) * (0.7 + 0.3 * math.sin(t * 90))

        def clique(t, p):
            return math.sin(TAU * 880 * t) * math.exp(-t * 60)

        def passar(t, p):
            return math.sin(TAU * 1400 * t) * math.exp(-t * 90) * 0.5

        def furia(t, p):
            serra = ((70 + 20 * math.sin(t * 30)) * t) % 1.0 * 2 - 1
            return (serra * 0.5 + random.uniform(-1, 1) * 0.25) * math.sin(math.pi * p) ** 0.5

        def troca(t, p):
            frequencia = 400 + 900 * p
            return math.sin(TAU * frequencia * t) * math.sin(math.pi * p) * 0.6

        self.sons = {
            "golpe": self._som(golpe(), 0.55),
            "corte": self._som(zunido(0.22, 0.5), 0.35),
            "flecha": self._som(zunido(0.16, 0.8), 0.3),
            "carregar": self._som(self._gerar(0.55, carregar), 0.3),
            "explosao": self._som(explosao(0.7), 0.55),
            "critico": self._som(explosao(0.9, 42), 0.75),
            "bloqueio": self._som(self._gerar(0.45, metal), 0.45),
            "cura": self._som(notas([523, 659, 784, 1047], 0.08, 0.7), 0.5),
            "falha": self._som(self._gerar(0.45, falha), 0.4),
            "clique": self._som(self._gerar(0.06, clique), 0.35),
            "passar": self._som(self._gerar(0.03, passar), 0.18),
            "vitoria": self._som(notas([392, 523, 659, 784, 1047, 784, 1047], 0.13, 2.2, 2.5), 0.55),
            "derrota": self._som(notas([392, 349, 311, 262, 196], 0.32, 2.6, 3.0), 0.5),
            "furia": self._som(self._gerar(0.7, furia), 0.45),
            "especial": self._som(explosao(1.4, 36), 0.85),
            "troca": self._som(self._gerar(0.4, troca), 0.35),
            "fuga": self._som(zunido(0.35, 0.3), 0.35),
        }
        self.musica = self._som(self._trilha(), 0.22)

    def _trilha(self):
        # Todas as frequências são múltiplas de 0,25 Hz: o laço de 8 s fecha sem emenda.
        duracao = 8.0
        acordes = [(55.0, 82.5, 110.0, 130.75), (49.0, 73.5, 98.0, 116.5)]

        def funcao(t, p):
            acorde = acordes[0] if t < duracao / 2 else acordes[1]
            local = t % (duracao / 2)
            entrada = min(1.0, local / 0.6) * min(1.0, (duracao / 2 - local) / 0.6)
            valor = 0.0
            for indice, frequencia in enumerate(acorde):
                valor += math.sin(TAU * frequencia * t) * (0.5 if indice == 0 else 0.25)
                valor += math.sin(TAU * (frequencia + 0.25) * t) * 0.12
            pulso = 0.75 + 0.25 * math.sin(TAU * 0.5 * t)
            batida = math.sin(TAU * 41 * t) * math.exp(-(t % 2.0) * 9) * 0.9
            return (valor * 0.4 * entrada * pulso) + batida

        return self._gerar(duracao, funcao)

    def tocar(self, nome, volume=1.0):
        if not self.ativo or self.mudo or nome not in self.sons:
            return
        canal = pygame.mixer.find_channel(True)
        if canal:
            canal.set_volume(volume)
            canal.play(self.sons[nome])

    def iniciar_musica(self):
        if self.ativo and self.musica and not self.mudo:
            pygame.mixer.Channel(0).play(self.musica, loops=-1, fade_ms=1500)

    def alternar_mudo(self):
        self.mudo = not self.mudo
        if not self.ativo:
            return self.mudo
        if self.mudo:
            pygame.mixer.stop()
        else:
            self.iniciar_musica()
        return self.mudo
