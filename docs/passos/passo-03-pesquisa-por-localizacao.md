# Passo 03 — Pesquisa por localização com dropdowns

Data: 2026-04-08

## Objetivo
Permitir pesquisar imóveis por localização usando filtros opcionais de:
- Distrito
- Concelho
- Freguesia

com menus dropdown alimentados diretamente pelas tabelas da base de dados.

## O que foi implementado

### Repositório de dados
Em [src/data/repository.py](../../src/data/repository.py):
- `listar_distritos()`
- `listar_concelhos_por_distrito(id_distrito)`
- `listar_freguesias_por_concelho(id_concelho)`
- Extensão de `pesquisar_imoveis(...)` para aceitar filtros opcionais por:
  - `id_distrito`
  - `id_concelho`
  - `id_freguesia`

### Interface de pesquisa
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Adição de 3 dropdowns (`QComboBox`) no separador de pesquisa
- Carregamento inicial de distritos
- Carregamento encadeado:
  - ao escolher distrito -> atualiza concelhos
  - ao escolher concelho -> atualiza freguesias
- Opção `Todos` em cada nível para manter filtros opcionais
- Tabela de resultados da pesquisa passou a mostrar também localização

## Resultado
A pesquisa agora suporta, em simultâneo e de forma opcional:
- texto livre (morada/descrição)
- preço máximo
- distrito/concelho/freguesia

## Próximo passo (sugestão)
- Usar dropdown também no formulário de criação de anúncio para escolher `id_freguesia` sem inserção manual.
