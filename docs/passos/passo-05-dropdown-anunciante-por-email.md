# Passo 05 — Dropdown de anunciante por email

Data: 2026-04-08

## Objetivo
Melhorar o formulário de criação de anúncio para selecionar o anunciante por email (UX), mantendo o `id_anunciante` internamente.

## O que foi implementado

### Repositório
Em [src/data/repository.py](../../src/data/repository.py):
- Novo método `listar_anunciantes()` que devolve:
  - `id_anunciante`
  - `email`

### UI (Criar anúncio)
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Substituição do campo manual `ID Anunciante*` por dropdown:
  - `Anunciante (email)*`
- O dropdown mostra o `email` ao utilizador, mas guarda internamente o `id_anunciante`.
- Na submissão (`_criar_anuncio`), o `payload` usa esse id interno.
- Adicionada validação para obrigar seleção de anunciante.

## Resultado
A UX melhora porque:
- o utilizador escolhe por email (informação reconhecível)
- evita erro de escrever ids manualmente
- compatibilidade mantida com o schema da base de dados

## Próximo passo (sugestão)
- Mostrar nome/tipo do anunciante junto ao email no dropdown (ex.: `email — Consultor`).
- Validar unicidade de email na tabela `anunciante` (se fizer sentido para o domínio).
