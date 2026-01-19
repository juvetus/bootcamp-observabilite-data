FROM eclipse-temurin:11-jdk-jammy

# Installer Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier les scripts et données
COPY scripts/ ./scripts/
COPY data/ ./data/

# Créer le dossier de sortie
RUN mkdir -p output

# Variables d'environnement Spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["python3", "scripts/spark_job.py"]
