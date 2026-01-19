# pipelines/ingest.py
import os
import logging
import pandas as pd
from datetime import datetime, UTC
from ddtrace import tracer
from monitoring.metrics import send_metric

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables d'environnement
RAW_PATH = os.getenv("RAW_PATH", "data/raw")
BRONZE_PATH = os.getenv("BRONZE_PATH", "data/bronze")
PIPELINE_NAME = os.getenv("PIPELINE_NAME", "fabric-pipeline")
ENV = os.getenv("ENV", "dev")

@tracer.wrap(service=PIPELINE_NAME, resource="ingest")
def ingest_data():
    try:
        start = datetime.now(UTC)
        logger.info(f"[{ENV}] Starting data ingestion from {RAW_PATH}/trucks.csv")
        
        # Lecture des données brutes
        df = pd.read_csv(f"{RAW_PATH}/trucks.csv")
        logger.info(f"Read {len(df)} records from CSV")
        
        # Sauvegarde en format Parquet
        output_path = f"{BRONZE_PATH}/trucks.parquet"
        df.to_parquet(output_path)
        logger.info(f"Saved data to {output_path}")
        
        # Métriques
        duration = (datetime.now(UTC) - start).total_seconds()
        send_metric("fabric.pipeline.ingest.success", 1, tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.ingest.records", len(df), tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.ingest.duration", duration, tags=[f"env:{ENV}"])
        
        logger.info(f"Ingestion completed in {duration:.2f}s")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        send_metric("fabric.pipeline.ingest.error", 1, tags=[f"env:{ENV}", "error:file_not_found"])
        raise
    except Exception as e:
        logger.error(f"Ingestion failed: {e}")
        send_metric("fabric.pipeline.ingest.error", 1, tags=[f"env:{ENV}", f"error:{type(e).__name__}"])
        raise

if __name__ == "__main__":
    ingest_data()
