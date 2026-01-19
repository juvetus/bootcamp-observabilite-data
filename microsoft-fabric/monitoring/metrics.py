import os
import logging
from datadog import initialize, statsd

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration Datadog
DD_AGENT_HOST = os.getenv("DD_AGENT_HOST", "localhost")
DD_DOGSTATSD_PORT = int(os.getenv("DD_DOGSTATSD_PORT", "8125"))

options = {
    'statsd_host': DD_AGENT_HOST,
    'statsd_port': DD_DOGSTATSD_PORT,
}

try:
    initialize(**options)
    logger.info(f"Datadog initialized: {DD_AGENT_HOST}:{DD_DOGSTATSD_PORT}")
except Exception as e:
    logger.error(f"Failed to initialize Datadog: {e}")

def send_metric(metric_name, value, tags=None):
    """
    Envoie une métrique à Datadog
    
    Args:
        metric_name (str): Nom de la métrique
        value (float): Valeur de la métrique
        tags (list): Tags associés à la métrique
    """
    try:
        if tags is None:
            tags = []
        
        statsd.gauge(metric_name, value, tags=tags)
        logger.debug(f"Metric sent: {metric_name}={value} tags={tags}")
    except Exception as e:
        logger.error(f"Failed to send metric {metric_name}: {e}")
