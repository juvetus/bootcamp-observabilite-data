FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV DD_SERVICE=flask-demo-bootcamp
ENV DD_ENV=dev
ENV DD_VERSION=1.0
ENV DD_AGENT_HOST=dd-agent
ENV DD_TRACE_AGENT_PORT=8126
ENV DD_TRACE_ENABLED=true
ENV DD_LOGS_INJECTION=true
ENV DD_RUNTIME_METRICS_ENABLED=true
ENV DD_RUNTIME_METRICS_RUNTIME_ID_ENABLED=true
ENV DD_APM_ENABLED=true
ENV DD_PROFILING_ENABLED=true

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["ddtrace-run", "python", "app.py"]
