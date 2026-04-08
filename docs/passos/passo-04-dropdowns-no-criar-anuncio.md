# Passo 04 — Dropdowns de localização no criar anúncio

Data: 2026-04-08

## Objetivo
Melhorar o formulário de criação de anúncio para escolher a localização por dropdowns, em vez de inserir `id_freguesia` manualmente.

## O que foi implementado
Em [src/ui/main_window.py](../../src/ui/main_window.py):
- Substituição do campo textual `ID Freguesia*` por 3 dropdowns:
  - `Distrito*`
  - `Concelho*`
  - `Freguesia*`
- Carregamento encadeado no formulário de criação:
  - ao escolher distrito -> carrega concelhos
  - ao escolher concelho -> carrega freguesias
- Validação na criação:
  - exige seleção de freguesia antes de submeter
- O `payload` da criação passa a usar o `id_freguesia` selecionado no dropdown.

## Resultado
A criação de anúncio fica mais segura e prática:
- menor risco de erro manual no `id_freguesia`
- experiência de utilização alinhada com o separador de pesquisa

## Próximo passo (sugestão)
- Trocar `ID Anunciante` por dropdown (ou pesquisa assistida) de anunciantes.
- Adicionar validações visuais de campos obrigatórios (com mensagem junto ao campo).
