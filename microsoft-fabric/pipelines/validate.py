# pipelines/validate.py
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
SILVER_PATH = os.getenv("SILVER_PATH", "data/silver")
GOLD_PATH = os.getenv("GOLD_PATH", "data/gold")
PIPELINE_NAME = os.getenv("PIPELINE_NAME", "fabric-pipeline")
ENV = os.getenv("ENV", "dev")
TEMP_THRESHOLD = float(os.getenv("TEMP_THRESHOLD", "95"))

@tracer.wrap(service=PIPELINE_NAME, resource="validate")
def validate_data():
    try:
        start = datetime.now(UTC)
        logger.info(f"[{ENV}] Starting data validation from {SILVER_PATH}/trucks.parquet")
        
        # Lecture des données silver
        df = pd.read_parquet(f"{SILVER_PATH}/trucks.parquet")
        logger.info(f"Read {len(df)} records from Silver layer")
        
        # Validation : température moteur
        alerts = df[df["engine_temp"] > TEMP_THRESHOLD]
        logger.warning(f"Found {len(alerts)} alerts (engine_temp > {TEMP_THRESHOLD}°C)")
        
        # Sauvegarde des alertes
        if len(alerts) > 0:
            output_path = f"{GOLD_PATH}/alerts.parquet"
            alerts.to_parquet(output_path)
            logger.info(f"Saved alerts to {output_path}")
        
        # Métriques
        duration = (datetime.now(UTC) - start).total_seconds()
        send_metric("fabric.pipeline.alerts", len(alerts), tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.validate.success", 1, tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.validate.duration", duration, tags=[f"env:{ENV}"])
        send_metric("fabric.pipeline.validate.records", len(df), tags=[f"env:{ENV}"])
        
        # Taux d'alertes
        alert_rate = (len(alerts) / len(df)) * 100 if len(df) > 0 else 0
        send_metric("fabric.pipeline.alert_rate", alert_rate, tags=[f"env:{ENV}"])
        
        logger.info(f"Validation completed in {duration:.2f}s - Alert rate: {alert_rate:.2f}%")
        return True
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        send_metric("fabric.pipeline.validate.error", 1, tags=[f"env:{ENV}", "error:file_not_found"])
        raise
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        send_metric("fabric.pipeline.validate.error", 1, tags=[f"env:{ENV}", f"error:{type(e).__name__}"])
        raise

if __name__ == "__main__":
    validate_data()