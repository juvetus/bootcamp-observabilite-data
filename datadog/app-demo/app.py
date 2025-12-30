from ddtrace import tracer
from ddtrace.runtime import RuntimeMetrics
RuntimeMetrics.enable()

from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello from Datadog APM"

@app.route("/slow")
def slow():
    time.sleep(1)
    return "Slow endpoint"

@app.route("/error")
def error():
    return 1 / 0

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
