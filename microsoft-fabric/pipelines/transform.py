# pipelines/transform.py
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
BRONZE_PATH = os.getenv("BRONZE_PATH", "data/bronze")
SILVER_PATH = os.getenv("SILVER_PATH", "data/silver")
PIPELINE_NAME = os.getenv("PIPELINE_NAME", "fabric-pipeline")
ENV = os.getenv("ENV", "dev")

@tracer.wrap(service=PIPELINE_NAME, resource="transform")
def transform_data():
    try:
        start = datetime.now(UTC)
        logger.info(f"[{ENV}] Starting data transformation from {BRONZE_PATH}/trucks.parquet")
        
        # Lecture des données bronze
        df = pd.read_parquet(f"{BRONZE_PATH}/trucks.parquet")
        logger.info(f"Read {len(df)} records from Bronze layer")
        
        # Transformations
        df["speed_kmh"] = df["speed"].astype(float)
        df["processed_at"] = datetime.now(UTC).isoformat()
        logger.info("Applied transformations: speed conversion, timestamp")
        
        # Sauvegarde en Silver
        output_path = f"{SILVER_PATH}/trucks.parquet"
        df.to_parquet(output_path)
        logger.info(f"Saved transformed data to {output_path}")
        
        # Métriques
        duration = (datetime.now(UTC) - start).total_seconds()
        send_metric("fabric.pipeline.transform.duration", duration, tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.transform.records", len(df), tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.transform.success", 1, tags=[f"env:{ENV}"])
        
        logger.info(f"Transformation completed in {duration:.2f}s")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        send_metric("fabric.pipeline.transform.error", 1, tags=[f"env:{ENV}", "error:file_not_found"])
        raise
    except Exception as e:
        logger.error(f"Transformation failed: {e}")
        send_metric("fabric.pipeline.transform.error", 1, tags=[f"env:{ENV}", f"error:{type(e).__name__}"])
        raise

if __name__ == "__main__":
    transform_data()
