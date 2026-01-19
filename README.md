#  Bootcamp Observabilité & Data Engineering

> **Formation intensive en autonomie** – Décembre 2025 - Janvier 2026  
> **Auteur** : Juvet | **Poste** : DevOps Ingénieur InfoHub  
> **Entreprise** : Mercedes-Benz Trucks Molsheim

---

##  Objectif du Bootcamp

Maîtriser l'**observabilité des pipelines de données** avec Datadog à travers 4 projets progressifs couvrant l'ensemble de la stack moderne Data Engineering & DevOps.

**Durée** : 10 jours intensifs (27 décembre 2025 → 4 janvier 2026)  
**Résultat** : 4 projets complets, documentés, dockerisés, avec observabilité Datadog

---

##  Les 4 Projets du Bootcamp

### 1️ [Datadog – Infrastructure & Application Monitoring](./datadog/)

**Objectif** : Superviser l'infrastructure et une application Flask avec Datadog

**Technologies** : Datadog Agent 7, Flask 3.0, ddtrace 2.5.0, Docker Compose

**Réalisations** :
-  Monitoring infrastructure (CPU, mémoire, disque, containers)
-  Application Flask instrumentée avec APM, métriques custom, logs
-  Dashboards infrastructure + application (8+ widgets)
-  Alertes sur CPU, mémoire, erreurs, latence
-  Agent Datadog conteneurisé avec APM + StatsD

**Métriques clés** : 6+ métriques custom (request count, duration, errors, etc.)

**Endpoints** : `/`, `/health`, `/slow`, `/compute`, `/error`, `/metrics`

---

### 2️ [Microsoft Fabric Local – Pipeline Medallion Architecture](./microsoft-fabric/)

**Objectif** : Simuler un pipeline Fabric avec architecture medallion (Bronze/Silver/Gold)

**Technologies** : Python 3.11, Pandas 2.1.4, PyArrow 14.0.2, ddtrace, Docker

**Réalisations** :
-  Pipeline 3 étapes : Ingestion → Transformation → Validation
-  Architecture medallion : Raw → Bronze → Silver → Gold
-  Observabilité complète (traces APM, métriques, logs)
-  Détection d'alertes métier (température moteur > 95°C)
-  Infrastructure Docker multi-services

**Métriques clés** : 14 métriques custom (records, duration, alerts, quality rate)

**Format** : CSV → Parquet (Bronze) → Parquet enrichi (Silver) → Alertes (Gold)

---

### 3️ [Databricks Spark – Traitement Distribué](./databricks/)

**Objectif** : Job Spark de traitement de télémétrie avec data quality monitoring

**Technologies** : PySpark 3.5.0, Java 11, datadog 0.49.1, Docker

**Réalisations** :
-  Job PySpark : Lecture CSV → Transformations → Agrégations → Parquet
-  Data Quality : Filtres de validation, calcul taux de qualité
-  Agrégations métier par véhicule (speed, consumption, temp max)
-  Observabilité : Métriques Datadog, logging avec execution_id
-  Image Docker Spark + Python optimisée

**Métriques clés** : 9 métriques custom (records, quality rate, throughput, duration)

**Performance** : ~240 records/sec, data quality rate tracking

---

### 4️ [Azure Data Factory – Pipeline ETL Dockerisé](./azure-data-factory/)

**Objectif** : Pipeline ETL avec observabilité complète et simulation d'erreurs

**Technologies** : Python 3.11, CSV, datadog 0.49.1, Docker Compose

**Réalisations** :
-  Pipeline ETL : CSV → Enrichissement → CSV processé
-  20 métriques Datadog (volumétrie, performance, qualité)
-  Logs vers Datadog via custom handler (API Logs)
-  Simulation d'erreurs (3 types : connection, validation, processing)
-  Docker multi-services avec healthcheck

**Métriques clés** : 20 métriques custom (records, duration, error rate, throughput, events by type)

**Tests** : Simulation d'erreurs pour validation du monitoring

---

##  Synthèse Globale

### Statistiques du Bootcamp

-  **4 projets** complets et documentés
-  **49 métriques custom** Datadog au total
-  **~1500 lignes** de code Python
-  **4 agents Datadog** déployés
-  **12 services Docker** (agent + applications)
-  **30+ widgets** de dashboards
-  **18 monitors** configurés
-  **~5000 lignes** de documentation technique

---

##  Compétences Acquises

### Observabilité
- [x] Installation et configuration agent Datadog
- [x] Instrumentation APM Python (ddtrace)
- [x] Métriques custom via StatsD (gauge, counter, histogram, timing)
- [x] Logs structurés et API Datadog Logs
- [x] Corrélation traces ↔ logs ↔ métriques
- [x] Dashboards opérationnels (30+ widgets)
- [x] Monitors et alertes (18 au total)

### Data Engineering
- [x] Pipeline ETL complet (Extract/Transform/Load)
- [x] Architecture medallion (Raw/Bronze/Silver/Gold)
- [x] Format Parquet (lecture, écriture, optimisations)
- [x] PySpark : DataFrames, transformations, agrégations
- [x] Data Quality : filtres, validation, taux de qualité
- [x] Traitement distribué avec Spark

### Infrastructure & DevOps
- [x] Docker : images optimisées, multi-stage
- [x] Docker Compose : orchestration multi-services
- [x] Healthchecks et depends_on
- [x] Réseaux Docker (isolation)
- [x] Variables d'environnement (.env)
- [x] Logging structuré

---

##  Points Forts du Bootcamp

### 1. Observabilité End-to-End
 Du code à Datadog : Métriques, traces, logs  
 Corrélation complète via execution_id / trace_id  
 Dashboards opérationnels  
 Alertes intelligentes

### 2. Pipelines Data Modernes
 Architecture medallion  
 Data Quality monitoring  
 Formats optimisés (Parquet)  
 Traitement distribué (PySpark)

### 3. Infrastructure Conteneurisée
 Multi-services (Agent + App/Pipeline)  
 Réseaux isolés  
 Health checks  
 Portabilité (local → cloud)

### 4. Code Production-Ready
 Variables d'environnement  
 Gestion d'erreurs  
 Logging structuré  
 Tests d'erreurs (simulation)

---

##  Documentation

### Par Projet

Chaque projet contient :
-  **note.md** - Documentation technique exhaustive (~1000 lignes)
-  **docker-compose.yml** - Orchestration multi-services
-  **Scripts Python** - Code instrumenté avec Datadog
-  **.env.example** - Template de configuration
-  **Dashboards recommandés** - Widgets détaillés
-  **Monitors** - Alertes configurées

### Documentation Globale

-  **[Synthèse complète](./synthese/note.md)** - Vue d'ensemble des 4 projets
-  Comparatif des projets
-  Patterns et best practices réutilisables
-  Roadmap d'évolution (court/moyen/long terme)
-  Ressources et liens utiles

---

##  Démarrage Rapide

### Prérequis

- Docker & Docker Compose installés
- Clé API Datadog ([inscription gratuite](https://www.datadoghq.com/))
- Python 3.11+ (pour exécution locale)

### Lancer un projet

```bash
# Exemple : Datadog Flask App
cd datadog/app-demo

# Copier et configurer les variables d'environnement
cp .env.example .env
# Éditer .env avec votre clé API Datadog

# Lancer les services
docker-compose up --build

# Tester l'application
curl http://localhost:5000
curl http://localhost:5000/metrics

# Voir les dashboards dans Datadog
# → https://app.datadoghq.eu
```

### Structure type

```
projet/
├── docker-compose.yml      # Orchestration
├── Dockerfile             # Image applicative
├── requirements.txt       # Dépendances Python
├── .env.example          # Template configuration
├── scripts/              # Code source
│   └── *.py
├── data/                 # Données input/output
└── note.md              # Documentation technique
```

---

##  Patterns Réutilisables

### Pattern 1 : Métriques de Pipeline

```python
# Volumétrie
statsd.gauge("pipeline.records.raw", raw_count, tags=tags)
statsd.gauge("pipeline.records.clean", clean_count, tags=tags)

# Qualité
quality_rate = (clean_count / raw_count) * 100
statsd.gauge("pipeline.data.quality_rate", quality_rate, tags=tags)

# Performance
statsd.gauge("pipeline.duration", duration, tags=tags)
statsd.gauge("pipeline.throughput", records/duration, tags=tags)
```

### Pattern 2 : Corrélation via Execution ID

```python
# Génération ID unique
execution_id = str(uuid.uuid4())[:8]

# Tags communs
COMMON_TAGS = [f"execution_id:{execution_id}", f"env:{env}"]

# Logging avec contexte
logging.basicConfig(
    format=f"[exec:{execution_id}] %(levelname)s - %(message)s"
)
```

### Pattern 3 : Gestion d'Erreurs

```python
try:
    process_data()
    statsd.increment("pipeline.success", tags=tags)
except Exception as e:
    statsd.increment("pipeline.error", 
                     tags=tags + [f"error_type:{type(e).__name__}"])
    logging.error(f"Failed: {e}", exc_info=True)
    raise
```

---

##  Évolutions Possibles

### Court Terme (1-3 mois)
- [ ] Tests unitaires (pytest)
- [ ] CI/CD avec GitHub Actions
- [ ] Validation de schéma (Great Expectations)
- [ ] SLO (Service Level Objectives)

### Moyen Terme (3-6 mois)
- [ ] Migration sur Azure (ACI, Blob Storage, ADF)
- [ ] Databricks Workflows (scheduling)
- [ ] Delta Lake pour versioning
- [ ] Distributed tracing multi-services

### Long Terme (6-12 mois)
- [ ] Event-driven architecture (Event Hubs)
- [ ] Streaming avec Spark Structured Streaming
- [ ] MLflow pour tracking ML
- [ ] Kubernetes pour orchestration

---

##  Ressources

### Documentation Officielle
- [Datadog](https://docs.datadoghq.com/)
- [Microsoft Fabric](https://learn.microsoft.com/fabric/)
- [Databricks](https://docs.databricks.com/)
- [Azure Data Factory](https://learn.microsoft.com/azure/data-factory/)

### Technologies
- [PySpark](https://spark.apache.org/docs/latest/api/python/)
- [Pandas](https://pandas.pydata.org/docs/)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://docs.docker.com/)

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

** Note** : Tous les projets sont prêts à l'emploi avec documentation complète, code source, et configurations Docker. Les patterns sont applicables en production avec adaptations mineures (secrets, scaling, monitoring).


