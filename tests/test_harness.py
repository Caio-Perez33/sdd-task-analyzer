"""Test Harness do TaskAnalyzer conforme os cenarios de aceite SDD."""

from datetime import datetime, timedelta, timezone

import pytest

from src.task_analyzer import TaskValidationError, analyze_tasks

UTC = timezone.utc
BASE = datetime(2025, 1, 1, 8, 0, tzinfo=UTC)


def make_task(
    task_id: int,
    *,
    priority: str = "media",
    status: str = "concluida",
    start_offset_minutes: int | None = 60,
    end_offset_minutes: int | None = 120,
    deadline_offset_minutes: int = 180,
) -> dict[str, object]:
    """Cria uma tarefa deterministica para os testes."""
    start = BASE + timedelta(minutes=start_offset_minutes) if start_offset_minutes is not None else None
    end = BASE + timedelta(minutes=end_offset_minutes) if end_offset_minutes is not None else None
    return {
        "id_tarefa": task_id,
        "data_criacao": BASE,
        "data_inicio": start,
        "data_conclusao": end,
        "prazo": BASE + timedelta(minutes=deadline_offset_minutes),
        "prioridade": priority,
        "status": status,
    }


def test_cenario_sucesso_calcula_metricas_gerais_e_por_prioridade() -> None:
    """Valida contadores, duracao media e taxa de atraso no total e por prioridade."""
    tarefas = [
        make_task(1, priority="alta", end_offset_minutes=180, deadline_offset_minutes=150),
        make_task(2, priority="baixa", end_offset_minutes=120, deadline_offset_minutes=180),
        make_task(3, priority="media", status="pendente", start_offset_minutes=None, end_offset_minutes=None),
        make_task(4, priority="media", status="cancelada", start_offset_minutes=None, end_offset_minutes=None),
    ]

    resultado = analyze_tasks(tarefas)

    assert resultado["total_tarefas"] == 4
    assert resultado["quantidade_tarefas"] == 4
    assert resultado["total_concluidas"] == 2
    assert resultado["total_pendentes"] == 1
    assert resultado["total_canceladas"] == 1
    assert resultado["tempo_medio_conclusao_min"] == 90.0
    assert resultado["tempo_medio_conclusao_horas"] == 1.5
    assert resultado["taxa_atraso_percentual"] == 50.0
    assert resultado["indicadores_por_prioridade"]["alta"]["taxa_atraso_percentual"] == 100.0
    assert resultado["indicadores_por_prioridade"]["baixa"]["tempo_medio_conclusao_min"] == 60.0
    assert resultado["indicadores_por_prioridade"]["media"]["total_concluidas"] == 0


def test_conclusao_anterior_a_criacao_dispara_erro() -> None:
    """Rejeita uma tarefa concluida antes da sua criacao."""
    tarefa = make_task(1, end_offset_minutes=-1)
    with pytest.raises(TaskValidationError, match="data_conclusao"):
        analyze_tasks([tarefa])


def test_lista_vazia_retorna_metricas_zero() -> None:
    """Trata a entrada vazia sem divisao por zero."""
    resultado = analyze_tasks([])
    assert resultado["total_tarefas"] == 0
    assert resultado["total_concluidas"] == 0
    assert resultado["tempo_medio_conclusao_min"] == 0.0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0
    assert set(resultado["indicadores_por_prioridade"]) == {"baixa", "media", "alta"}


def test_apenas_pendentes_retorna_medias_zero() -> None:
    """Uma lista sem tarefas concluidas possui media e atraso iguais a zero."""
    tarefas = [
        make_task(1, status="pendente", start_offset_minutes=None, end_offset_minutes=None),
        make_task(2, status="pendente", start_offset_minutes=None, end_offset_minutes=None),
    ]
    resultado = analyze_tasks(tarefas)
    assert resultado["total_pendentes"] == 2
    assert resultado["tempo_medio_conclusao_min"] == 0.0
    assert resultado["tempo_medio_conclusao_horas"] == 0.0
    assert resultado["taxa_atraso_percentual"] == 0.0


def test_status_invalido_dispara_erro() -> None:
    """Rejeita status nao previsto pelo contrato."""
    tarefa = make_task(1)
    tarefa["status"] = "em andamento"
    with pytest.raises(TaskValidationError, match="status"):
        analyze_tasks([tarefa])


def test_id_duplicado_dispara_erro() -> None:
    """Rejeita identificadores repetidos na mesma chamada."""
    with pytest.raises(TaskValidationError, match="duplicado"):
        analyze_tasks([make_task(7), make_task(7, priority="baixa")])


def test_tarefa_concluida_sem_datas_de_execucao_dispara_erro() -> None:
    """Exige inicio e conclusao quando o status e concluida."""
    tarefa = make_task(1, start_offset_minutes=None, end_offset_minutes=None)
    with pytest.raises(TaskValidationError, match="exigem data_inicio e data_conclusao"):
        analyze_tasks([tarefa])


def test_conclusao_anterior_ao_inicio_dispara_erro() -> None:
    """Rejeita duracao negativa mesmo quando a conclusao ocorre apos a criacao."""
    tarefa = make_task(1, start_offset_minutes=120, end_offset_minutes=90)
    with pytest.raises(TaskValidationError, match="anterior a data_inicio"):
        analyze_tasks([tarefa])
