# Registro de prompt-base e decisoes de governanca

Este registro documenta o contexto recomendado para solicitar mudancas no TaskAnalyzer. Ele nao afirma que cada frase abaixo foi usada literalmente em todas as iteracoes.

## Prompt-base rastreavel

> Leia `CONTEXT_RULES.md` e `specs/task_analyzer_spec.md` antes de sugerir qualquer mudanca. Implemente somente o comportamento previsto no contrato, usando Python 3.11+, type hints, docstrings no estilo Google, logging padrao e excecoes especificas. Nao adicione bibliotecas externas de runtime, nao persista dados e nao altere a assinatura publica `analyze_tasks(tasks)`. Inclua ou atualize testes pytest para cada comportamento. Explique ambiguidades e decisoes de compatibilidade, principalmente datas UTC, cronologia de tarefas e entradas sem tarefas concluidas. Ao final, informe os testes que foram executados e quaisquer validacoes que ainda dependem do ambiente do repositorio.

## Decisoes documentadas

1. Uma tarefa concluida sem data de inicio ou de conclusao e invalida.
2. Timestamps sem fuso sao rejeitados para evitar interpretacao ambigua de UTC.
3. Conclusao anterior a criacao ou ao inicio gera `TaskValidationError`.
4. Sem tarefas concluidas, a media e a taxa de atraso retornam `0.0`.
5. Dependencias de runtime permanecem vazias; `pytest` e usado apenas na verificacao.
6. CI executa testes antes da construcao da imagem Docker.
7. O container executa os testes como usuario nao-root e com filesystem somente leitura via Compose.

## Homologacao

Antes do merge, conferir o diff, revisar a especificacao, rodar `python -m pytest -v`, validar `docker compose run --build --rm testes` e confirmar o resultado verde em GitHub Actions. A revisao humana e obrigatoria.
