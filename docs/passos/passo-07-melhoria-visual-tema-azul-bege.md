# Passo 07 — Melhoria visual (tema azul e bege)

Data: 2026-04-08

## Objetivo
Aplicar um visual mais apelativo e consistente na app PyQt6, com paleta em tons de azul e bege.

## O que foi implementado
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Adição de um tema global via `stylesheet` com:
  - fundo bege claro
  - abas com azul claro/escuro
  - campos (`QLineEdit` e `QComboBox`) com bordas suaves
  - botões com estilo principal azul
  - botão secundário (atualizar lista) em bege
  - tabela com cabeçalho azul e linhas alternadas
- Melhorias de layout/legibilidade das tabelas:
  - colunas ajustadas para preencher largura
  - ocultação de cabeçalho vertical
  - alternância de cores nas linhas

## Resultado
A interface mantém o comportamento atual, mas com uma apresentação mais moderna e clara.

## Próximo passo (sugestão)
- Adicionar ícones leves nos botões principais (pesquisar, criar, atualizar).
- Incluir feedback visual de validação junto aos campos obrigatórios.
