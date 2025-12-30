import csv
import time
import logging
import os
import json
import requests
import uuid
from datetime import datetime, timezone
from datadog import statsd
from dotenv import load_dotenv

load_dotenv()

PIPELINE_NAME = os.getenv("PIPELINE_NAME", "unknown-pipeline")
DD_API_KEY = os.getenv("DD_API_KEY", "")
DD_SITE = os.getenv("DD_SITE", "datadoghq.eu")
SIMULATE_ERROR = os.getenv("SIMULATE_ERROR", "false").lower() == "true"
ERROR_TYPE = os.getenv("ERROR_TYPE", "processing")  # processing, validation, connection

# Générer un ID unique pour cette exécution
EXECUTION_ID = str(uuid.uuid4())[:8]  # 8 premiers caractères pour lisibilité

# Custom handler pour envoyer les logs à Datadog
class DatadogLogHandler(logging.Handler):
    def __init__(self, api_key, site="datadoghq.eu", service="adf-pipeline", execution_id=None):
        super().__init__()
        self.api_key = api_key
        self.url = f"https://http-intake.logs.{site}/api/v2/logs"
        self.service = service
        self.hostname = os.getenv("DD_HOSTNAME", "local-host")
        self.execution_id = execution_id
        
    def emit(self, record):
        if not self.api_key:
            return
            
        log_entry = {
            "ddsource": "python",
            "ddtags": f"env:dev,service:{self.service},pipeline:{PIPELINE_NAME},execution_id:{self.execution_id}",
            "hostname": self.hostname,
            "message": self.format(record),
            "service": self.service,
            "status": record.levelname.lower(),
            "timestamp": int(record.created * 1000),
            # Attributs personnalisés pour faciliter la corrélation
            "execution_id": self.execution_id,
            "pipeline": PIPELINE_NAME,
            "environment": "dev"
        }
        
        try:
            headers = {
                "DD-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }
            requests.post(self.url, json=[log_entry], headers=headers, timeout=5)
        except Exception:
            pass  # Ne pas interrompre le pipeline si l'envoi de log échoue

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s | %(levelname)s | [exec:{EXECUTION_ID}] | %(message)s"
)

# Ajouter le handler Datadog si l'API key est configurée
if DD_API_KEY:
    dd_handler = DatadogLogHandler(DD_API_KEY, DD_SITE, "adf-pipeline", EXECUTION_ID)
    dd_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    logging.getLogger().addHandler(dd_handler)
    logging.info(f"Datadog log handler configured | execution_id: {EXECUTION_ID}")

start_time = time.time()
records = 0
errors = 0
event_types = {}  # Compteur par type d'événement
processing_times = []  # Temps de traitement par record

# Tags communs pour toutes les métriques
COMMON_TAGS = [f"pipeline:{PIPELINE_NAME}", f"execution_id:{EXECUTION_ID}", "env:dev"]

try:
    logging.info(f"Pipeline {PIPELINE_NAME} started")
    
    # Métrique: Démarrage du pipeline
    statsd.increment("pipeline.started", tags=COMMON_TAGS)
    
    if SIMULATE_ERROR:
        logging.warning(f"⚠️ SIMULATION MODE: Error type '{ERROR_TYPE}' will be triggered")

    # Simulation d'erreur de connexion
    if SIMULATE_ERROR and ERROR_TYPE == "connection":
        logging.error("Connection to data source failed: Timeout after 30s")
        statsd.increment("pipeline.connection_error", tags=COMMON_TAGS)
        raise ConnectionError("Failed to connect to Azure Blob Storage")

    with open("data/input/events.csv") as infile, open("data/output/events_processed.csv", "w", newline="") as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["processed_at", "pipeline"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            record_start = time.time()
            records += 1
            
            # Simulation d'erreur de validation
            if SIMULATE_ERROR and ERROR_TYPE == "validation" and records == 10:
                logging.error(f"Validation error at record {records}: Invalid event_type '{row['event_type']}'")
                errors += 1
                statsd.increment("pipeline.validation_error", tags=COMMON_TAGS + [f"event_type:{row.get('event_type', 'unknown')}"])
                continue
            
            # Simulation d'erreur de processing
            if SIMULATE_ERROR and ERROR_TYPE == "processing" and records == 30:
                logging.error(f"Processing error at record {records}: Failed to parse timestamp")
                statsd.increment("pipeline.processing_error", tags=COMMON_TAGS)
                raise ValueError(f"Cannot process record {records}: Invalid timestamp format")
            
            # Compter les types d'événements
            event_type = row.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            row["processed_at"] = datetime.now(timezone.utc).isoformat()
            row["pipeline"] = PIPELINE_NAME
            writer.writerow(row)
            
            # Mesurer le temps de traitement de ce record
            record_duration = time.time() - record_start
            processing_times.append(record_duration)
            
            # Envoyer la métrique de temps de traitement
            statsd.timing("pipeline.record_processing_time", record_duration * 1000, tags=COMMON_TAGS)

    duration = time.time() - start_time
    records_success = records - errors

    # Calcul des statistiques de traitement
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0
    max_processing_time = max(processing_times) if processing_times else 0
    min_processing_time = min(processing_times) if processing_times else 0

    # Métriques globales du pipeline
    statsd.gauge("pipeline.records_processed", records, tags=COMMON_TAGS)
    statsd.gauge("pipeline.records_success", records_success, tags=COMMON_TAGS)
    statsd.gauge("pipeline.records_errors", errors, tags=COMMON_TAGS)
    statsd.gauge("pipeline.duration_seconds", duration, tags=COMMON_TAGS)
    
    # Métriques de performance
    statsd.gauge("pipeline.throughput_records_per_second", records / duration if duration > 0 else 0, tags=COMMON_TAGS)
    statsd.gauge("pipeline.avg_record_processing_time_ms", avg_processing_time * 1000, tags=COMMON_TAGS)
    statsd.gauge("pipeline.max_record_processing_time_ms", max_processing_time * 1000, tags=COMMON_TAGS)
    statsd.gauge("pipeline.min_record_processing_time_ms", min_processing_time * 1000, tags=COMMON_TAGS)
    
    # Métriques de qualité
    error_rate = (errors / records * 100) if records > 0 else 0
    success_rate = 100 - error_rate
    statsd.gauge("pipeline.error_rate_percent", error_rate, tags=COMMON_TAGS)
    statsd.gauge("pipeline.success_rate_percent", success_rate, tags=COMMON_TAGS)
    
    # Métriques par type d'événement
    for event_type, count in event_types.items():
        statsd.gauge("pipeline.events_by_type", count, tags=COMMON_TAGS + [f"event_type:{event_type}"])
        logging.info(f"  → {event_type}: {count} events")
    
    statsd.increment("pipeline.success", tags=COMMON_TAGS)

    if errors > 0:
        logging.warning(f"Pipeline finished with warnings ({records} records, {errors} errors, {duration:.2f}s)")
        logging.warning(f"Error rate: {error_rate:.2f}%")
    else:
        logging.info(f"Pipeline finished successfully ({records} records, {duration:.2f}s)")
    
    logging.info(f"Throughput: {records/duration:.2f} records/sec")
    logging.info(f"Avg processing time: {avg_processing_time*1000:.2f}ms per record")
    logging.info(f"Output file: data/output/events_processed.csv")

except Exception as e:
    duration = time.time() - start_time
    error_type_name = type(e).__name__
    
    # Métriques d'erreur enrichies
    statsd.increment("pipeline.error", tags=COMMON_TAGS + [f"error_type:{error_type_name}"])
    statsd.gauge("pipeline.duration_seconds", duration, tags=COMMON_TAGS)
    statsd.gauge("pipeline.records_before_failure", records, tags=COMMON_TAGS)
    
    # Taux de complétion avant échec
    completion_rate = (records / 60 * 100) if records > 0 else 0  # Assume 60 records total
    statsd.gauge("pipeline.completion_rate_percent", completion_rate, tags=COMMON_TAGS)
    
    logging.error(f"Pipeline failed after {duration:.2f}s: {str(e)}", exc_info=True)
    logging.error(f"Records processed before failure: {records} ({completion_rate:.1f}% complete)")
    logging.error(f"Error type: {error_type_name}")
    raise 
