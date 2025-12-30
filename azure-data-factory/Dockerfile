FROM python:3.11-slim

# Installer netcat pour le healthcheck
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY scripts/ ./scripts/
COPY data/input/ ./data/input/
COPY entrypoint.sh .

# Rendre le script exécutable
RUN chmod +x entrypoint.sh

# Créer le dossier de sortie
RUN mkdir -p data/output logs

# Variables d'environnement par défaut
ENV DD_AGENT_HOST=dd-agent \
    DD_STATSD_PORT=8125 \
    PIPELINE_NAME=docker-adf-pipeline \
    ENV=dev \
    DD_SITE=datadoghq.eu \
    DD_HOSTNAME=docker-pipeline \
    SIMULATE_ERROR=false \
    ERROR_TYPE=processing

# Commande par défaut
CMD ["./entrypoint.sh"]
