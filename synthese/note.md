#  Synthèse Bootcamp Observabilité & Data Engineering

**Auteur** : Juvet  
**Poste** : DevOps Ingénieur InfoHub  
**Entreprise** : Mercedes-Benz Trucks Molsheim  
**Période** : Décembre 2025 - Janvier 2026  
**Objectif** : Maîtriser l'observabilité des pipelines de données avec Datadog

---

##  Vue d'ensemble du Bootcamp

Ce bootcamp a permis de construire une **compétence complète en observabilité de systèmes data** à travers 4 projets progressifs couvrant l'ensemble de la stack moderne :

1. **Infrastructure & Containers** → Datadog
2. **Pipeline Data Cloud** → Microsoft Fabric (local)
3. **Traitement Distribué** → Databricks Spark
4. **Orchestration ETL** → Azure Data Factory

### Fil conducteur : Observabilité avec Datadog

Tous les projets partagent une **philosophie commune** :
-  **Traces APM** pour suivre les exécutions
-  **Métriques custom** pour mesurer la performance
-  **Logs structurés** pour diagnostiquer les problèmes
-  **Dashboards** pour visualiser l'état
-  **Alertes** pour réagir rapidement

---

##  Les 4 Projets du Bootcamp

### 1️ Datadog – Infrastructure & Application Monitoring

**Objectif** : Superviser l'infrastructure et une application Flask

#### Ce qui a été réalisé
-  **Monitoring infrastructure** : CPU, mémoire, disque, containers Docker
-  **Application Flask instrumentée** : APM, métriques custom, logs
-  **Dashboards** : Infrastructure + Application avec 8+ widgets
-  **Alertes** : CPU, mémoire, erreurs, latence
-  **Agent Datadog** : Déployé en container avec APM + StatsD

#### Technologies
- Datadog Agent 7
- Flask 3.0
- ddtrace 2.5.0 (APM Python)
- datadog 0.49.1 (StatsD client)
- Docker Compose

#### Métriques clés
- `flask.request.count` - Compteur de requêtes
- `flask.request.duration` - Durée des requêtes (histogramme)
- `flask.error.count` - Compteur d'erreurs
- `system.cpu.user` - Utilisation CPU
- `system.mem.used` - Mémoire utilisée

#### Endpoints Flask
- `GET /` - Page d'accueil avec infos service
- `GET /health` - Health check
- `GET /slow` - Endpoint lent (0.5-2s) pour tests perfs
- `GET /compute` - Calculs intensifs avec span custom
- `GET /error` - Génération d'erreur pour monitoring
- `GET /metrics` - Métriques du service

#### Apprentissages
- Installation et configuration agent Datadog
- Instrumentation APM avec ddtrace
- Métriques custom via StatsD
- Corrélation traces ↔ logs ↔ métriques
- Construction de dashboards opérationnels
- Configuration d'alertes pertinentes

---

### 2️ Microsoft Fabric Local – Pipeline Medallion Architecture

**Objectif** : Simuler un pipeline Fabric avec architecture medallion (Bronze/Silver/Gold)

#### Ce qui a été réalisé
-  **Pipeline 3 étapes** : Ingestion → Transformation → Validation
-  **Architecture medallion** : Raw → Bronze → Silver → Gold
-  **Observabilité complète** : Traces, métriques, logs avec Datadog
-  **Détection d'alertes métier** : Température moteur > 95°C
-  **Infrastructure Docker** : Agent Datadog + Pipeline Python

#### Technologies
- Python 3.11
- Pandas 2.1.4 + PyArrow 14.0.2 (Parquet)
- ddtrace 2.5.0 (APM)
- datadog 0.49.1 (métriques)
- Docker Compose

#### Pipeline de données
```
trucks.csv (Raw)
    ↓
ingest.py → trucks.parquet (Bronze)
    ↓
transform.py → trucks.parquet enrichi (Silver)
    ↓
validate.py → alerts.parquet (Gold)
```

#### Métriques clés
- `fabric.pipeline.ingest.success` - Succès ingestion
- `fabric.pipeline.ingest.records` - Nombre de records ingérés
- `fabric.pipeline.transform.duration` - Durée transformation
- `fabric.pipeline.alerts` - Nombre d'alertes détectées
- `fabric.pipeline.alert_rate` - Taux d'alertes (%)

#### Fonctionnalités par étape
1. **Ingestion** : CSV → Parquet, comptage records
2. **Transformation** : Enrichissement (speed_kmh, processed_at)
3. **Validation** : Détection alertes (engine_temp > threshold)

#### Apprentissages
- Architecture medallion (Bronze/Silver/Gold)
- Format Parquet pour big data
- Variables d'environnement pour config
- Gestion d'erreurs avec métriques
- Data quality monitoring
- Idempotence des transformations

---

### 3️ Databricks Spark – Traitement Distribué

**Objectif** : Job Spark de traitement de télémétrie avec data quality

#### Ce qui a été réalisé
-  **Job PySpark** : Lecture CSV, transformations, agrégations, écriture Parquet
-  **Data Quality** : Filtres de validation, calcul taux de qualité
-  **Agrégations métier** : Moyenne vitesse, consommation, température max par véhicule
-  **Observabilité** : Métriques Datadog, logging structuré avec execution_id
-  **Docker** : Image Spark + Python avec PySpark 3.5

#### Technologies
- PySpark 3.5.0
- Java 11 (Eclipse Temurin)
- datadog 0.49.1
- Docker

#### Pipeline Spark
```
truck_data.csv
    ↓
[Spark] Type Casting (int, double)
    ↓
[Spark] Data Quality Filters
    ↓
[Spark] Agrégations par vehicle_id
    ↓
truck_metrics/ (Parquet)
```

#### Filtres de qualité appliqués
- Speed : 0 < speed ≤ 120
- Engine temp : 0 < temp ≤ 120  
- Fuel level : ≥ 0

#### Métriques clés
- `spark.records.raw` - Enregistrements bruts
- `spark.records.clean` - Records après nettoyage
- `spark.records.filtered` - Records invalides filtrés
- `spark.data.quality_rate` - Taux de qualité (%)
- `spark.vehicles.processed` - Véhicules traités
- `spark.job.duration` - Durée du job
- `spark.job.throughput` - Records/seconde

#### Agrégations calculées
- `avg(speed)` - Vitesse moyenne par véhicule
- `avg(consumption)` - Consommation moyenne
- `avg(fuel_level)` - Niveau carburant moyen
- `max(engine_temp)` - Température moteur maximale
- `count(*)` - Nombre d'événements par véhicule

#### Apprentissages
- Architecture Spark (Driver/Executors)
- DataFrames Spark et transformations
- Lazy evaluation et DAG
- Data Quality Monitoring
- PySpark en production
- Logging structuré avec execution_id unique

---

### 4️ Azure Data Factory – Pipeline ETL Dockerisé

**Objectif** : Pipeline ETL avec observabilité complète et simulation d'erreurs

#### Ce qui a été réalisé
-  **Pipeline ETL Python** : Lecture CSV → Enrichissement → Écriture
-  **20 métriques Datadog** : Volumétrie, performance, qualité
-  **Logs vers Datadog** : Custom handler avec API Logs
-  **Simulation d'erreurs** : 3 types (connection, validation, processing)
-  **Docker multi-services** : Agent Datadog + Pipeline avec healthcheck

#### Technologies
- Python 3.11
- CSV (module stdlib)
- datadog 0.49.1
- requests 2.31.0
- Docker Compose avec healthcheck

#### Pipeline ETL
```
events.csv (60 lignes)
    ↓
[Python] Lecture + Enrichissement
    - Ajout processed_at (timestamp)
    - Ajout pipeline (source)
    ↓
events_processed.csv (60 lignes enrichies)
```

#### Métriques clés (20 au total)
- `pipeline.started` / `pipeline.success` / `pipeline.error`
- `pipeline.records_processed` / `records_success` / `records_errors`
- `pipeline.duration_seconds`
- `pipeline.throughput_records_per_second`
- `pipeline.record_processing_time` (timing par record)
- `pipeline.avg/max/min_record_processing_time_ms`
- `pipeline.error_rate_percent` / `success_rate_percent`
- `pipeline.events_by_type` (login, logout, error)
- `pipeline.completion_rate_percent` (avant échec)

#### Simulation d'erreurs pour tests
1. **Connection error** : Échec connexion source
2. **Validation error** : Enregistrement invalide (ignoré)
3. **Processing error** : Erreur de traitement (arrêt)

#### Custom Datadog Log Handler
```python
class DatadogLogHandler(logging.Handler):
    # Envoie les logs directement à Datadog Logs API
    # POST https://http-intake.logs.datadoghq.eu/api/v2/logs
    # Avec tags: execution_id, pipeline, env
```

#### Apprentissages
- Pipeline ETL complet
- Logs vers Datadog via API HTTP
- Corrélation logs/métriques via execution_id
- Simulation d'erreurs pour tests
- Métriques de qualité (error rate, success rate)
- Docker healthcheck et depends_on

---

##  Comparatif des 4 Projets

| Aspect | Datadog | Fabric | Databricks | ADF |
|--------|---------|---------|-----------|-----|
| **Focus** | Monitoring infra & app | Pipeline medallion | Traitement distribué | ETL orchestré |
| **Langage** | Python (Flask) | Python (Pandas) | Python (PySpark) | Python (CSV) |
| **Format données** | HTTP/JSON | Parquet | Parquet | CSV |
| **Volume** | N/A (app web) | ~1000 records | ~10000 records | 60 records |
| **Métriques** | 6+ custom | 14 custom | 9 custom | 20 custom |
| **Traces APM** |  Avec spans |  Par étape |  (métriques only) |  (métriques only) |
| **Logs** |  Injection trace_id |  Structurés |  Avec execution_id |  API Logs Datadog |
| **Docker** |  Agent + App |  Agent + Pipeline |  Job standalone |  Agent + Pipeline |
| **Simulation erreurs** |  Endpoint /error |  Try/except |  |  3 types |
| **Dashboards** |  8 widgets |  6 widgets |  8 widgets |  8 widgets |
| **Monitors** |  4 alertes |  4 alertes |  5 alertes |  5 alertes |

---

##  Compétences Acquises

### Techniques

#### Observabilité
- [x] Installation et configuration agent Datadog
- [x] Instrumentation APM Python avec ddtrace
- [x] Métriques custom via StatsD (gauge, counter, histogram, timing)
- [x] Logs structurés avec contexte
- [x] Logs vers API Datadog (HTTP)
- [x] Corrélation traces ↔ logs ↔ métriques
- [x] Dashboards Datadog (8+ widgets par projet)
- [x] Monitors et alertes (20+ au total)
- [x] Tags cohérents pour filtrage

#### Data Engineering
- [x] Pipeline ETL complet (Extract/Transform/Load)
- [x] Architecture medallion (Raw/Bronze/Silver/Gold)
- [x] Format Parquet (lecture, écriture, optimisations)
- [x] PySpark : DataFrames, transformations, agrégations
- [x] Data Quality : filtres, validation, taux de qualité
- [x] Traitement distribué avec Spark
- [x] CSV : lecture, écriture, enrichissement

#### Infrastructure & DevOps
- [x] Docker : images optimisées, multi-stage
- [x] Docker Compose : orchestration multi-services
- [x] Healthchecks et depends_on
- [x] Réseaux Docker (isolation)
- [x] Volumes Docker (persistance)
- [x] Variables d'environnement (.env)
- [x] Logging structuré (Python logging)

#### Python
- [x] Flask : API REST, middlewares
- [x] Pandas : DataFrames, transformations
- [x] PySpark : Spark SQL, agrégations
- [x] CSV : DictReader/DictWriter
- [x] Requests : API HTTP
- [x] UUID : identifiants uniques
- [x] Datetime : timezone-aware timestamps

### Conceptuelles

#### Observabilité
- [x] Les 3 piliers : Métriques / Traces / Logs
- [x] Golden signals : Latence, Trafic, Erreurs, Saturation
- [x] Observabilité vs Monitoring
- [x] Corrélation et contexte (execution_id, trace_id)
- [x] Alerting intelligent (thresholds, windows)
- [x] SLI, SLO, SLA (concepts)

#### Data Engineering
- [x] Architecture medallion
- [x] Data Quality Monitoring
- [x] Immutabilité des données
- [x] Idempotence des transformations
- [x] Data lineage (traçabilité)
- [x] Pipeline patterns (batch processing)

#### Architecture
- [x] Microservices (containers isolés)
- [x] Calcul distribué (Spark)
- [x] Cloud readiness (portable vers Azure)
- [x] Infrastructure as Code (Docker Compose)
- [x] Configuration externalisée (env vars)

---

##  Métriques Globales du Bootcamp

### Volume de code
- **4 projets** complets et documentés
- **8 scripts Python** (app.py, 3 pipelines, spark_job.py, transform.py, metrics.py)
- **~1500 lignes de code Python**
- **4 docker-compose.yml** avec services multiples
- **4 Dockerfiles** optimisés
- **4 requirements.txt** avec dépendances

### Métriques Datadog
- **49 métriques custom** au total (6+14+9+20)
- **4 agents Datadog** déployés
- **30+ dashboards widgets** recommandés
- **18 monitors** configurés
- **Logs structurés** sur les 4 projets

### Documentation
- **4 notes techniques** exhaustives
- **~5000 lignes de markdown**
- **Architecture détaillée** par projet
- **Guides pas à pas** de démarrage
- **Tableaux de métriques** complets

---

##  Réalisations Clés

### 1. Observabilité End-to-End

 **Du code à Datadog** : Chaque projet envoie métriques, traces et logs
 **Corrélation complète** : execution_id ou trace_id pour lier les données
 **Dashboards opérationnels** : Visualisation immédiate de l'état
 **Alertes intelligentes** : Détection proactive des problèmes

### 2. Pipelines Data Modernes

 **Architecture medallion** : Bronze → Silver → Gold
 **Data Quality** : Filtres, validation, métriques de qualité
 **Formats optimisés** : Parquet pour performance
 **Traitement distribué** : PySpark pour scalabilité

### 3. Infrastructure Conteneurisée
 **Multi-services** : Agent Datadog + Application/Pipeline
 **Réseaux isolés** : Sécurité et organisation
 **Health checks** : Démarrage orchestré
 **Portabilité** : Fonctionne partout (local → cloud)

### 4. Code Production-Ready

 **Variables d'environnement** : Configuration externalisée
 **Gestion d'erreurs** : Try/except avec métriques
 **Logging structuré** : Contexte, niveaux, timestamps
 **Tests d'erreurs** : Simulation pour validation

---

##  Patterns et Best Practices

### Pattern 1 : Métriques de Pipeline Data

```python
# Volumétrie
statsd.gauge("pipeline.records.raw", raw_count)
statsd.gauge("pipeline.records.clean", clean_count)

# Qualité
quality_rate = (clean_count / raw_count) * 100
statsd.gauge("pipeline.data.quality_rate", quality_rate)

# Performance
statsd.gauge("pipeline.duration", duration)
statsd.gauge("pipeline.throughput", records / duration)
```

### Pattern 2 : Corrélation via Execution ID

```python
# Génération d'un ID unique
execution_id = str(uuid.uuid4())[:8]

# Tags communs sur toutes les métriques
COMMON_TAGS = [f"execution_id:{execution_id}", f"env:{env}"]

# Logging avec contexte
logging.basicConfig(
    format=f"[exec:{execution_id}] %(levelname)s - %(message)s"
)
```

### Pattern 3 : Gestion d'Erreurs avec Métriques

```python
try:
    process_data()
    statsd.increment("pipeline.success", tags=COMMON_TAGS)
    
except Exception as e:
    error_type = type(e).__name__
    statsd.increment("pipeline.error", 
                     tags=COMMON_TAGS + [f"error_type:{error_type}"])
    logging.error(f"Pipeline failed: {str(e)}", exc_info=True)
    raise
```

### Pattern 4 : Docker Healthcheck

```yaml
services:
  dd-agent:
    healthcheck:
      test: ["CMD", "agent", "health"]
      interval: 10s
      timeout: 5s
      retries: 5
      
  app:
    depends_on:
      dd-agent:
        condition: service_healthy  # ← Attend que l'agent soit prêt
```

### Pattern 5 : Métriques de Qualité

```python
# Comptage des erreurs et succès
records_success = records - errors
error_rate = (errors / records * 100) if records > 0 else 0
success_rate = 100 - error_rate

# Envoi à Datadog
statsd.gauge("pipeline.error_rate_percent", error_rate)
statsd.gauge("pipeline.success_rate_percent", success_rate)
```

---

##  Évolutions et Extensions

### Court Terme (1-3 mois)

#### Datadog
- [ ] Créer des SLO (Service Level Objectives)
- [ ] Implémenter le profiling continu
- [ ] Ajouter RUM (Real User Monitoring) si frontend
- [ ] Synthetic tests pour monitoring externe

#### Pipelines Data
- [ ] Ajout de tests unitaires (pytest)
- [ ] Validation de schéma (Great Expectations)
- [ ] Partitionnement par date
- [ ] Compaction Parquet automatique

#### Infrastructure
- [ ] CI/CD avec GitHub Actions
- [ ] Secrets management (Vault)
- [ ] Monitoring des containers (cAdvisor)
- [ ] Log aggregation (Loki)

### Moyen Terme (3-6 mois)

#### Migration Cloud
- [ ] Déployer sur Azure Container Instances
- [ ] Intégration Azure Blob Storage
- [ ] Azure Data Factory en production
- [ ] Azure Monitor + Datadog

#### Databricks Production
- [ ] Cluster Spark multi-nœuds
- [ ] Databricks Workflows (scheduling)
- [ ] Delta Lake pour versioning
- [ ] Unity Catalog pour governance

#### Observabilité Avancée
- [ ] Distributed tracing multi-services
- [ ] Anomaly detection avec ML
- [ ] Custom APM pour Spark jobs
- [ ] Cost monitoring et optimisation

### Long Terme (6-12 mois)

#### Architecture
- [ ] Event-driven architecture (Event Hubs)
- [ ] Streaming avec Spark Structured Streaming
- [ ] Data Lakehouse complet (Databricks)
- [ ] Kubernetes pour orchestration

#### Governance
- [ ] Data Catalog complet
- [ ] Data lineage end-to-end
- [ ] GDPR compliance (data masking)
- [ ] Access control (RBAC)

#### ML & Analytics
- [ ] MLflow pour tracking ML
- [ ] Feature Store (Databricks/Azure ML)
- [ ] Power BI pour visualisation
- [ ] Real-time analytics

---

##  Ressources et Documentation

### Documentation Officielle

#### Datadog
- [Getting Started](https://docs.datadoghq.com/getting_started/)
- [APM Python](https://docs.datadoghq.com/tracing/setup_overview/setup/python/)
- [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/)
- [Log Management](https://docs.datadoghq.com/logs/)
- [Dashboards](https://docs.datadoghq.com/dashboards/)

#### Microsoft Fabric
- [Documentation](https://learn.microsoft.com/fabric/)
- [Medallion Architecture](https://learn.microsoft.com/fabric/onelake/onelake-medallion-lakehouse-architecture)
- [Data Engineering Best Practices](https://learn.microsoft.com/fabric/data-engineering/best-practices-fabric-data-engineering)

#### Databricks
- [Documentation](https://docs.databricks.com/)
- [PySpark Guide](https://spark.apache.org/docs/latest/api/python/)
- [Optimizations](https://docs.databricks.com/en/optimizations/index.html)
- [Delta Lake](https://docs.delta.io/)

#### Azure Data Factory
- [Documentation](https://learn.microsoft.com/azure/data-factory/)
- [Tutorials](https://learn.microsoft.com/azure/data-factory/tutorial-copy-data-portal)
- [Best Practices](https://learn.microsoft.com/azure/data-factory/concepts-data-flow-best-practices)

### Outils et Technologies

#### Python
- [Pandas](https://pandas.pydata.org/docs/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://requests.readthedocs.io/)

#### Data Formats
- [Parquet](https://parquet.apache.org/docs/)
- [PyArrow](https://arrow.apache.org/docs/python/)

#### Docker
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Compose](https://docs.docker.com/compose/)
- [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

---

##  Conclusion

### Objectifs Atteints

 **Maîtrise de l'observabilité** : 4 projets avec Datadog (APM, métriques, logs)  
 **Pipelines data modernes** : Architecture medallion, Spark, ETL  
 **Infrastructure cloud-ready** : Docker, variables d'environnement, portabilité  
 **Code production-ready** : Gestion d'erreurs, logging, tests  
 **Documentation exhaustive** : ~5000 lignes de markdown technique

### Compétences Professionnelles

Ce bootcamp a permis de développer des compétences directement applicables en entreprise :

1. **DevOps** : Docker, CI/CD readiness, infrastructure as code
2. **Data Engineering** : Pipelines ETL, Spark, formats optimisés
3. **Observabilité** : Monitoring complet, alerting, dashboards
4. **Cloud** : Architecture cloud-ready, migration path vers Azure
5. **Python** : Flask, Pandas, PySpark, patterns de production

### Valeur pour Mercedes-Benz Trucks

Ces projets sont directement transposables au contexte automobile :

- **Télémétrie véhicules** : Pipelines Spark pour traiter les données capteurs
- **Fleet Management** : Dashboards Datadog pour monitoring parc de camions
- **Maintenance prédictive** : Data Quality + ML pour anticiper les pannes
- **Optimisation logistique** : ETL pour analyser routes et consommation

### Prochaines Étapes

1. **Application métier** : Adapter les pipelines aux cas d'usage Mercedes-Benz
2. **Migration cloud** : Déployer sur Azure avec ADF et Databricks
3. **Intégration continue** : CI/CD pour automatiser les déploiements
4. **Formation équipe** : Partager les connaissances et patterns

---

##  Statistiques Finales

### Projets
-  **4 projets** complets et documentés
-  **4 agents Datadog** déployés et configurés
-  **12 services Docker** (dd-agent + applications)
-  **4 réseaux Docker** isolés

### Code
-  **~1500 lignes** de Python
-  **49 métriques custom** Datadog
-  **30+ widgets** de dashboards
-  **18 monitors** configurés

### Documentation
-  **4 notes techniques** (~1000 lignes chacune)
-  **1 synthèse** complète (ce document)
-  **Architecture détaillée** par projet
-  **Guides de démarrage** pas à pas

### Technologies Maîtrisées
-  Datadog (Agent, APM, Métriques, Logs)
-  Python (Flask, Pandas, PySpark, CSV)
-  Docker (Compose, multi-stage, healthcheck)
-  Spark (PySpark, DataFrames, agrégations)
-  Formats data (CSV, Parquet, JSON)

---

##  Auteur

**Juvet**  
**Poste** : DevOps Ingénieur InfoHub  
**Entreprise** : Mercedes-Benz Trucks Molsheim  
**Période** : Décembre 2025 - Janvier 2026

---

##  Remerciements

- **Mercedes-Benz Trucks** pour l'opportunité de ce bootcamp
- **Datadog** pour la plateforme d'observabilité
- **Communauté Open Source** pour les outils (Spark, Pandas, Docker)

---

** Note** : Tous les projets sont disponibles dans ce repository avec documentation complète, code source, et configurations Docker prêtes à l'emploi.

** Ready for Production** : Les patterns et architectures présentés sont applicables en environnement de production avec adaptations mineures (secrets, scaling, monitoring).
