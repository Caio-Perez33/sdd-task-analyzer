# TaskAnalyzer - Especificacao SDD (contrato refinado para a Etapa Final)

## 1. Objetivo
Receber uma colecao de tarefas e produzir metricas gerais e por prioridade, sem gravar dados em arquivos ou bancos de dados.

## 2. Interface publica
`analyze_tasks(tasks: list[dict[str, object]]) -> dict[str, object]`

A funcao recebe uma lista de tarefas. Cada tarefa deve possuir:

| Campo | Tipo | Obrigatorio | Regra |
|---|---|---|---|
| `id_tarefa` | int | Sim | Inteiro positivo e unico na lista. |
| `data_criacao` | datetime | Sim | Data/hora com fuso; normalizada para UTC. |
| `data_inicio` | datetime ou None | Para tarefa concluida | Inicio da execucao. |
| `data_conclusao` | datetime ou None | Para tarefa concluida | Fim da execucao. |
| `prazo` | datetime | Sim | Data/hora limite, com fuso. |
| `prioridade` | str | Sim | `baixa`, `media` ou `alta`. |
| `status` | str | Sim | `concluida`, `pendente` ou `cancelada`. |

A implementacao exige timestamps com fuso para evitar ambiguidade de timezone e converte todos para UTC.

## 3. Validacoes
- Rejeitar tarefas que nao sejam objetos de mapeamento.
- Rejeitar ID ausente, nao inteiro, menor ou igual a zero ou repetido.
- Rejeitar prioridade/status fora dos enumerados autorizados.
- Rejeitar datas que nao sejam `datetime` com fuso horario.
- Rejeitar `data_inicio` anterior a `data_criacao`.
- Para tarefa concluida, exigir `data_inicio` e `data_conclusao`.
- Rejeitar conclusao anterior a criacao ou ao inicio.
- Usar `TaskValidationError` para entradas invalidas.

## 4. Regras de metricas
- `total_tarefas` e `quantidade_tarefas` contam todas as tarefas recebidas, incluindo as canceladas.
- `total_concluidas`, `total_pendentes` e `total_canceladas` contam cada status separadamente.
- Tempo de conclusao = `data_conclusao - data_inicio`, em minutos.
- Media de tempo considera apenas tarefas concluidas; apresenta minutos e horas, arredondados a duas casas.
- Uma tarefa concluida esta atrasada se `data_conclusao > prazo`.
- Taxa de atraso = tarefas concluidas apos o prazo / total concluido * 100.
- Medias e taxa de atraso retornam `0.0` quando nao ha tarefas concluidas; nao ocorre divisao por zero.
- Repetir as metricas para o total geral e para cada prioridade.

## 5. Estrutura de saida
A resposta inclui `total_tarefas`, contadores por status, `quantidade_tarefas`, `tempo_medio_conclusao_min`, `tempo_medio_conclusao_horas`, `taxa_atraso_percentual` e `indicadores_por_prioridade`. O mapa de prioridades sempre contem `baixa`, `media` e `alta`, mesmo quando uma prioridade nao aparece na entrada.

## 6. Cenarios automatizados
1. Sucesso: metricas gerais e por prioridade corretas.
2. Erro: cronologia invalida gera `TaskValidationError`.
3. Entrada vazia retorna metricas numericas zero.
4. Apenas tarefas pendentes retorna medias e taxa zero.
5. Status invalido gera erro especifico.
6. ID duplicado gera erro especifico.
7. Tarefa concluida sem datas de execucao gera erro.
8. Conclusao anterior ao inicio gera erro.

## 7. Refinamento e rastreabilidade
A especificacao inicial menciona ignorar datas inconsistentes; a entrega intermediaria solicita `TaskValidationError` para datas inconsistentes. Este pacote adota a excecao especifica e documenta essa escolha. A regra de zero para ausencia de tarefas concluidas tambem e mantida, conforme os casos de borda da etapa intermediaria.
