FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu "torch>=2.2,<3" \
    && pip install --no-cache-dir -r requirements.txt \
    && useradd --create-home --uid 1000 appuser

COPY p16_service ./p16_service
COPY artifacts ./artifacts
COPY deployment.json ./deployment.json

USER appuser
EXPOSE 7860
CMD ["sh", "-c", "uvicorn p16_service.app:app --host 0.0.0.0 --port ${PORT:-7860}"]
