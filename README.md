# TaskAnalyzer - Etapa Final do Bootcamp III

[![CI TaskAnalyzer](https://github.com/Caio-Perez33/sdd-task-analyzer/actions/workflows/ci.yml/badge.svg)](https://github.com/Caio-Perez33/sdd-task-analyzer/actions/workflows/ci.yml)

Projeto Python para calcular metricas de produtividade de tarefas, com contrato SDD, testes automatizados, CI/CD no GitHub Actions, containerizacao com Docker e controles de governanca para uso de IA.

## Estrutura do repositorio

```text
sdd-task-analyzer/
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── CONTEXT_RULES.md
├── requirements.yaml
├── requirements.txt
├── README.md
├── specs/
│   ├── system_design_document.pdf
│   └── task_analyzer_spec.md
├── src/
│   ├── __init__.py
│   └── task_analyzer.py
├── tests/
│   ├── __init__.py
│   └── test_harness.py
└── docs/
    ├── AI_PROMPT_LOG.md
    ├── Relatorio_Governanca_Etica_TaskAnalyzer.pdf
    └── Roteiro_Pitch_Etapa_Final.md
```

## Contrato funcional

A funcao publica `analyze_tasks(tasks)` valida IDs, prioridades, status e datas com fuso horario, converte as datas para UTC e devolve metricas gerais e por prioridade. Calcula contadores por status, tempo medio de conclusao em minutos e horas e percentual de tarefas concluidas apos o prazo. Quando nao existem tarefas concluidas, medias e taxa de atraso retornam `0.0`. Entradas invalidas geram `TaskValidationError`.

A implementacao nao persiste tarefas e nao usa bibliotecas externas em tempo de execucao. `pytest` e a unica dependencia de teste.

## Executar localmente

Requisitos: Python 3.11 ou superior.

### Git Bash (Windows)

```bash
python --version
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

### PowerShell (Windows)

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -v
```

### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v
```

## Docker e Docker Compose

Com o Docker Desktop aberto e o mecanismo Docker iniciado, execute na raiz do repositorio:

```bash
docker compose run --build --rm testes
```

O container usa `python:3.11-slim`, executa os mesmos testes em ambiente isolado e termina com codigo de saida diferente de zero se algum teste falhar. A imagem roda como usuario sem privilegios e o servico de testes usa filesystem somente leitura.

Tambem e possivel construir e executar diretamente:

```bash
docker build --pull -t sdd-task-analyzer:local .
docker run --rm sdd-task-analyzer:local
```

## CI/CD com GitHub Actions

O workflow `.github/workflows/ci.yml` e executado em `push` para `main`, `develop` e branches `feature/**`, em `pull_request` com destino a `main` ou `develop`, e manualmente pelo menu Actions. O pipeline instala as dependencias, executa os testes em Python 3.11 e depois constroi a imagem Docker. A etapa de imagem depende da aprovacao dos testes.

A configuracao esta preparada no codigo; o status verde precisa ser confirmado na aba Actions depois do push para o GitHub.

## Governanca e uso responsavel de IA

- `CONTEXT_RULES.md` limita a solucao ao contrato, proibe persistencia e dependencias nao autorizadas e exige testes e revisao humana.
- `specs/task_analyzer_spec.md` registra entradas, saidas, validacoes e a decisao sobre datas inconsistentes.
- O Test Harness cobre sucesso, datas invalidas, entradas vazias, tarefas pendentes, status invalido, IDs duplicados e falta de datas de execucao.
- Codigo gerado por IA deve ser revisto contra a especificacao; sugestoes nao sao aprovadas automaticamente.

Consulte `docs/Relatorio_Governanca_Etica_TaskAnalyzer.pdf` para a analise tecnica e `docs/Roteiro_Pitch_Etapa_Final.md` para a demonstracao de cinco minutos.

## Referencias internas

- `specs/task_analyzer_spec.md`: contrato SDD executavel.
- `specs/system_design_document.pdf`: desenho de componentes, fluxo de validacao e implantacao.
- `requirements.yaml`: resumo declarativo das dependencias e restricoes.
