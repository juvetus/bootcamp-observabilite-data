#  Microsoft Fabric Local – Pipeline Data avec Observabilité Datadog

---

##  Résumé Exécutif

Ce document présente la mise en place d'un pipeline de données simulant l'architecture medallion de Microsoft Fabric (Bronze → Silver → Gold) avec une observabilité complète via Datadog.

**Ce qui a été réalisé :**

1. **Pipeline de données en 3 étapes** 
   - **Ingestion (Raw → Bronze)** : Lecture CSV et conversion Parquet
   - **Transformation (Bronze → Silver)** : Enrichissement et nettoyage des données
   - **Validation (Silver → Gold)** : Détection d'alertes et quality checks

2. **Observabilité complète avec Datadog** 
   - Traces APM pour chaque étape du pipeline
   - Métriques custom (durée, nombre d'enregistrements, taux d'alertes)
   - Logs structurés avec contexte
   - Corrélation traces ↔ logs ↔ métriques

3. **Architecture medallion locale** 
   - Simulation de l'architecture Microsoft Fabric
   - 4 couches de données (Raw/Bronze/Silver/Gold)
   - Pipeline orchestré via Docker Compose
   - Variables d'environnement pour configuration

**Bénéfices :**
- Visibilité complète sur le pipeline de données
- Détection rapide des anomalies (température moteur)
- Métriques pour optimisation des performances
- Architecture évolutive vers un vrai Microsoft Fabric

---

##  Objectifs

- Simuler un pipeline de données Microsoft Fabric en local
- Implémenter l'architecture medallion (Bronze/Silver/Gold)
- Instrumenter le pipeline avec Datadog (APM, Metrics, Logs)
- Détecter des alertes métier (température moteur excessive)
- Préparer une base pour migration vers Microsoft Fabric cloud

---

##  Architecture

### Architecture medallion

```
Raw Layer (CSV)
    ↓
Bronze Layer (Parquet brut)
    ↓
Silver Layer (Parquet transformé)
    ↓
Gold Layer (Alertes et analytics)
```

### Flux de données

```
trucks.csv (Raw)
    → ingest.py → trucks.parquet (Bronze)
    → transform.py → trucks.parquet (Silver)
    → validate.py → alerts.parquet (Gold)
```

### Infrastructure

```
┌─────────────────┐
│   dd-agent      │  Agent Datadog (APM, StatsD, Logs)
│   Port 8126/8125│
└────────┬────────┘
         │
┌────────▼────────┐
│  fabric-sim     │  Pipeline Python
│  - ingest.py    │  - Traces APM
│  - transform.py │  - Métriques custom
│  - validate.py  │  - Logs structurés
└─────────────────┘
```

---

##  Structure du projet

```
microsoft-fabric/
├── data/
│   ├── raw/                    # Données sources (CSV)
│   │   └── trucks.csv
│   ├── bronze/                 # Parquet brut
│   │   └── trucks.parquet
│   ├── silver/                 # Parquet transformé
│   │   └── trucks.parquet
│   └── gold/                   # Alertes et analytics
│       └── alerts.parquet
│
├── pipelines/
│   ├── ingest.py              # Raw → Bronze
│   ├── transform.py           # Bronze → Silver
│   └── validate.py            # Silver → Gold
│
├── monitoring/
│   └── metrics.py             # Client Datadog StatsD
│
├── docker-compose.yaml        # Orchestration
├── Dockerfile                 # Image Python
├── requirements.txt           # Dépendances
└── .env.example              # Template configuration
```

---

##  Pipelines Python

### 1. Ingestion (ingest.py)

**Objectif** : Charger les données brutes CSV et les convertir en Parquet (Bronze layer)

**Fonctionnalités** :
- Lecture du fichier `trucks.csv`
- Conversion en format Parquet
- Comptage des enregistrements
- Envoi de métriques : durée, nombre de records, succès/erreur
- Traces APM avec span `ingest`

**Métriques envoyées** :
- `fabric.pipeline.ingest.success` (counter)
- `fabric.pipeline.ingest.records` (gauge)
- `fabric.pipeline.ingest.duration` (histogram)
- `fabric.pipeline.ingest.error` (counter en cas d'erreur)

**Variables d'environnement utilisées** :
- `RAW_PATH` : Chemin des données raw
- `BRONZE_PATH` : Chemin de sortie bronze
- `PIPELINE_NAME` : Nom du service pour APM
- `ENV` : Environnement (dev/prod)

### 2. Transformation (transform.py)

**Objectif** : Enrichir et nettoyer les données Bronze → Silver

**Transformations appliquées** :
- Conversion de vitesse en km/h
- Ajout du timestamp de traitement
- Nettoyage des données invalides (optionnel)
- Standardisation des colonnes

**Métriques envoyées** :
- `fabric.pipeline.transform.duration` (histogram)
- `fabric.pipeline.transform.records` (gauge)
- `fabric.pipeline.transform.success` (counter)
- `fabric.pipeline.transform.error` (counter)

**Variables d'environnement utilisées** :
- `BRONZE_PATH` : Source des données
- `SILVER_PATH` : Destination transformée
- `PIPELINE_NAME` : Service APM
- `ENV` : Environnement

### 3. Validation (validate.py)

**Objectif** : Détecter les alertes et valider la qualité des données

**Validations** :
- Détection température moteur > seuil (`TEMP_THRESHOLD`)
- Identification des camions en surchauffe
- Calcul du taux d'alertes
- Sauvegarde des alertes dans Gold layer

**Métriques envoyées** :
- `fabric.pipeline.alerts` (gauge) - Nombre d'alertes
- `fabric.pipeline.alert_rate` (gauge) - Pourcentage
- `fabric.pipeline.validate.duration` (histogram)
- `fabric.pipeline.validate.records` (gauge)
- `fabric.pipeline.validate.success` (counter)

**Variables d'environnement utilisées** :
- `SILVER_PATH` : Source des données validées
- `GOLD_PATH` : Destination des alertes
- `TEMP_THRESHOLD` : Seuil de température (défaut: 95°C)
- `PIPELINE_NAME` : Service APM
- `ENV` : Environnement

---

##  Monitoring avec Datadog

### Module metrics.py

Client StatsD pour envoyer des métriques custom à Datadog.

**Fonctionnalités** :
- Initialisation automatique du client StatsD
- Fonction `send_metric()` avec support des tags
- Logging des métriques envoyées
- Gestion d'erreurs robuste

**Configuration** :
```python
DD_AGENT_HOST = os.getenv("DD_AGENT_HOST", "localhost")
DD_DOGSTATSD_PORT = int(os.getenv("DD_DOGSTATSD_PORT", "8125"))
```

**Usage** :
```python
from monitoring.metrics import send_metric

send_metric("fabric.pipeline.records", 1000, tags=["env:dev", "layer:bronze"])
```

### Traces APM

Chaque pipeline utilise le décorateur `@tracer.wrap()` :

```python
@tracer.wrap(service=PIPELINE_NAME, resource="ingest")
def ingest_data():
    # Code tracé automatiquement
```

**Spans custom** pour opérations spécifiques :
```python
with tracer.trace("computation.task", service=DD_SERVICE) as span:
    result = heavy_computation()
    span.set_tag("result", result)
```

### Logs structurés

Configuration logging Python :
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

**Injection automatique du trace_id** via `DD_LOGS_INJECTION=true`

---

##  Configuration Docker

### docker-compose.yaml

```yaml
version: "3.8"

services:
  dd-agent:
    image: datadog/agent:latest
    container_name: dd-agent
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=${DD_SITE:-datadoghq.eu}
      - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
      - DD_APM_ENABLED=true
      - DD_APM_NON_LOCAL_TRAFFIC=true
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    ports:
      - "8126:8126"  # APM
      - "8125:8125/udp"  # StatsD
    networks:
      - fabric-network

  fabric-sim:
    build: .
    command: >
      sh -c "python pipelines/ingest.py &&
             python pipelines/transform.py &&
             python pipelines/validate.py"
    container_name: fabric-sim
    environment:
      - DD_SERVICE=${PIPELINE_NAME:-docker-fabric-pipeline}
      - DD_ENV=${ENV:-dev}
      - DD_VERSION=1.0.0
      - DD_AGENT_HOST=dd-agent
      - DD_TRACE_AGENT_PORT=8126
      - DD_DOGSTATSD_PORT=8125
      - PIPELINE_NAME=${PIPELINE_NAME:-docker-fabric-pipeline}
      - ENV=${ENV:-dev}
      - RAW_PATH=/app/data/raw
      - BRONZE_PATH=/app/data/bronze
      - SILVER_PATH=/app/data/silver
      - GOLD_PATH=/app/data/gold
      - TEMP_THRESHOLD=95
    volumes:
      - ./data:/app/data
      - ./pipelines:/app/pipelines
      - ./monitoring:/app/monitoring
    depends_on:
      - dd-agent
    networks:
      - fabric-network

networks:
  fabric-network:
    driver: bridge
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installation gcc pour compilation des dépendances
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code
COPY pipelines/ ./pipelines/
COPY monitoring/ ./monitoring/

# Création des dossiers de données
RUN mkdir -p data/raw data/bronze data/silver data/gold

CMD ["python", "-m", "ddtrace-run", "pipelines/ingest.py"]
```

### requirements.txt

```txt
pandas==2.1.4
pyarrow==14.0.2
ddtrace==2.5.0
datadog==0.49.1
```

### Variables d'environnement (.env)

```env
DD_API_KEY=votre_cle_api_datadog
DD_SITE=datadoghq.eu
PIPELINE_NAME=docker-fabric-pipeline
ENV=dev
TEMP_THRESHOLD=95
```

---

##  Démarrage du projet

### 1. Préparation

```bash
cd microsoft-fabric

# Copier le template des variables d'environnement
cp .env.example .env

# Éditer .env avec votre clé API Datadog
nano .env
```

### 2. Préparer les données

Créer un fichier `data/raw/trucks.csv` avec la structure :

```csv
truck_id,driver,speed,engine_temp,location,timestamp
T001,John,80,92,Paris,2026-01-19T10:00:00
T002,Sarah,95,98,Lyon,2026-01-19T10:05:00
T003,Mike,70,85,Marseille,2026-01-19T10:10:00
```

### 3. Lancement

```bash
# Build et démarrage
docker-compose up --build

# Ou en arrière-plan
docker-compose up -d --build

# Voir les logs
docker-compose logs -f fabric-sim

# Vérifier l'agent Datadog
docker exec -it dd-agent agent status
```

### 4. Vérification des résultats

```bash
# Vérifier les fichiers générés
ls -lh data/bronze/
ls -lh data/silver/
ls -lh data/gold/

# Inspecter les données
docker exec -it fabric-sim python -c "
import pandas as pd
df = pd.read_parquet('/app/data/gold/alerts.parquet')
print(df)
"
```

---

##  Métriques collectées

### Métriques pipeline

| Métrique | Type | Description | Tags |
|----------|------|-------------|------|
| `fabric.pipeline.ingest.success` | Counter | Succès de l'ingestion | env |
| `fabric.pipeline.ingest.records` | Gauge | Nombre d'enregistrements ingérés | env |
| `fabric.pipeline.ingest.duration` | Histogram | Durée de l'ingestion (s) | env |
| `fabric.pipeline.ingest.error` | Counter | Erreurs d'ingestion | env, error |
| `fabric.pipeline.transform.duration` | Histogram | Durée de transformation (s) | env |
| `fabric.pipeline.transform.records` | Gauge | Records transformés | env |
| `fabric.pipeline.transform.success` | Counter | Succès transformation | env |
| `fabric.pipeline.transform.error` | Counter | Erreurs transformation | env, error |
| `fabric.pipeline.alerts` | Gauge | Nombre d'alertes détectées | env |
| `fabric.pipeline.alert_rate` | Gauge | Taux d'alertes (%) | env |
| `fabric.pipeline.validate.duration` | Histogram | Durée validation (s) | env |
| `fabric.pipeline.validate.records` | Gauge | Records validés | env |
| `fabric.pipeline.validate.success` | Counter | Succès validation | env |
| `fabric.pipeline.validate.error` | Counter | Erreurs validation | env, error |

### Traces APM

**Services** :
- `docker-fabric-pipeline` (ou valeur de `PIPELINE_NAME`)

**Resources** :
- `ingest` - Pipeline d'ingestion
- `transform` - Pipeline de transformation
- `validate` - Pipeline de validation

**Spans custom** :
- Opérations de lecture fichier
- Transformations spécifiques
- Calculs d'alertes

---

##  Dashboard Datadog recommandé

### Widgets suggérés

#### 1. Pipeline Execution Time
- Métrique : `fabric.pipeline.*.duration` (p95)
- Visualisation : Timeseries
- Group by : `pipeline_step`

#### 2. Records Processed
- Métriques : 
  - `fabric.pipeline.ingest.records`
  - `fabric.pipeline.transform.records`
  - `fabric.pipeline.validate.records`
- Visualisation : Query Value

#### 3. Alert Rate
- Métrique : `fabric.pipeline.alert_rate`
- Visualisation : Timeseries avec threshold
- Threshold : warning > 5%, critical > 10%

#### 4. Pipeline Success Rate
- Métriques : 
  - `fabric.pipeline.*.success`
  - `fabric.pipeline.*.error`
- Formula : `(success / (success + error)) * 100`
- Visualisation : Query Value avec gauge

#### 5. APM Service Map
- Source : APM
- Service : `docker-fabric-pipeline`
- Visualisation : Service Map

#### 6. Error Logs
- Source : Logs
- Query : `status:error service:docker-fabric-pipeline`
- Visualisation : Log Stream

---

##  Monitors et Alertes

### 1. Monitor : High Alert Rate

**Objectif** : Alerter si trop de camions en surchauffe

```
Metric: fabric.pipeline.alert_rate
Condition: > 10% for 15 minutes
Alert message: "Alert rate is {{value}}% - Too many overheating trucks"
Tags: env:{{env.name}}
```

### 2. Monitor : Pipeline Failure

**Objectif** : Détecter les échecs du pipeline

```
Metric: fabric.pipeline.*.error
Condition: sum > 0 for 5 minutes
Alert message: "Pipeline {{pipeline_step.name}} failed"
```

### 3. Monitor : High Processing Time

**Objectif** : Détecter les ralentissements

```
Metric: fabric.pipeline.*.duration (p95)
Condition: > 30 seconds for 10 minutes
Alert message: "Pipeline {{pipeline_step.name}} is slow: {{value}}s"
```

### 4. Monitor : No Data Ingested

**Objectif** : Détecter l'absence de données

```
Metric: fabric.pipeline.ingest.records
Condition: no data for 1 hour
Alert message: "No data ingested in the last hour"
```

---

##  Tests et validation

### Test 1 : Pipeline nominal

```bash
# Lancer le pipeline
docker-compose up

# Vérifier les métriques dans Datadog
# - fabric.pipeline.ingest.success = 1
# - fabric.pipeline.transform.success = 1
# - fabric.pipeline.validate.success = 1
```

### Test 2 : Détection d'alertes

```bash
# Modifier trucks.csv pour ajouter des températures > 95°C
echo "T999,Test,100,105,Test,2026-01-19T12:00:00" >> data/raw/trucks.csv

# Relancer le pipeline
docker-compose restart fabric-sim

# Vérifier dans Datadog
# - fabric.pipeline.alerts > 0
# - fabric.pipeline.alert_rate > 0%
# - gold/alerts.parquet contient la ligne
```

### Test 3 : Gestion d'erreurs

```bash
# Supprimer le fichier source
rm data/raw/trucks.csv

# Relancer
docker-compose restart fabric-sim

# Vérifier
# - fabric.pipeline.ingest.error = 1
# - Logs d'erreur visibles dans Datadog
# - Trace avec status error
```

---

##  Résultats et livrables

###  Pipeline fonctionnel
- [x] Architecture medallion implémentée (Bronze/Silver/Gold)
- [x] 3 étapes de traitement instrumentées
- [x] Variables d'environnement configurables
- [x] Gestion d'erreurs robuste

###  Observabilité complète
- [x] Traces APM pour chaque étape
- [x] 14 métriques custom avec tags
- [x] Logs structurés avec contexte
- [x] Corrélation traces ↔ logs via trace_id

###  Infrastructure Docker
- [x] Agent Datadog conteneurisé
- [x] Docker Compose multi-services
- [x] Réseau dédié pour isolation
- [x] Volumes pour persistance des données

###  Monitoring opérationnel
- [x] Dashboard recommandé (6 widgets)
- [x] 4 monitors configurés
- [x] Alertes avec contexte
- [x] Tests de validation

###  Livrables
```
microsoft-fabric/
├── pipelines/        # 3 scripts Python instrumentés
├── monitoring/       # Client Datadog StatsD
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
├── .env.example
└── note.md          # Documentation complète
```

---

##  Apprentissages clés

### Concepts Microsoft Fabric

#### Architecture medallion
- **Bronze** : Données brutes, format Parquet, pas de transformation
- **Silver** : Données nettoyées, enrichies, prêtes pour analytics
- **Gold** : Agrégations, alertes, métriques métier
- **Raw** : Données sources (CSV, JSON, etc.)

#### Avantages
- Traçabilité complète (raw → gold)
- Rollback facile en cas d'erreur
- Séparation des responsabilités
- Optimisation du stockage (Parquet)

### Observabilité data pipeline

#### Métriques importantes
- **Volumétrie** : Nombre d'enregistrements par couche
- **Performance** : Durée de chaque étape
- **Qualité** : Taux d'alertes, données invalides
- **Fiabilité** : Succès/échec, taux d'erreur

#### Patterns appliqués
```python
# Pattern : Mesure de volumétrie
df = pd.read_csv(source)
send_metric("records", len(df), tags=["layer:bronze"])

# Pattern : Mesure de performance
start = time.time()
process_data(df)
duration = time.time() - start
send_metric("duration", duration, tags=["step:transform"])

# Pattern : Détection d'anomalies
alerts = df[df["value"] > threshold]
send_metric("alerts", len(alerts), tags=["severity:high"])
```

### Bonnes pratiques

#### Code
 Variables d'environnement pour tous les chemins
 Logging à chaque étape critique
 Gestion d'erreurs avec métriques
 Tags cohérents sur toutes les métriques
 Traces APM avec spans explicites

#### Data pipeline
 Validation des données à chaque couche
 Format Parquet pour performance
 Immutabilité des couches Bronze/Silver
 Alertes métier dans Gold layer
 Idempotence des transformations

#### Monitoring
 Métriques de volumétrie ET performance
 Alertes sur anomalies métier
 Dashboard orienté diagnostic
 Corrélation traces/logs/métriques
 Seuils basés sur l'observation

---

##  Compétences acquises

### Techniques
- [x] Architecture medallion (Bronze/Silver/Gold)
- [x] Pipeline de données Python avec Pandas
- [x] Format Parquet pour big data
- [x] Instrumentation APM avec ddtrace
- [x] Métriques custom StatsD
- [x] Docker Compose multi-containers
- [x] Variables d'environnement et configuration
- [x] Logs structurés Python

### Conceptuelles
- [x] Data lakehouse pattern
- [x] Observabilité de pipelines data
- [x] Golden signals pour data (volume/performance/qualité/fiabilité)
- [x] Data quality monitoring
- [x] Architecture événementielle
- [x] Immutabilité des données
- [x] Idempotence des transformations

---

##  Extensions possibles

### Court terme
- [ ] Ajout d'étapes de transformation (agrégations, joins)
- [ ] Quality checks supplémentaires (nulls, duplicates)
- [ ] Métriques de data lineage
- [ ] Dashboard Datadog complet
- [ ] CI/CD pour déploiement automatique

### Moyen terme
- [ ] Scheduler (Airflow/Prefect) pour orchestration
- [ ] Intégration avec vraie source de données (API, DB)
- [] Partitionnement des données par date
- [ ] Compaction et optimisation Parquet
- [ ] Tests unitaires et d'intégration

### Long terme
- [ ] Migration vers Microsoft Fabric cloud
- [ ] Intégration OneLake
- [ ] Notebooks Synapse Spark
- [ ] Power BI pour visualisation
- [ ] Real-time streaming avec Event Hubs

---

##  Ressources utiles

### Microsoft Fabric
- [Documentation officielle](https://learn.microsoft.com/fabric/)
- [Medallion Architecture](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Best practices](https://learn.microsoft.com/fabric/data-engineering/best-practices-fabric-data-engineering)

### Datadog
- [APM Python](https://docs.datadoghq.com/tracing/setup_overview/setup/python/)
- [Custom Metrics](https://docs.datadoghq.com/metrics/custom_metrics/)
- [Data Pipeline Monitoring](https://www.datadoghq.com/blog/data-pipeline-monitoring/)

### Pandas & Parquet
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [PyArrow Parquet](https://arrow.apache.org/docs/python/parquet.html)

---

##  Conclusion

Ce projet démontre la mise en place d'un **pipeline de données moderne** avec :

 **Architecture medallion** (Bronze/Silver/Gold)
 **Observabilité complète** (APM/Metrics/Logs)
 **Détection d'alertes métier** (température moteur)
 **Infrastructure conteneurisée** (Docker)
 **Monitoring opérationnel** (Datadog)

Cette base est **prête pour migration vers Microsoft Fabric cloud** tout en conservant les mêmes principes d'observabilité.
