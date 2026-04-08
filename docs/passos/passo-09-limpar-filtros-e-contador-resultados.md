# Passo 09 — Limpar filtros e contador de resultados

Data: 2026-04-08

## Objetivo
Melhorar a experiência no separador de pesquisa com:
- botão para limpar rapidamente os filtros
- contador de resultados encontrados

## O que foi implementado
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Botão `Limpar filtros` no bloco de pesquisa
- Método ` _limpar_filtros_pesquisa()` para:
  - limpar campos de texto
  - repor dropdowns para "Todos/Todas"
  - limpar tabela de resultados
- Label de contador `Resultados encontrados: X`
- Método `_atualizar_contador_resultados(total)`
- Atualização automática do contador após cada pesquisa

## Resultado
A pesquisa ficou mais prática e transparente: o utilizador limpa filtros com 1 clique e vê imediatamente quantos imóveis foram devolvidos.

## Próximo passo (sugestão)
- Adicionar ordenação de resultados (preço asc/desc, área asc/desc, data mais recente).
