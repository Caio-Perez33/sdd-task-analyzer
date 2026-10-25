# CONTEXT_RULES.md - TaskAnalyzer

## Objetivo
Este arquivo define os limites para qualquer assistente de IA que apoie a implementacao do TaskAnalyzer. O contrato em `specs/task_analyzer_spec.md` e a fonte de verdade do comportamento.

## Diretrizes obrigatorias
1. Usar Python 3.11 ou superior.
2. Adicionar type hints a todas as funcoes e metodos.
3. Seguir PEP 8, nomes descritivos e funcoes pequenas com responsabilidade unica.
4. Documentar modulos, classes e funcoes com docstrings no estilo Google.
5. Usar o modulo padrao `logging` para eventos relevantes.
6. Tratar dados invalidos por meio de excecoes especificas e mensagens objetivas.
7. Validar o comportamento com pytest antes de aceitar alteracoes.
8. Manter a implementacao simples, legivel e rastreavel ao contrato.

## Proibicoes explicitas
1. Nao adicionar bibliotecas de runtime nao autorizadas.
2. Nao alterar os cenarios de aceite sem documentar e aprovar o refinamento.
3. Nao alterar a estrutura de pastas definida pelo projeto.
4. Nao persistir tarefas em arquivos, bancos de dados ou servicos externos.
5. Nao alterar a assinatura publica `analyze_tasks(tasks)` sem autorizacao.
6. Nao introduzir funcionalidades sem testes correspondentes.
7. Nao duplicar codigo, adicionar complexidade sem necessidade ou inserir comentarios excessivos.
8. Nao assumir regras que nao estejam no contrato.
9. Nao retornar metricas em unidades diferentes das documentadas.
10. Nao tratar codigo gerado por IA como automaticamente correto.

## Regras de interacao com IA
1. Fornecer o contexto completo antes de gerar ou alterar codigo.
2. Pedir esclarecimento quando houver ambiguidade de negocio.
3. Revisar criticamente toda resposta gerada.
4. Rejeitar bibliotecas, persistencia ou regras que violem o contrato.
5. Relacionar cada comportamento relevante a um teste automatizado.

## Homologacao humana
A aceitacao final depende da revisao do diff, execucao dos testes, conferencia dos calculos e validacao dos arquivos CI/Docker. A IA auxilia a implementacao, mas a responsabilidade de aprovacao permanece humana.
