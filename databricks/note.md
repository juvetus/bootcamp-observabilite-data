#  Databricks Spark – Traitement de Données Distribuées avec Observabilité

---

##  Résumé Exécutif

Ce document présente la mise en place d'un job Spark de traitement de données de télémétrie de camions avec une observabilité complète via Datadog.

**Ce qui a été réalisé :**

1. **Job Spark de traitement de données** 
   - Lecture de données CSV de télémétrie (camions)
   - Nettoyage et validation de qualité des données
   - Agrégations par véhicule (moyenne vitesse, consommation, température max)
   - Écriture des résultats en Parquet

2. **Observabilité complète avec Datadog** 
   - Métriques custom (volumétrie, qualité, performance)
   - Logging structuré avec execution_id pour traçabilité
   - Monitoring de la qualité des données
   - Mesure du throughput et de la performance

3. **Infrastructure Docker** 
   - Job Spark conteneurisé avec PySpark
   - Configuration Datadog intégrée
   - Variables d'environnement pour flexibilité
   - Volumes pour données input/output

**Bénéfices :**
- Traitement distribué de données de télémétrie
- Visibilité complète sur la qualité des données
- Métriques de performance du job Spark
- Architecture portable (local → Databricks cloud)

---

##  Objectifs

- Implémenter un job Spark de traitement de données
- Nettoyer et valider la qualité des données (data quality)
- Calculer des agrégations métier (par véhicule)
- Instrumenter le job avec Datadog (métriques custom)
- Préparer une base pour migration vers Databricks

---

##  Architecture

### Pipeline de traitement

```
truck_data.csv (Input)
    ↓
[Spark] Lecture + Cast types
    ↓
[Spark] Data Quality Filters
    ↓
[Spark] Agrégations par vehicle_id
    ↓
truck_metrics/ (Output Parquet)
```

### Flux de données détaillé

```
1. Raw Data (CSV)
   - vehicle_id, timestamp, speed, consumption, fuel_level
   - engine_temp, location_lat, location_lon

2. Type Casting
   - Conversion des colonnes en types appropriés
   - int pour speed, consumption, fuel_level, engine_temp
   - double pour location_lat, location_lon

3. Data Quality
   - Filtrage speed: 0 < speed <= 120
   - Filtrage engine_temp: 0 < temp <= 120
   - Filtrage fuel_level: >= 0
   - Calcul du taux de qualité

4. Aggregations
   - Groupement par vehicle_id
   - avg(speed), avg(consumption), avg(fuel_level)
   - max(engine_temp), count(events)

5. Output (Parquet)
   - Format optimisé pour analytics
   - Partitionnement possible
```

### Infrastructure

```
┌──────────────────┐
│  spark-job       │  PySpark Job
│  - spark_job.py  │  - Lecture CSV
│  - PySpark 3.5   │  - Transformations
│  - Java 11       │  - Écriture Parquet
│                  │  - Métriques Datadog
└────────┬─────────┘
         │
         │ StatsD (UDP 8125)
         ↓
┌──────────────────┐
│  dd-agent        │  Agent Datadog
│  (host.docker)   │  - StatsD server
└──────────────────┘
```

---

##  Structure du projet

```
databricks/
├── data/
│   ├── input/
│   │   └── truck_data.csv         # Données sources
│   └── output/
│       └── truck_metrics/         # Parquet output
│           ├── _SUCCESS
│           └── part-*.parquet
│
├── scripts/
│   └── spark_job.py              # Job PySpark principal
│
├── docker-compose.yml            # Orchestration
├── Dockerfile                    # Image Spark + Python
├── requirements.txt              # Dépendances Python
├── .env                         # Variables d'environnement
└── note.md                      # Documentation
```

---

##  Job Spark (spark_job.py)

### Vue d'ensemble

Job PySpark qui traite des données de télémétrie de camions avec instrumentation Datadog complète.

### Fonctionnalités principales

#### 1. **Initialisation**
```python
# Génération execution_id unique pour traçabilité
execution_id = str(uuid.uuid4())

# Tags communs pour toutes les métriques
COMMON_TAGS = [
    f'service:spark-job',
    f'env:{env}',
    f'execution_id:{execution_id}',
    'job:truck_telemetry'
]
```

#### 2. **Configuration Spark**
```python
spark = SparkSession.builder \
    .appName("TruckTelemetryJob") \
    .master("local[*]") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()
```

#### 3. **Lecture des données**
```python
df = spark.read.option("header", True).csv(data_path)
raw_count = df.count()

# Métrique : volumétrie brute
statsd.gauge('spark.records.raw', raw_count, tags=COMMON_TAGS)
```

#### 4. **Type casting**
```python
typed_df = df \
    .withColumn("speed", col("speed").cast("int")) \
    .withColumn("consumption", col("consumption").cast("int")) \
    .withColumn("fuel_level", col("fuel_level").cast("int")) \
    .withColumn("engine_temp", col("engine_temp").cast("int")) \
    .withColumn("location_lat", col("location_lat").cast("double")) \
    .withColumn("location_lon", col("location_lon").cast("double"))
```

#### 5. **Data Quality Filters**
```python
clean_df = typed_df \
    .filter((col("speed") > 0) & (col("speed") <= 120)) \
    .filter((col("engine_temp") > 0) & (col("engine_temp") <= 120)) \
    .filter(col("fuel_level") >= 0)

clean_count = clean_df.count()
filtered_count = raw_count - clean_count

# Métriques : qualité des données
statsd.gauge('spark.records.clean', clean_count, tags=COMMON_TAGS)
statsd.gauge('spark.records.filtered', filtered_count, tags=COMMON_TAGS)

quality_rate = (clean_count / raw_count) * 100
statsd.gauge('spark.data.quality_rate', quality_rate, tags=COMMON_TAGS)
```

#### 6. **Agrégations métier**
```python
agg_df = clean_df.groupBy("vehicle_id").agg(
    avg("speed").alias("avg_speed"),
    avg("consumption").alias("avg_consumption"),
    avg("fuel_level").alias("avg_fuel_level"),
    max("engine_temp").alias("max_engine_temp"),
    count("*").alias("nb_events")
)

agg_count = agg_df.count()
statsd.gauge('spark.vehicles.processed', agg_count, tags=COMMON_TAGS)
```

#### 7. **Écriture des résultats**
```python
agg_df.write.mode("overwrite").parquet(output_path)
```

#### 8. **Métriques de performance**
```python
duration = end_time - start_time
statsd.gauge('spark.job.duration', duration, tags=COMMON_TAGS)
statsd.increment('spark.job.success', tags=COMMON_TAGS)

throughput = raw_count / duration if duration > 0 else 0
statsd.gauge('spark.job.throughput', throughput, tags=COMMON_TAGS)
```

### Variables d'environnement utilisées

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DD_API_KEY` | Clé API Datadog | - |
| `DD_AGENT_HOST` | Host agent Datadog | dd-agent |
| `DD_DOGSTATSD_PORT` | Port StatsD | 8125 |
| `ENV` | Environnement (dev/prod) | dev |

### Logging structuré

Tous les logs incluent l'`execution_id` pour traçabilité :

```python
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - [execution_id:{execution_id}] - %(levelname)s - %(message)s'
)
```

**Exemples de logs** :
```
2026-01-19 10:00:00 - [execution_id:abc-123] - INFO - Starting Spark job
2026-01-19 10:00:01 - [execution_id:abc-123] - INFO - Raw data loaded: 1000 records
2026-01-19 10:00:02 - [execution_id:abc-123] - INFO - Data quality rate: 95.50%
2026-01-19 10:00:03 - [execution_id:abc-123] - INFO - ✅ Job completed successfully in 3.45s
```

---

##  Métriques collectées

### Métriques Spark

| Métrique | Type | Description | Tags |
|----------|------|-------------|------|
| `spark.job.start` | Counter | Démarrage du job | service, env, execution_id, job |
| `spark.records.raw` | Gauge | Nombre d'enregistrements bruts | service, env, execution_id, job |
| `spark.records.clean` | Gauge | Enregistrements après nettoyage | service, env, execution_id, job |
| `spark.records.filtered` | Gauge | Enregistrements filtrés (invalides) | service, env, execution_id, job |
| `spark.data.quality_rate` | Gauge | Taux de qualité (%) | service, env, execution_id, job |
| `spark.vehicles.processed` | Gauge | Nombre de véhicules traités | service, env, execution_id, job |
| `spark.job.duration` | Gauge | Durée totale du job (s) | service, env, execution_id, job |
| `spark.job.throughput` | Gauge | Records/seconde | service, env, execution_id, job |
| `spark.job.success` | Counter | Succès du job | service, env, execution_id, job |

### Tags appliqués

Tous les metrics incluent ces tags pour filtrage et corrélation :
- `service:spark-job`
- `env:{dev|prod}`
- `execution_id:{uuid}`
- `job:truck_telemetry`

---

##  Configuration Docker

### docker-compose.yml

```yaml
services:
  spark-job:
    build: .
    container_name: databricks-spark-job
    volumes:
      - ./data/input:/app/data/input
      - ./data/output:/app/data/output
    environment:
      - SPARK_LOCAL_DIRS=/tmp/spark
      - DD_API_KEY=${DD_API_KEY}
      - DD_AGENT_HOST=host.docker.internal  # Accès à l'agent sur l'hôte
      - DD_DOGSTATSD_PORT=8125
      - ENV=dev
```

**Note** : `host.docker.internal` permet au container d'accéder à l'agent Datadog tournant sur l'hôte.

### Dockerfile

```dockerfile
FROM eclipse-temurin:11-jdk-jammy

# Installer Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copier requirements et installer
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copier les scripts et données
COPY scripts/ ./scripts/
COPY data/ ./data/

# Créer le dossier de sortie
RUN mkdir -p output

# Variables d'environnement Spark
ENV PYSPARK_PYTHON=python3
ENV PYSPARK_DRIVER_PYTHON=python3

CMD ["python3", "scripts/spark_job.py"]
```

### requirements.txt

```txt
pyspark==3.5.0
datadog==0.49.1
python-dotenv==1.0.0
requests==2.31.0
```

---

##  Ressources utiles

### Apache Spark
- [Documentation officielle](https://spark.apache.org/docs/latest/)
- [PySpark API](https://spark.apache.org/docs/latest/api/python/)
- [Spark SQL Guide](https://spark.apache.org/docs/latest/sql-programming-guide.html)

### Databricks
- [Databricks Documentation](https://docs.databricks.com/)
- [Best Practices](https://docs.databricks.com/en/optimizations/index.html)

### Datadog
- [Custom Metrics](https://docs.datadoghq.com/metrics/custom_metrics/)
- [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/)

---

##  Conclusion

Ce projet démontre la mise en place d'un **job Spark de production** avec :

 **Traitement de données distribué** (PySpark)
 **Data Quality Monitoring** (filtres, métriques)
 **Observabilité complète** (Datadog)
 **Infrastructure portable** (Docker)
 **Architecture évolutive** (vers Databricks cloud)

Cette base est **prête pour migration vers Databricks** tout en conservant les mêmes principes d'observabilité et de qualité de données.
