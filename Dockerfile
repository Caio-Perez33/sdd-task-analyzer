FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt \
    && adduser --disabled-password --gecos "" --uid 10001 appuser \
    && chown appuser:appuser /app

COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser tests/ ./tests/
COPY --chown=appuser:appuser specs/ ./specs/
COPY --chown=appuser:appuser CONTEXT_RULES.md README.md ./

USER appuser

CMD ["python", "-m", "pytest", "-p", "no:cacheprovider", "tests/test_harness.py", "-v"]
