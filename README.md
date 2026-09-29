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

## Como executar

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

## Estrutura do projeto

```text
src/
  arqueiro.py
  batalha.py
  chefe_final.py
  esqueleto.py
  guerreiro.py
  inimigo.py
  item.py
  mago.py
  main.py
  personagem.py

tests/
  test_batalha.py
  test_personagem.py
```

## Regras de desenvolvimento

- Cada funcionalidade deve ser implementada em uma branch separada.
- Testes devem ser executados antes de enviar alterações.
- O código deve continuar compatível com a execução em linha de comando.

## Validação

Para rodar a suíte de testes:

```bash
python -m pytest -q
```
