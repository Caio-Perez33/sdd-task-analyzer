# TaskAnalyzer - Especificação SDD

## 1. Visão geral

### 1.1 Propósito
O módulo TaskAnalyzer deve analisar tarefas executadas e gerar métricas de produtividade. Deve calcular o tempo médio de conclusão por tipo/prioridade, identificar a taxa de atraso, gerar indicadores por prioridade e fornecer métricas para tomada de decisão e melhoria contínua.

### 1.2 Contrato executável de interface

#### 1.2.1 Entradas (inputs)

| Campo | Tipo | Obrigatório | Descrição / Restrições |
|---|---|---|---|
| `id_tarefa` | `int` | Sim | Identificador único da tarefa (> 0) |
| `data_criacao` | `datetime` | Sim | Data/hora de criação (UTC) |
| `data_inicio` | `datetime` | Não | Data/hora de início da execução |
| `data_conclusao` | `datetime` | Não | Data/hora de conclusão da execução |
| `prazo` | `datetime` | Sim | Data/hora limite para conclusão |
| `prioridade` | `str enum` | Sim | Valores: `baixa`, `media`, `alta` |
| `status` | `str enum` | Sim | Valores: `concluida`, `pendente`, `cancelada` |

#### 1.2.2 Saídas (outputs)

| Campo | Tipo | Descrição |
|---|---|---|
| `tempo_medio_conclusao_min` | `float` | Tempo médio de conclusão em minutos (por prioridade e geral) |
| `taxa_atraso_percentual` | `float` | Percentual de tarefas concluídas após o prazo (por prioridade e geral) |
| `quantidade_tarefas` | `int` | Total de tarefas consideradas na análise (por prioridade e geral) |
| `indicadores_por_prioridade` | `dict` | Estrutura com métricas agrupadas por prioridade (`baixa`, `media`, `alta`) |

#### 1.2.3 Regras de negócio e restrições
1. Considerar apenas tarefas cujo status seja `concluida` para o cálculo de tempo e atraso.
2. Calcular tempo de conclusão como `data_conclusao - data_inicio`, em minutos.
3. Considerar tarefa em atraso quando `data_conclusao > prazo`.
4. Ignorar tarefas com datas inconsistentes, como conclusão anterior ao início.
5. Tratar divisão por zero quando não houver tarefas concluídas.
6. Usar UTC como referência de fuso horário.
7. Arredondar tempos e percentuais para 2 casas decimais.

## 2. Cenários de aceite e Test Harness

### 2.1 Cenário 1 - Sucesso (métricas corretas)
**Dado:** um conjunto de tarefas válidas com diferentes prioridades, prazos e status (`concluida` e `pendente`).

**Quando:** o analisador de tarefas for executado.

**Então:** as métricas retornadas devem estar corretas, incluindo:
- tempo médio de conclusão por prioridade e geral;
- taxa de atraso correta por prioridade e geral;
- quantidade de tarefas corretas por prioridade.

### 2.2 Cenário 2 - Exceção / Erro (entradas inválidas)
**Dado:** uma entrada com datas inválidas (por exemplo, conclusão antes do início) ou ausência de tarefas concluídas, o que pode levar à divisão por zero.

**Quando:** o analisador de tarefas for executado.

**Então:** deve disparar uma exceção específica tratada, com mensagem clara e objetiva ao usuário.

### 2.3 Planejamento do Test Harness
Os cenários descritos acima devem ser convertidos em casos de teste específicos. O Test Harness deve:
- separar cenário de aceite em casos de teste;
- preparar os dados de entrada e os resultados esperados;
- usar `pytest` para os testes automatizados;
- validar outputs, tipos e exceções;
- executar os testes continuamente e bloquear o avanço da próxima fase em caso de falha;
- produzir evidências/relatórios de resultado e cobertura.

## 3. Arquitetura preparada para a Fase 2

```text
sdd-task-analyzer/
├── README.md
├── CONTEXT_RULES.md
├── specs/
│   └── task_analyzer_spec.md
├── tests/
│   └── test_harness.py
├── src/
│   └── task_analyzer.py
├── .gitignore
└── requirements.txt
```

## 4. Estratégia de versionamento (preparação para a Fase 2)
- Git Flow simplificado: `main`, `develop`, `feature/*`.
- Commits pequenos e descritivos.
- Pull Requests para revisão e aprovação.
- Revisões obrigatórias antes do merge.
- Tags para releases importantes.

## 5. Homologação humana
Antes de aceitar qualquer código gerado por IA:
1. executar os testes automatizados e verificar cobertura;
2. revisar conformidade com o contrato de negócio e com `CONTEXT_RULES.md`;
3. analisar qualidade, legibilidade e tratamento de erros;
4. verificar se não houve violação das proibições;
5. realizar testes manuais complementares quando necessário;
6. somente então aprovar e efetuar o commit no repositório.
