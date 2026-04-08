# Passo 06 — Dropdown de anunciante com Nome - Email - Tipo

Data: 2026-04-08

## Objetivo
Melhorar a UX do formulário de criação de anúncio para que o dropdown de anunciante mostre informação mais reconhecível.

## O que foi implementado

### Repositório
Em [src/data/repository.py](../../src/data/repository.py):
- O método `listar_anunciantes()` foi enriquecido para devolver:
  - `id_anunciante`
  - `email`
  - `nome` (resolvido por `COALESCE` entre proprietário, consultor ou agência)
  - `tipo_label` (ex.: `Proprietário`, `Consultor`, `Agência`)

### UI
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- O label do campo passou para: `Anunciante (Nome - Email - Tipo)*`
- Cada opção no dropdown é mostrada como:
  - `Nome - Email - Tipo`
- Internamente continua a guardar e enviar o `id_anunciante` para a inserção na tabela `imovel`.

## Resultado
Dropdown mais informativo e rápido de usar, sem perder compatibilidade com a base de dados.

## Próximo passo (sugestão)
- Adicionar caixa de pesquisa (filtro) para anunciantes quando houver muitos registos.
