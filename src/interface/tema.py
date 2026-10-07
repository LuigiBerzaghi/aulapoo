LARGURA, ALTURA = 1280, 720
FPS = 60
TITULO_JANELA = "Eldoria - Jogo de Batalha RPG"

# Paleta geral
FUNDO = (8, 7, 14)
OURO = (232, 188, 96)
OURO_CLARO = (255, 232, 170)
OURO_ESCURO = (118, 84, 38)
TEXTO = (238, 232, 218)
TEXTO_FRACO = (150, 140, 128)
PAINEL = (14, 12, 22)
VIDA = (222, 50, 68)
VIDA_ESCURA = (70, 12, 22)
FANTASMA = (255, 214, 130)
MANA = (70, 140, 255)
MANA_ESCURA = (14, 26, 70)
CURA = (110, 236, 140)
CRITICO = (255, 204, 60)
DANO = (255, 86, 86)
BLOQUEIO = (150, 190, 255)

FONTES_TITULO = "cinzel,trajanpro,palatinolinotype,bookantiqua,georgia,timesnewroman"
FONTES_TEXTO = "segoeui,calibri,arial"

# Posições da arena
CHAO_Y = 505
HEROI_X = 340
VILAO_X = 940

HEROIS = {
    "guerreiro": {
        "classe": "Guerreiro",
        "titulo": "O Escudo do Reino",
        "cor": (240, 176, 86),
        "descricao": ["Mais vida e defesa.", "Golpes de dano constante."],
    },
    "mago": {
        "classe": "Mago",
        "titulo": "O Arcano de Eldoria",
        "cor": (96, 196, 255),
        "descricao": ["Magia: 20 de mana, 20 a 45 de dano.", "Pode falhar (1/5) ou ser crítica (1/8)."],
    },
    "arqueiro": {
        "classe": "Arqueiro",
        "titulo": "A Flecha Silenciosa",
        "cor": (130, 226, 120),
        "descricao": ["Começa com 10 flechas.", "Cada tiro soma de 0 a 8 de dano."],
    },
}

VILOES = {
    "Goblin": {"titulo": "Saqueador da Floresta", "cor": (150, 210, 80), "cenario": "floresta"},
    "Esqueleto": {"titulo": "Guardião da Cripta", "cor": (140, 255, 180), "cenario": "cripta"},
    "GuerreiroSombrio": {"titulo": "O Herói Caído", "cor": (255, 96, 56), "cenario": "ruinas"},
    "MagoSombrio": {"titulo": "Senhor das Runas", "cor": (196, 110, 255), "cenario": "torre"},
    "ArqueiroSombrio": {"titulo": "O Olho na Névoa", "cor": (255, 84, 110), "cenario": "desfiladeiro"},
    "ChefeFinal": {"titulo": "Senhor do Castelo da Noite", "cor": (110, 170, 255), "cenario": "trono"},
}

# Escala de cada figura na arena (1.0 = altura padrão)
ESCALA_FIGURA = {
    "guerreiro": 1.0,
    "mago": 1.0,
    "arqueiro": 1.0,
    "goblin": 0.95,
    "esqueleto": 1.0,
    "guerreirosombrio": 1.08,
    "magosombrio": 1.05,
    "arqueirosombrio": 1.0,
    "chefefinal": 1.32,
}
