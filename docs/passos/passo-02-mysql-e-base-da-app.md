# Passo 02 — MySQL e base da app PyQt6

Data: 2026-04-08

## Objetivo
Criar a base técnica da aplicação desktop em PyQt6, já ligada a MySQL, e preparar as 3 funcionalidades da v1:
1. Listar imóveis
2. Pesquisar imóveis
3. Criar anúncio

## Informação recebida
- SGBD: MySQL
- Ligação: host/porta
- Funcionalidades prioritárias: listar, pesquisar, criar anúncio
- Estrutura SQL das tabelas partilhada

## Correção identificada no SQL
Foi identificado um desajuste de tipos:
- `freguesia.id_freguesia` está como `VARCHAR(9)`
- `imovel.id_freguesia` foi criado como `INT`

Isto pode causar erro de integridade referencial na foreign key.

### Script de correção
- [docs/sql/correcao-imovel-id_freguesia.sql](../sql/correcao-imovel-id_freguesia.sql)

## O que foi implementado neste passo
- Configuração de dependências:
  - [requirements.txt](../../requirements.txt)
  - [.env.example](../../.env.example)
- Camada de ligação MySQL:
  - [src/data/db.py](../../src/data/db.py)
- Repositório de dados dos imóveis:
  - [src/data/repository.py](../../src/data/repository.py)
- Interface principal com 3 separadores:
  - [src/ui/main_window.py](../../src/ui/main_window.py)
- Ponto de entrada da app:
  - [src/main.py](../../src/main.py)

## Resultado
Já existe uma versão funcional base da aplicação com:
- Listagem de imóveis
- Pesquisa por texto (e preço máximo opcional)
- Criação de anúncio (campos principais)

## Próximo passo (Passo 03)
- Melhorar UX e validações de formulário
- Adicionar seleção guiada de localização (Distrito > Concelho > Freguesia)
- Criar ecrã de detalhes do imóvel
