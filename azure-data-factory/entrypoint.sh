#!/bin/bash

# Attendre que l'agent Datadog soit prêt
echo "Waiting for Datadog agent to be ready..."

# L'agent utilise UDP pour StatsD (8125), on ne peut pas le tester avec nc -z
# On attend simplement que le conteneur soit démarré
counter=0
max_wait=15

while [ $counter -lt $max_wait ]; do
    # Vérifier si l'agent répond (via health check ou simple ping)
    if docker-compose ps dd-agent 2>/dev/null | grep -q "healthy" || nc -z $DD_AGENT_HOST 8126 2>/dev/null; then
        echo "✅ Datadog agent is ready (${counter}s)"
        break
    fi
    sleep 1
    counter=$((counter + 1))
done

if [ $counter -ge $max_wait ]; then
    echo "⚠️  Note: Could not verify Datadog agent connection after ${max_wait}s"
    echo "Pipeline will continue. Metrics and logs will be sent to Datadog API."
fi

# Lancer le pipeline
echo "Starting pipeline..."
python scripts/transform.py
