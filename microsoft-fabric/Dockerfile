FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie des requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY pipelines/ ./pipelines/
COPY monitoring/ ./monitoring/

# Création des dossiers de données
RUN mkdir -p data/raw data/bronze data/silver data/gold

CMD ["python", "-m", "ddtrace-run", "pipelines/ingest.py"]
