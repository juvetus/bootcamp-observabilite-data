FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système si nécessaire
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY app.py .

# Variables d'environnement par défaut (peuvent être overridées par docker-compose)
ENV DD_SERVICE=flask-demo-bootcamp
ENV DD_ENV=dev
ENV DD_VERSION=1.0
ENV DD_AGENT_HOST=dd-agent
ENV DD_TRACE_AGENT_PORT=8126
ENV DD_DOGSTATSD_PORT=8125
ENV DD_TRACE_ENABLED=true
ENV DD_LOGS_INJECTION=true
ENV DD_RUNTIME_METRICS_ENABLED=true
ENV DD_RUNTIME_METRICS_RUNTIME_ID_ENABLED=true
ENV DD_APM_ENABLED=true
ENV DD_PROFILING_ENABLED=true
ENV FLASK_APP=app.py

EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

CMD ["ddtrace-run", "python", "app.py"]
