import os
import logging
import time
import random
from flask import Flask, jsonify, request
from ddtrace import tracer
from ddtrace.runtime import RuntimeMetrics
from datadog import initialize, statsd

# Configuration logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Activation des métriques runtime
RuntimeMetrics.enable()

# Variables d'environnement
DD_SERVICE = os.getenv("DD_SERVICE", "flask-demo")
DD_ENV = os.getenv("DD_ENV", "dev")
DD_VERSION = os.getenv("DD_VERSION", "1.0")
DD_AGENT_HOST = os.getenv("DD_AGENT_HOST", "localhost")
DD_DOGSTATSD_PORT = int(os.getenv("DD_DOGSTATSD_PORT", "8125"))

# Initialisation Datadog
options = {
    'statsd_host': DD_AGENT_HOST,
    'statsd_port': DD_DOGSTATSD_PORT,
}

try:
    initialize(**options)
    logger.info(f"Datadog initialized: {DD_AGENT_HOST}:{DD_DOGSTATSD_PORT}")
except Exception as e:
    logger.error(f"Failed to initialize Datadog: {e}")

app = Flask(__name__)

# Compteur de requêtes
request_count = 0

@app.before_request
def before_request():
    """Middleware pour tracker les requêtes"""
    global request_count
    request_count += 1
    request.start_time = time.time()
    logger.info(f"[{DD_ENV}] Request {request_count}: {request.method} {request.path}")

@app.after_request
def after_request(response):
    """Middleware pour envoyer les métriques"""
    if hasattr(request, 'start_time'):
        duration = time.time() - request.start_time
        statsd.increment(
            'flask.request.count',
            tags=[
                f'env:{DD_ENV}',
                f'method:{request.method}',
                f'endpoint:{request.path}',
                f'status:{response.status_code}'
            ]
        )
        statsd.histogram(
            'flask.request.duration',
            duration,
            tags=[
                f'env:{DD_ENV}',
                f'method:{request.method}',
                f'endpoint:{request.path}'
            ]
        )
        logger.info(f"Request completed in {duration:.3f}s - Status: {response.status_code}")
    return response

@app.route("/")
@tracer.wrap(service=DD_SERVICE, resource="home")
def hello():
    """Endpoint principal"""
    logger.info("Home endpoint called")
    statsd.increment('flask.endpoint.home', tags=[f'env:{DD_ENV}'])
    return jsonify({
        "message": "Hello from Datadog APM",
        "service": DD_SERVICE,
        "environment": DD_ENV,
        "version": DD_VERSION,
        "request_count": request_count
    })

@app.route("/health")
def health():
    """Health check endpoint"""
    logger.debug("Health check")
    return jsonify({
        "status": "healthy",
        "service": DD_SERVICE,
        "environment": DD_ENV
    })

@app.route("/slow")
@tracer.wrap(service=DD_SERVICE, resource="slow_endpoint")
def slow():
    """Endpoint lent pour tester les performances"""
    delay = random.uniform(0.5, 2.0)
    logger.warning(f"Slow endpoint - sleeping for {delay:.2f}s")
    
    with tracer.trace("sleep.operation", service=DD_SERVICE):
        time.sleep(delay)
    
    statsd.increment('flask.endpoint.slow', tags=[f'env:{DD_ENV}'])
    statsd.histogram('flask.endpoint.slow.delay', delay, tags=[f'env:{DD_ENV}'])
    
    return jsonify({
        "message": "Slow endpoint",
        "delay_seconds": round(delay, 2)
    })

@app.route("/compute")
@tracer.wrap(service=DD_SERVICE, resource="compute")
def compute():
    """Endpoint avec calculs intensifs"""
    logger.info("Starting computation")
    
    with tracer.trace("computation.task", service=DD_SERVICE) as span:
        result = sum(i * i for i in range(10000))
        span.set_tag("computation.result", result)
    
    statsd.increment('flask.endpoint.compute', tags=[f'env:{DD_ENV}'])
    
    return jsonify({
        "message": "Computation complete",
        "result": result
    })

@app.route("/error")
@tracer.wrap(service=DD_SERVICE, resource="error_endpoint")
def error():
    """Endpoint qui génère une erreur pour tester le monitoring"""
    logger.error("Error endpoint called - generating ZeroDivisionError")
    statsd.increment('flask.endpoint.error', tags=[f'env:{DD_ENV}', 'error:zero_division'])
    
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        logger.exception("ZeroDivisionError occurred")
        statsd.increment('flask.error.count', tags=[f'env:{DD_ENV}', 'error_type:ZeroDivisionError'])
        return jsonify({
            "error": "Division by zero",
            "type": type(e).__name__
        }), 500

@app.route("/metrics")
def metrics():
    """Endpoint pour afficher les métriques custom"""
    return jsonify({
        "service": DD_SERVICE,
        "environment": DD_ENV,
        "version": DD_VERSION,
        "total_requests": request_count,
        "agent_host": DD_AGENT_HOST,
        "agent_port": DD_DOGSTATSD_PORT
    })

@app.errorhandler(404)
def not_found(error):
    """Handler pour les erreurs 404"""
    logger.warning(f"404 Not Found: {request.path}")
    statsd.increment('flask.error.404', tags=[f'env:{DD_ENV}'])
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handler pour les erreurs 500"""
    logger.error(f"500 Internal Server Error: {error}")
    statsd.increment('flask.error.500', tags=[f'env:{DD_ENV}'])
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    logger.info(f"Starting Flask app - Service: {DD_SERVICE}, Env: {DD_ENV}, Version: {DD_VERSION}")
    app.run(host="0.0.0.0", port=5000)
