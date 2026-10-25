"""Analise de metricas de tarefas conforme o contrato SDD."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger(__name__)

PRIORIDADES: tuple[str, ...] = ("baixa", "media", "alta")
STATUS_VALIDOS: tuple[str, ...] = ("concluida", "pendente", "cancelada")


class TaskValidationError(ValueError):
    """Indica que uma tarefa nao respeita o contrato de entrada."""


def _datetime_utc(value: Any, campo: str, id_tarefa: Any) -> datetime | None:
    """Valida e converte uma data com fuso para UTC.

    Args:
        value: Valor a validar.
        campo: Nome do campo da tarefa.
        id_tarefa: Identificador usado para contextualizar a mensagem.

    Returns:
        Data normalizada em UTC ou None quando o valor e None.

    Raises:
        TaskValidationError: Se o valor nao for um datetime com fuso.
    """
    if value is None:
        return None
    if not isinstance(value, datetime):
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: campo '{campo}' deve ser um datetime com fuso horario."
        )
    if value.tzinfo is None or value.utcoffset() is None:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: campo '{campo}' deve informar o fuso horario UTC."
        )
    return value.astimezone(timezone.utc)


def _validar_tarefa(
    tarefa: Any, indice: int, ids_vistos: set[int]
) -> dict[str, Any]:
    """Valida os campos de uma tarefa e devolve valores normalizados."""
    if not isinstance(tarefa, dict):
        raise TaskValidationError(f"Tarefa na posicao {indice} deve ser um dicionario.")

    id_tarefa = tarefa.get("id_tarefa")
    if isinstance(id_tarefa, bool) or not isinstance(id_tarefa, int) or id_tarefa <= 0:
        raise TaskValidationError(
            f"Tarefa na posicao {indice}: 'id_tarefa' deve ser um inteiro positivo."
        )
    if id_tarefa in ids_vistos:
        raise TaskValidationError(f"ID de tarefa duplicado: {id_tarefa}.")
    ids_vistos.add(id_tarefa)

    prioridade = tarefa.get("prioridade")
    if prioridade not in PRIORIDADES:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: prioridade deve ser uma destas opcoes: {', '.join(PRIORIDADES)}."
        )

    status = tarefa.get("status")
    if status not in STATUS_VALIDOS:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: status deve ser uma destas opcoes: {', '.join(STATUS_VALIDOS)}."
        )

    if "data_criacao" not in tarefa or "prazo" not in tarefa:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: os campos 'data_criacao' e 'prazo' sao obrigatorios."
        )

    criada = _datetime_utc(tarefa.get("data_criacao"), "data_criacao", id_tarefa)
    prazo = _datetime_utc(tarefa.get("prazo"), "prazo", id_tarefa)
    inicio = _datetime_utc(tarefa.get("data_inicio"), "data_inicio", id_tarefa)
    conclusao = _datetime_utc(tarefa.get("data_conclusao"), "data_conclusao", id_tarefa)

    if criada is None or prazo is None:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: 'data_criacao' e 'prazo' nao podem ser nulos."
        )
    if inicio is not None and inicio < criada:
        raise TaskValidationError(
            f"Tarefa {id_tarefa}: data_inicio nao pode ser anterior a data_criacao."
        )
    if status == "concluida":
        if inicio is None or conclusao is None:
            raise TaskValidationError(
                f"Tarefa {id_tarefa}: tarefas concluidas exigem data_inicio e data_conclusao."
            )
        if conclusao < criada:
            raise TaskValidationError(
                f"Tarefa {id_tarefa}: data_conclusao nao pode ser anterior a data_criacao."
            )
        if conclusao < inicio:
            raise TaskValidationError(
                f"Tarefa {id_tarefa}: data_conclusao nao pode ser anterior a data_inicio."
            )

    return {
        "id_tarefa": id_tarefa,
        "data_criacao": criada,
        "data_inicio": inicio,
        "data_conclusao": conclusao,
        "prazo": prazo,
        "prioridade": prioridade,
        "status": status,
    }


def _calcular_metricas(tarefas: list[dict[str, Any]]) -> dict[str, Any]:
    """Calcula contadores e metricas para um conjunto de tarefas validado."""
    total = len(tarefas)
    concluidas = [t for t in tarefas if t["status"] == "concluida"]
    pendentes = sum(t["status"] == "pendente" for t in tarefas)
    canceladas = sum(t["status"] == "cancelada" for t in tarefas)

    duracoes_min = [
        (t["data_conclusao"] - t["data_inicio"]).total_seconds() / 60.0
        for t in concluidas
    ]
    atrasadas = sum(t["data_conclusao"] > t["prazo"] for t in concluidas)
    media_min = round(sum(duracoes_min) / len(duracoes_min), 2) if duracoes_min else 0.0
    taxa_atraso = round((atrasadas / len(concluidas)) * 100.0, 2) if concluidas else 0.0

    return {
        "total_tarefas": total,
        "quantidade_tarefas": total,
        "total_concluidas": len(concluidas),
        "total_pendentes": pendentes,
        "total_canceladas": canceladas,
        "tempo_medio_conclusao_min": media_min,
        "tempo_medio_conclusao_horas": round(media_min / 60.0, 2),
        "taxa_atraso_percentual": taxa_atraso,
    }


def analyze_tasks(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    """Valida tarefas e retorna metricas gerais e agrupadas por prioridade.

    Args:
        tasks: Lista de dicionarios conforme `specs/task_analyzer_spec.md`.

    Returns:
        Dicionario com contadores e metricas gerais e por prioridade.

    Raises:
        TaskValidationError: Se a entrada ou uma tarefa violar o contrato.
    """
    if not isinstance(tasks, list):
        raise TaskValidationError("A entrada 'tasks' deve ser uma lista.")

    ids_vistos: set[int] = set()
    tarefas_validadas = [
        _validar_tarefa(tarefa, indice, ids_vistos)
        for indice, tarefa in enumerate(tasks)
    ]
    metricas_gerais = _calcular_metricas(tarefas_validadas)
    indicadores_por_prioridade: dict[str, dict[str, Any]] = {}

    for prioridade in PRIORIDADES:
        grupo = [t for t in tarefas_validadas if t["prioridade"] == prioridade]
        indicadores_por_prioridade[prioridade] = _calcular_metricas(grupo)

    resultado: dict[str, Any] = {
        **metricas_gerais,
        "indicadores_por_prioridade": indicadores_por_prioridade,
    }
    logger.info(
        "task_analysis_completed",
        extra={"total_tarefas": len(tarefas_validadas), "total_concluidas": metricas_gerais["total_concluidas"]},
    )
    return resultado
