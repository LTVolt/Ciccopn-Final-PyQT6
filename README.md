# Nota Importante 1: Para efeitos de gestão de tempo, foi utilizada IA - e consequentemente Vibe Coding. Em termos de BD, não houve IA envolvida.

# Nota Importante 2: As credenciais não vão funcionar fora do Ciccopn, terá de ser feita nova BD utilizando os ficheiros .sql fornecidos, e conectada corretamente nos ficheiros `db.py` e `.env`.

# Imobiliario PyQt6

Aplicação desktop em PyQt6 para gestão e consulta de imóveis, com base de dados existente.

## Abordagem
Vamos construir em passos curtos e validados.
Cada passo ficará documentado em `docs/passos`.

## Configuração rápida
1. Instalar dependências de `requirements.txt`.
2. Copiar `.env.example` para `.env` e preencher credenciais MySQL - Já feito por defeito.
3. Garantir que o schema está criado na base de dados.
4. Executar a aplicação pelo ponto de entrada `src/main.py`.

## Estado atual
- Projeto inicializado
- Estrutura base criada (`src/` e `docs/passos/`)
- Integração base com MySQL concluída
- Janela principal com 3 funcionalidades v1:
	- listar imóveis
	- pesquisar imóveis
	- criar anúncio

## Documentação por passo
- `docs/passos/passo-01-inicio-e-planeamento.md`
- `docs/passos/passo-02-mysql-e-base-da-app.md`
- `docs/passos/passo-03-pesquisa-por-localizacao.md`
- `docs/passos/passo-04-dropdowns-no-criar-anuncio.md`
- `docs/passos/passo-05-dropdown-anunciante-por-email.md`
- `docs/passos/passo-06-dropdown-anunciante-nome-email-tipo.md`
- `docs/passos/passo-07-melhoria-visual-tema-azul-bege.md`
- `docs/passos/passo-08-cabecalho-e-filtros-avancados-pesquisa.md`
- `docs/passos/passo-09-limpar-filtros-e-contador-resultados.md`
