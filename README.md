# ⚔️ Jogo de Batalha RPG

Projeto desenvolvido na disciplina de Programação Orientada a Objetos.

## Visão geral

Este jogo simula um combate por turnos em que o jogador escolhe um herói, enfrenta inimigos e usa itens para sobreviver. O projeto foi expandido para incluir:

- Poção de vida
- Uso de itens em combate
- Turno do inimigo após cada ação do jogador
- Condição de vitória/derrota
- Classe Arqueiro
- Novo tipo de inimigo: Esqueleto
- Chefe final
- Testes automatizados para personagens e batalha
- Troca de personagem durante a batalha
- Mago com mana, magia que pode falhar ou dar crítico e poção de mana
- Pergaminho arcano, que aumenta o dano do próximo ataque
- Inventário diferente para cada herói
- Vilões sombrios (Guerreiro, Mago e Arqueiro Sombrio)
- Opção de fugir da batalha
- Barra de vida, narrativa e pausas entre as rodadas

## Como executar

É preciso ter o Python 3 instalado. O jogo não usa bibliotecas externas.

Na raiz do projeto, use:

```bash
python src/main.py
```

Você também pode iniciar com um personagem específico:

```bash
python src/main.py guerreiro
python src/main.py mago
python src/main.py arqueiro
```

Para ir direto para a batalha do Guerreiro contra o chefe final:

```bash
python src/main.py chefe
```

Para sair, escolha a opção 4 no menu de heróis ou pressione `Ctrl + C` a qualquer momento.

## Interface gráfica (pygame)

O jogo também tem uma versão com janela, animações, efeitos e trilha sonora. Ela usa as mesmas classes e regras da versão de terminal.

```bash
pip install -r requirements.txt
python src/main_pygame.py
```

Na versão gráfica:

- Use as setas e o Enter, as teclas numéricas ou o mouse para escolher as opções.
- Esc volta ao menu anterior ou pausa a batalha.
- M liga e desliga o som. F11 alterna a tela cheia.
- Cada vilão tem o próprio cenário. Os golpes têm animação, números de dano, tremor de tela e efeitos de partículas.

Todos os gráficos e sons são gerados pelo código. O projeto não usa arquivos de imagem nem de áudio.

## Como jogar

1. Escolha um herói e o vilão que deseja enfrentar.
2. A cada rodada, escolha uma ação: atacar, usar magia (só o Mago), usar item, trocar de personagem ou fugir.
3. Depois da sua ação, o vilão ataca de volta. Pressione Enter para seguir para a próxima rodada.
4. A defesa de quem é atingido é descontada do dano de cada golpe.
5. A batalha termina quando um dos lados chega a 0 de vida (vitória ou derrota) ou quando você foge.

Trocar de personagem não gasta a rodada: o novo herói entra com a vida cheia e o vilão não ataca.

### Heróis

| Herói | Nome | Vida | Ataque | Defesa | Diferencial |
|-------|------|------|--------|--------|-------------|
| Guerreiro | Arthur | 120 | 20 | 10 | Mais vida e defesa, dano sempre igual |
| Mago | Merlin | 80 | 30 | 5 | Magia: gasta 20 de mana e causa de 20 a 45 de dano. Pode falhar (1 em 5) ou dar crítico de +20 (1 em 8) |
| Arqueiro | Legolas | 100 | 18 | 8 | Começa com 10 flechas. Cada tiro gasta uma e soma de 0 a 8 de dano. Sem flechas, não consegue atacar |

### Vilões

| Vilão | Vida | Ataque | Defesa | Observação |
|-------|------|--------|--------|------------|
| Goblin | 70 | 18 | 4 | - |
| Esqueleto | 70 | 18 | 4 | - |
| Guerreiro Sombrio | 100 | 22 | 8 | Não aparece para o Guerreiro |
| Mago Sombrio | 90 | 24 | 6 | Não aparece para o Mago |
| Arqueiro Sombrio | 85 | 20 | 7 | Não aparece para o Arqueiro |
| Chefe Final | 200 | 35 | 12 | Com 30% de vida ou menos, usa o Golpe do Crepúsculo (+15 de dano) |

### Itens

Cada item pode ser usado uma vez. A cura nunca passa da vida máxima.

| Item | Herói | Efeito |
|------|-------|--------|
| Poção de vida | Todos | Recupera 20 de vida |
| Bandagem | Guerreiro | Recupera 15 de vida |
| Elixir do soldado | Guerreiro | Recupera 25 de vida |
| Poção de mana | Mago | Recupera 25 de mana |
| Pergaminho arcano | Mago | O próximo ataque ou magia causa 1.5x de dano |
| Flecha especial | Arqueiro | Dá 5 flechas extras |
| Elixir do arqueiro | Arqueiro | Recupera 18 de vida |

### Exemplo de tela

```text
========================================
                RODADA 2
========================================
Arthur | Vida: [##################--] 112/120 | Ataque: 20 | Defesa: 10
Goblin | Vida: [###############-----] 54/70 | Ataque: 18 | Defesa: 4
Inventário: Poção de vida, Bandagem, Elixir do soldado

--- AÇÕES ---
0 - Trocar de personagem
1 - Atacar
2 - Usar item
3 - Fugir
Escolha uma opção: 1

Arthur decide atacar!
Arthur avança com sua espada e investe contra Goblin!
Goblin sofre 16 de dano! (a defesa bloqueou 4)

--- Turno de Goblin ---
Goblin aproveita a abertura e acerta Arthur!
Arthur sofre 8 de dano! (a defesa bloqueou 10)

Pressione Enter para continuar...
```

## Estrutura do projeto

```text
src/
  arqueiro.py      classe Arqueiro (flechas)
  batalha.py       classe Batalha: rodadas, turnos, itens e fim da batalha
  chefe_final.py   atalho para importar o ChefeFinal
  esqueleto.py     atalho para importar o Esqueleto
  guerreiro.py     classe Guerreiro
  inimigo.py       classe Inimigo e todos os vilões
  item.py          classe Item e o efeito de cada item
  mago.py          classe Mago (mana e magia)
  main.py          abertura, menus de escolha e início do jogo
  main_pygame.py   início da versão gráfica
  personagem.py    classe base Personagem (vida, dano e status)
  interface/       versão gráfica em pygame
    controlador.py   liga a interface à Batalha (não depende do pygame)
    app.py           laço principal, transições, som e tela cheia
    cenas_menu.py    abertura, escolha de herói e de oponente
    cena_batalha.py  arena, animações, HUD, crônica e telas de fim
    figuras.py       personagens desenhados por código
    cenarios.py      cenários de cada vilão
    efeitos.py       partículas, textos flutuantes, tremor e projéteis
    sons.py          efeitos sonoros e trilha sintetizados
    widgets.py       botões, barras, ícones e retratos

tests/
  test_batalha.py                testes da batalha
  test_personagem.py             testes dos heróis, vilões e itens
  test_interface_controlador.py  testes da ponte entre interface e jogo
  test_interface_grafica.py      batalha completa na interface, sem abrir janela
```

## Regras de desenvolvimento

- Cada funcionalidade deve ser implementada em uma branch separada.
- Testes devem ser executados antes de enviar alterações.
- O código deve continuar compatível com a execução em linha de comando.

## Validação

Para rodar a suíte de testes, instale as dependências (só na primeira vez) e execute os comandos abaixo. Sem o pygame instalado, o teste da interface gráfica é ignorado.

```bash
pip install -r requirements.txt
python -m pytest -q
```
