# Passo 08 — Cabeçalho e filtros avançados na pesquisa

Data: 2026-04-08

## Objetivo
1. Adicionar um cabeçalho visual com nome do portal + subtítulo.
2. Enriquecer os filtros do separador de pesquisa.

## O que foi implementado

### Cabeçalho visual
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Criação de cabeçalho no topo da janela com:
  - título: `Imociccopn — Portal Imobiliário`
  - subtítulo: `Pesquisa e gestão de anúncios de imóveis`
- Ajustes de estilo para o cabeçalho no tema (`QLabel#portalTitle` e `QLabel#portalSubtitle`).

### Novos filtros no separador Pesquisar
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Campos adicionais:
  - `Preço mín` (opcional)
  - `Preço máx` (opcional)
  - `Área mín` (opcional)
  - `Área máx` (opcional)
- Dropdown de tipologia:
  - `Todas`, `T0`, `T1`, `T2`, `T3`, `T4`, `T5`
- Dropdown de casas de banho:
  - `Todos`, `0`, `1`, `2`, `3`, `4`, `5`
- Validações de intervalo:
  - `preço mínimo <= preço máximo`
  - `área mínima <= área máxima`

### Camada de dados
Em [src/data/repository.py](../../src/data/repository.py):
- O método `pesquisar_imoveis(...)` passou a aceitar e aplicar novos filtros opcionais:
  - `preco_min`, `preco_max`
  - `area_min`, `area_max`
  - `tipologia` (`numero_quartos`)
  - `numero_wc`
  - mantendo filtros de localização (`distrito`, `concelho`, `freguesia`).

## Resultado
Pesquisa consideravelmente mais completa, sem perder simplicidade de uso.

## Próximo passo (sugestão)
- Adicionar botão `Limpar filtros` no separador de pesquisa.
- Mostrar número de resultados encontrados após cada pesquisa.
