#  Azure Data Factory – Automatisation du Traitement de Données

---

##  Résumé Simple

**Imaginez une usine de traitement de données** : des informations brutes entrent d'un côté, elles sont nettoyées et enrichies au milieu, puis ressortent propres et utilisables de l'autre côté. C'est exactement ce que fait ce projet !

###  L'Analogie de la Chaîne de Production

Pensez à une **chaîne de montage automobile** :
1.  **Entrée** : Les pièces brutes arrivent (nos fichiers CSV)
2.  **Transformation** : Les ouvriers assemblent et ajoutent des composants (notre script Python)
3.  **Sortie** : Une voiture complète sort de la chaîne (fichier enrichi)
4.  **Contrôle qualité** : Des inspecteurs vérifient chaque étape (Datadog)

---

##  Ce Qui a Été Fait

### 1. Création d'un Robot de Traitement de Données 

**En termes simples** : Un programme qui lit automatiquement un fichier Excel (CSV), ajoute des informations utiles, et crée un nouveau fichier.

**Exemple concret** :
- **Avant** : `alice, login, 10:00`
- **Après** : `alice, login, 10:00, traité le 30/12/2025 à 13:00, par pipeline-adf`

C'est comme un tampon qui marque "Vu et vérifié" sur chaque ligne du document.

### 2. Installation d'un Système de Surveillance 

**Datadog** = Un tableau de bord comme celui d'une voiture qui montre :
-  Combien de temps ça prend
-  Combien de lignes ont été traitées
-  Si tout s'est bien passé ou s'il y a eu des erreurs
-  Des alertes si quelque chose ne va pas

### 3. Mise en Boîte avec Docker 

**Docker** = Une boîte magique qui contient tout le nécessaire pour faire fonctionner notre robot :
- Le programme Python (le cerveau)
- Les outils nécessaires (les mains)
- La configuration (le mode d'emploi)

**Avantage** : On peut transporter cette boîte partout et elle fonctionnera de la même manière !

---

##  Le Contexte Technique (Vulgarisé)

### Les Outils Utilisés

| Outil | Analogie | À Quoi Ça Sert |
|-------|----------|-----------------|
| **Python** | Le chef cuisinier | Suit la recette pour transformer les données |
| **CSV** | Un tableau Excel | Format simple pour stocker des données |
| **Datadog** | Caméras de surveillance | Surveille que tout fonctionne bien |
| **Docker** | Boîte hermétique | Garantit que ça marche partout pareil |
| **Azure Data Factory** | Usine dans le cloud | Version professionnelle hébergée chez Microsoft |

---

##  Comment Ça Marche ?

### Le Processus en 3 Étapes

```
 ENTRÉE                    🔧 TRAITEMENT                     SORTIE
─────────────────────────────────────────────────────────────────────
Fichier events.csv           Robot Python lit                 Fichier enrichi
62 lignes d'événements  →    Ajoute date + source      →     62 lignes + infos
(login, logout, error)       Compte et vérifie                Prêt à utiliser
```

### Exemple Réel de Transformation

**Fichier d'entrée** (ce qu'on a au départ) :
```
id | type   | utilisateur | heure
1  | login  | alice       | 10:00
2  | logout | bob         | 10:05
```

**Fichier de sortie** (ce qu'on obtient) :
```
id | type   | utilisateur | heure | date_traitement           | source_pipeline
1  | login  | alice       | 10:00 | 2025-12-30T13:00:00      | docker-adf-pipeline
2  | logout | bob         | 10:05 | 2025-12-30T13:00:00      | docker-adf-pipeline
```

**Ce qui a été ajouté** :
-  **date_traitement** : Quand le fichier a été traité (pour traçabilité)
-  **source_pipeline** : Quel robot a fait le travail (pour l'audit)

---

##  Les Métriques : Voir Ce Qui Se Passe

### Tableau de Bord (Dashboard)

Imaginez le **compteur kilométrique d'une voiture** qui affiche :

|  Métrique |  Signification |  Exemple |
|------------|-----------------|-----------|
| **Records traités** | Nombre de lignes lues | 60 lignes |
| **Durée** | Temps pour tout traiter | 0.25 seconde |
| **Taux de succès** | Pourcentage sans erreur | 100%  |
| **Vitesse** | Lignes par seconde | 240 lignes/sec |
| **Erreurs** | Nombre de problèmes | 0 erreur |

### Graphiques Visuels

Dans Datadog, vous voyez des **graphiques en temps réel** comme :
-  Une courbe de la vitesse de traitement
-  Un camembert des types d'événements (login vs logout vs error)
-  Des feux tricolores : vert = OK, rouge = problème

---

##  Système d'Alerte Intelligent

### Comment Ça Fonctionne ?

C'est comme une **alarme incendie** dans un bâtiment :

1. **Situation normale** 
   - Le pipeline tourne
   - Tout fonctionne bien
   - Indicateurs au vert

2. **Alerte warning** 
   - Le traitement prend plus de 5 secondes (normalement < 1s)
   - → Email ou SMS envoyé : " Performance dégradée"

3. **Alerte critique** 
   - Le pipeline échoue complètement
   - → Notification immédiate : " Pipeline en échec, intervention requise"

### Tests de Simulation d'Erreurs

Le système peut **simuler des pannes** pour tester les alertes :

| Type d'Erreur | Simulation | Réaction du Système |
|---------------|------------|---------------------|
| **Connexion** | Le fichier n'est pas accessible |  Arrêt immédiat + alerte |
| **Validation** | Une ligne a un format invalide |  Ligne ignorée + warning |
| **Traitement** | Bug dans le code |  Arrêt + stacktrace dans les logs |

---

##  Le Déploiement Docker

### Pourquoi Docker ?

**Analogie** : Docker = Un **conteneur de transport maritime**

Sans Docker :
-  "Ça marche sur mon PC mais pas sur le serveur"
-  "Il manque une bibliothèque Python"
-  "La version n'est pas la bonne"

Avec Docker :
-  Tout est emballé dans le conteneur
-  Fonctionne partout de la même façon
-  Facile à démarrer : `docker compose up`

### Architecture Docker

```
 Conteneur 1 : Agent Datadog
   → Collecte les métriques
   → Envoie à Datadog Cloud
   
 Conteneur 2 : Pipeline Python
   → Lit le CSV
   → Transforme les données
   → Envoie les stats à l'agent
   
 Réseau Docker
   → Les 2 conteneurs communiquent
```

---

##  Images Suggérées

### 1. Architecture Simplifiée
Un schéma avec 3 boîtes et des flèches :
```
[ CSV Entrée] → [ Robot Python] → [ CSV Sortie]
                        ↓
                   [ Datadog]
```

### 2. Avant/Après
Capture côte à côte des fichiers CSV pour montrer la transformation

### 3. Dashboard Datadog
Tableau de bord coloré avec graphiques et indicateurs

### 4. Logs dans le Terminal
Terminal avec messages "Pipeline started" et "Pipeline finished successfully"

---

##  Résultats Concrets

### Performance

 **60 lignes traitées en 0.25 seconde**
- Équivalent de 240 lignes par seconde
- Temps de traitement moyen : 0.01 ms par ligne
- 100% de réussite

### Fiabilité

 **Système robuste avec 3 niveaux de protection** :
1. **Vérification avant traitement** : Le fichier existe-t-il ?
2. **Contrôle pendant** : Chaque ligne est-elle valide ?
3. **Validation après** : Le fichier de sortie est-il correct ?

### Traçabilité

 **Chaque exécution est identifiée** :
- ID unique : `exec:8469c7c5`
- Tous les logs et métriques sont liés
- Permet de retrouver ce qui s'est passé à un moment précis

---

##  Ce Que Ce Projet Démontre

### Compétences Techniques

1. **Automatisation** : Créer des processus qui tournent seuls
2. **Qualité** : Vérifier et valider les données
3. **Surveillance** : Savoir ce qui se passe en temps réel
4. **Containerisation** : Empaqueter une application pour la production

### Valeur Business

 **ROI (Retour sur Investissement)** :
- **Temps gagné** : Plus besoin de traiter manuellement
- **Fiabilité** : Moins d'erreurs humaines
- **Rapidité** : 240 lignes/seconde vs traitement manuel
- **Visibilité** : On sait toujours où on en est

### Évolutivité

 **Prêt pour la mise à l'échelle** :
-  Fonctionne sur 60 lignes
-  Peut traiter 60 000 lignes
-  Peut être déployé sur Azure Cloud
-  Peut tourner 24/7 automatiquement

---

##  Migration vers Azure Cloud

### La Prochaine Étape

Ce projet **local** (sur votre ordinateur) est la **maquette** d'un système **production** (dans le cloud).

**Analogie** : C'est comme construire une **maquette de pont** avant de construire le vrai pont !

### Correspondance Local → Cloud

|  Version Locale |  Version Cloud Azure |
|-------------------|----------------------|
| Script Python sur PC | Azure Data Factory |
| Fichier CSV local | Azure Blob Storage |
| Docker local | Azure Container Instances |
| Datadog Dashboard | Azure Monitor |

**Le code reste le même**, seul l'environnement change !

---

##  Section Technique Détaillée

###  Structure du projet

```
azure-data-factory/
├── data/
│   ├── input/
│   │   └── events.csv              # Données sources (60 événements)
│   └── output/
│       └── events_processed.csv    # Données enrichies
│
├── scripts/
│   └── transform.py               # Script de transformation principal
│
├── logs/                          # Logs de l'application
├── docker-compose.yml            # Orchestration des services
├── Dockerfile                    # Image Python du pipeline
├── entrypoint.sh                 # Script de démarrage
├── requirements.txt              # Dépendances Python
├── .env                         # Variables d'environnement
└── note.md                      # Documentation
```

---

##  Script de Transformation (transform.py)

### Vue d'ensemble

Script Python de 195 lignes qui implémente un pipeline ETL complet avec observabilité Datadog.

### Fonctionnalités principales

#### 1. **Initialisation et Configuration**

```python
# Génération d'un execution_id unique pour traçabilité
EXECUTION_ID = str(uuid.uuid4())[:8]

# Tags communs pour toutes les métriques
COMMON_TAGS = [
    f"pipeline:{PIPELINE_NAME}", 
    f"execution_id:{EXECUTION_ID}", 
    "env:dev"
]
```

#### 2. **Logging vers Datadog**

Custom handler pour envoyer les logs directement à Datadog Logs :

```python
class DatadogLogHandler(logging.Handler):
    def emit(self, record):
        log_entry = {
            "ddsource": "python",
            "ddtags": f"env:dev,service:adf-pipeline,execution_id:{execution_id}",
            "message": self.format(record),
            "execution_id": self.execution_id,
            "pipeline": PIPELINE_NAME
        }
        # POST vers https://http-intake.logs.datadoghq.eu/api/v2/logs
```

**Avantages** :
- Logs centralisés dans Datadog
- Corrélation automatique avec les métriques via `execution_id`
- Recherche et filtrage avancés

#### 3. **Lecture et Transformation CSV**

```python
with open("data/input/events.csv") as infile, \
     open("data/output/events_processed.csv", "w") as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ["processed_at", "pipeline"]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    for row in reader:
        # Enrichissement
        row["processed_at"] = datetime.now(timezone.utc).isoformat()
        row["pipeline"] = PIPELINE_NAME
        writer.writerow(row)
        
        # Métriques par record
        statsd.timing("pipeline.record_processing_time", duration_ms)
```

#### 4. **Comptage par type d'événement**

```python
event_types = {}  # Dictionnaire de comptage

for row in reader:
    event_type = row.get('event_type', 'unknown')
    event_types[event_type] = event_types.get(event_type, 0) + 1

# Envoi des métriques
for event_type, count in event_types.items():
    statsd.gauge("pipeline.events_by_type", count, 
                 tags=COMMON_TAGS + [f"event_type:{event_type}"])
```

#### 5. **Simulation d'erreurs (pour tests)**

```python
# Variables d'environnement
SIMULATE_ERROR = os.getenv("SIMULATE_ERROR", "false").lower() == "true"
ERROR_TYPE = os.getenv("ERROR_TYPE", "processing")

# Types d'erreurs simulables
if ERROR_TYPE == "connection":
    raise ConnectionError("Failed to connect to data source")
    
if ERROR_TYPE == "validation":
    # Erreur au 10ème enregistrement
    continue
    
if ERROR_TYPE == "processing":
    # Erreur au 30ème enregistrement
    raise ValueError("Cannot process record")
```

#### 6. **Métriques de performance**

```python
# Calcul des statistiques
avg_processing_time = sum(processing_times) / len(processing_times)
max_processing_time = max(processing_times)
min_processing_time = min(processing_times)
throughput = records / duration

# Envoi à Datadog
statsd.gauge("pipeline.throughput_records_per_second", throughput)
statsd.gauge("pipeline.avg_record_processing_time_ms", avg_time_ms)
statsd.gauge("pipeline.max_record_processing_time_ms", max_time_ms)
```

#### 7. **Métriques de qualité**

```python
error_rate = (errors / records * 100) if records > 0 else 0
success_rate = 100 - error_rate

statsd.gauge("pipeline.error_rate_percent", error_rate)
statsd.gauge("pipeline.success_rate_percent", success_rate)
statsd.gauge("pipeline.records_success", records - errors)
statsd.gauge("pipeline.records_errors", errors)
```

#### 8. **Gestion d'erreurs complète**

```python
try:
    # Traitement normal
    process_data()
    statsd.increment("pipeline.success", tags=COMMON_TAGS)
    
except Exception as e:
    error_type_name = type(e).__name__
    
    # Métriques d'échec enrichies
    statsd.increment("pipeline.error", 
                     tags=COMMON_TAGS + [f"error_type:{error_type_name}"])
    statsd.gauge("pipeline.records_before_failure", records)
    statsd.gauge("pipeline.completion_rate_percent", completion_rate)
    
    logging.error(f"Pipeline failed: {str(e)}", exc_info=True)
    raise
```

---

##  Métriques Datadog collectées

### Tableau complet des métriques

| Métrique | Type | Description | Tags |
|----------|------|-------------|------|
| `pipeline.started` | Counter | Démarrage du pipeline | pipeline, execution_id, env |
| `pipeline.success` | Counter | Pipeline terminé avec succès | pipeline, execution_id, env |
| `pipeline.error` | Counter | Pipeline en échec | pipeline, execution_id, env, error_type |
| `pipeline.records_processed` | Gauge | Nombre total d'enregistrements | pipeline, execution_id, env |
| `pipeline.records_success` | Gauge | Enregistrements traités avec succès | pipeline, execution_id, env |
| `pipeline.records_errors` | Gauge | Enregistrements en erreur | pipeline, execution_id, env |
| `pipeline.duration_seconds` | Gauge | Durée totale du pipeline (s) | pipeline, execution_id, env |
| `pipeline.throughput_records_per_second` | Gauge | Débit (records/sec) | pipeline, execution_id, env |
| `pipeline.record_processing_time` | Timing | Temps par enregistrement (ms) | pipeline, execution_id, env |
| `pipeline.avg_record_processing_time_ms` | Gauge | Temps moyen par record | pipeline, execution_id, env |
| `pipeline.max_record_processing_time_ms` | Gauge | Temps max par record | pipeline, execution_id, env |
| `pipeline.min_record_processing_time_ms` | Gauge | Temps min par record | pipeline, execution_id, env |
| `pipeline.error_rate_percent` | Gauge | Taux d'erreur (%) | pipeline, execution_id, env |
| `pipeline.success_rate_percent` | Gauge | Taux de succès (%) | pipeline, execution_id, env |
| `pipeline.events_by_type` | Gauge | Compteur par type d'événement | pipeline, execution_id, env, event_type |
| `pipeline.completion_rate_percent` | Gauge | Taux de complétion avant échec | pipeline, execution_id, env |
| `pipeline.records_before_failure` | Gauge | Records traités avant échec | pipeline, execution_id, env |
| `pipeline.connection_error` | Counter | Erreurs de connexion | pipeline, execution_id, env |
| `pipeline.validation_error` | Counter | Erreurs de validation | pipeline, execution_id, env, event_type |
| `pipeline.processing_error` | Counter | Erreurs de traitement | pipeline, execution_id, env |

### Types de métriques

- **Counter** : Incrémenté à chaque occurrence (succès, erreurs)
- **Gauge** : Valeur instantanée (nombre de records, durée)
- **Timing** : Distribution de temps (processing time par record)

---

##  Configuration Docker complète

### docker-compose.yml

```yaml
services:
  # Agent Datadog pour collecte des métriques et logs
  dd-agent:
    image: gcr.io/datadoghq/agent:7
    container_name: dd-agent-adf
    environment:
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=${DD_SITE:-datadoghq.eu}
      - DD_HOSTNAME=docker-host
      - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true  # Accepte métriques des containers
      - DD_APM_ENABLED=true
      - DD_LOGS_ENABLED=true
      - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
    networks:
      - pipeline-network
    healthcheck:
      test: ["CMD", "agent", "health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Pipeline ETL Python
  adf-pipeline:
    build: .
    container_name: adf-pipeline
    environment:
      - DD_AGENT_HOST=dd-agent           # Nom du service agent
      - DD_STATSD_PORT=8125
      - DD_API_KEY=${DD_API_KEY}
      - DD_SITE=${DD_SITE:-datadoghq.eu}
      - PIPELINE_NAME=${PIPELINE_NAME:-docker-adf-pipeline}
      - ENV=${ENV:-dev}
      - SIMULATE_ERROR=${SIMULATE_ERROR:-false}
      - ERROR_TYPE=${ERROR_TYPE:-processing}
    volumes:
      - ./data/output:/app/data/output
      - ./logs:/app/logs
    depends_on:
      dd-agent:
        condition: service_healthy        # Attend que l'agent soit prêt
    networks:
      - pipeline-network

networks:
  pipeline-network:
    driver: bridge
```

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Installation des dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie des fichiers
COPY scripts/ ./scripts/
COPY data/input/ ./data/input/
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

# Création des dossiers
RUN mkdir -p data/output logs

CMD ["./entrypoint.sh"]
```

### requirements.txt

```txt
datadog==0.49.1
python-dotenv==1.0.0
requests==2.31.0
```

### Variables d'environnement (.env)

```env
# Datadog
DD_API_KEY=votre_cle_api_datadog
DD_SITE=datadoghq.eu

# Pipeline
PIPELINE_NAME=docker-adf-pipeline
ENV=dev

# Simulation d'erreurs (pour tests)
SIMULATE_ERROR=false
ERROR_TYPE=processing  # connection, validation, processing
```

---

##  Commandes de démarrage

### Exécution normale

```bash
cd azure-data-factory

# Créer le fichier .env
cp .env.example .env
# Éditer .env avec votre clé API Datadog

# Lancer le pipeline
docker-compose up --build

# Voir les logs en temps réel
docker-compose logs -f adf-pipeline

# Arrêter
docker-compose down
```

### Tests de simulation d'erreurs

#### 1. Erreur de connexion
```bash
# Modifier .env
SIMULATE_ERROR=true
ERROR_TYPE=connection

docker-compose up

# Résultat attendu :
# - Pipeline échoue immédiatement
# - Métrique: pipeline.connection_error = 1
# - Logs: "Connection to data source failed"
```

#### 2. Erreur de validation
```bash
SIMULATE_ERROR=true
ERROR_TYPE=validation

docker-compose up

# Résultat attendu :
# - Pipeline continue malgré l'erreur
# - 1 enregistrement ignoré (le 10ème)
# - Métrique: pipeline.validation_error = 1
# - pipeline.records_success = 59 (au lieu de 60)
```

#### 3. Erreur de processing
```bash
SIMULATE_ERROR=true
ERROR_TYPE=processing

docker-compose up

# Résultat attendu :
# - Pipeline échoue au 30ème enregistrement
# - Métrique: pipeline.records_before_failure = 30
# - Métrique: pipeline.completion_rate_percent = 50%
# - Logs: "Processing error at record 30"
```

---

##  Dashboards et Monitoring

### Widgets recommandés pour Datadog

#### 1. Pipeline Executions (Timeseries)
- Métrique : `pipeline.started` (counter - rate)
- Visualisation : Line chart
- Permet de voir le nombre d'exécutions par heure/jour

#### 2. Success vs Error Rate (Query Value)
- Métrique : `pipeline.success_rate_percent`
- Visualisation : Gauge avec threshold
- Vert > 95%, Jaune > 90%, Rouge < 90%

#### 3. Throughput (Query Value)
- Métrique : `pipeline.throughput_records_per_second`
- Visualisation : Big Number
- Affiche les records/seconde

#### 4. Processing Time Distribution (Timeseries)
- Métriques :
  - `pipeline.avg_record_processing_time_ms` (moyenne)
  - `pipeline.max_record_processing_time_ms` (max)
  - `pipeline.min_record_processing_time_ms` (min)
- Visualisation : Multi-line chart

#### 5. Events by Type (Pie Chart)
- Métrique : `pipeline.events_by_type`
- Group by : `event_type`
- Visualisation : Donut chart
- Montre la répartition login/logout/error

#### 6. Error Rate Trend (Timeseries)
- Métrique : `pipeline.error_rate_percent`
- Visualisation : Area chart avec threshold rouge à 5%

#### 7. Recent Executions (Table)
- Métriques :
  - `pipeline.records_processed`
  - `pipeline.duration_seconds`
  - `pipeline.success_rate_percent`
- Group by : `execution_id`
- Top 10 dernières exécutions

#### 8. Logs Stream
- Source : Logs
- Query : `service:adf-pipeline`
- Colonnes : timestamp, status, message, execution_id
- Live tail activé

---

##  Monitors et Alertes recommandés

### 1. Monitor : Pipeline Failure

```
Metric: pipeline.error (counter)
Condition: sum > 0 for 1 evaluation
Alert message: 
  " Pipeline {{pipeline.name}} failed
   Execution ID: {{execution_id.name}}
   Error type: {{error_type.name}}"
Priority: Critical
```

### 2. Monitor : High Error Rate

```
Metric: pipeline.error_rate_percent
Condition: > 5% for 2 consecutive evaluations
Alert message:
  " Error rate is {{value}}% (threshold: 5%)
   Pipeline: {{pipeline.name}}"
Priority: High
```

### 3. Monitor : Slow Processing

```
Metric: pipeline.duration_seconds
Condition: > 5 seconds for 3 evaluations
Alert message:
  " Pipeline duration is {{value}}s (expected < 1s)
   Execution ID: {{execution_id.name}}"
Priority: Medium
```

### 4. Monitor : Low Throughput

```
Metric: pipeline.throughput_records_per_second
Condition: < 100 for 2 evaluations
Alert message:
  " Throughput is {{value}} records/sec (expected > 200)"
Priority: Low
```

### 5. Monitor : No Execution

```
Metric: pipeline.started (counter)
Condition: no data for 1 hour
Alert message:
  " No pipeline execution detected in the last hour"
Priority: Medium
```

---

##  Validation des résultats

### Vérification des fichiers

```bash
# Compter les lignes input
wc -l data/input/events.csv
# Résultat : 61 (60 + header)

# Compter les lignes output
wc -l data/output/events_processed.csv
# Résultat : 61 (60 + header)

# Vérifier l'enrichissement
head -n 3 data/output/events_processed.csv
# Colonnes supplémentaires: processed_at, pipeline
```

### Vérification des métriques dans Datadog

```bash
# Recherche dans Metrics Explorer
pipeline.records_processed{pipeline:docker-adf-pipeline}
# Valeur attendue : 60

pipeline.success_rate_percent{pipeline:docker-adf-pipeline}
# Valeur attendue : 100.0

pipeline.duration_seconds{pipeline:docker-adf-pipeline}
# Valeur attendue : ~0.25s
```

### Vérification des logs dans Datadog

```bash
# Recherche dans Logs Explorer
service:adf-pipeline execution_id:*

# Logs attendus :
# - "Pipeline docker-adf-pipeline started"
# - "→ login: X events"
# - "→ logout: Y events"  
# - "→ error: Z events"
# - "Pipeline finished successfully"
```

---

##  Cas d'usage et extensions

### Migration vers Azure Cloud

| Composant Local | Équivalent Azure | Migration |
|-----------------|------------------|-----------|
| `transform.py` | Azure Data Factory Pipeline | Copier la logique dans Copy Activity + Data Flow |
| CSV local | Azure Blob Storage | Upload via Azure Storage Explorer |
| Docker | Azure Container Instances | Déployer l'image Docker |
| Datadog | Azure Monitor | Intégration Datadog-Azure ou migration complète |

### Extensions possibles

#### Court terme
- [ ] Ajouter plus de transformations (filtres, agrégations)
- [ ] Implémenter la validation des données (schéma)
- [ ] Ajouter des tests unitaires (pytest)
- [ ] Créer un dashboard Datadog complet

#### Moyen terme
- [ ] Planification avec Azure Data Factory Triggers
- [ ] Intégration avec Azure Blob Storage
- [ ] Pipeline multi-étapes (ingestion → transformation → chargement)
- [ ] Gestion des échecs et retry logic

#### Long terme
- [ ] Migration complète vers Azure Data Factory
- [ ] Intégration avec Azure Synapse Analytics
- [ ] Data lineage et governance
- [ ] CI/CD avec Azure DevOps

---

##  Ressources techniques

### Azure Data Factory
- [Documentation officielle](https://learn.microsoft.com/azure/data-factory/)
- [Tutoriels](https://learn.microsoft.com/azure/data-factory/tutorial-copy-data-portal)
- [Best Practices](https://learn.microsoft.com/azure/data-factory/concepts-data-flow-best-practices)

### Datadog
- [Python Integration](https://docs.datadoghq.com/developers/community/libraries/)
- [DogStatsD](https://docs.datadoghq.com/developers/dogstatsd/)
- [Log Management](https://docs.datadoghq.com/logs/)

### Docker
- [Best practices](https://docs.docker.com/develop/dev-best-practices/)
- [Docker Compose](https://docs.docker.com/compose/)

---

##  Checklist de vérification

### Code Quality
- [x] Variables d'environnement pour configuration
- [x] Logging structuré avec contexte
- [x] Gestion d'erreurs complète avec try/except
- [x] Métriques sur tous les points critiques
- [x] Tags cohérents sur toutes les métriques
- [x] Documentation inline (docstrings)

### Observabilité
- [x] Métriques de volumétrie (records traités)
- [x] Métriques de performance (durée, throughput)
- [x] Métriques de qualité (error rate, success rate)
- [x] Métriques métier (events by type)
- [x] Logs centralisés dans Datadog
- [x] Corrélation logs/métriques via execution_id

### Infrastructure
- [x] Docker multi-services (agent + pipeline)
- [x] Health checks configurés
- [x] Volumes pour persistance
- [x] Réseau Docker dédié
- [x] Variables d'environnement externalisées

### Tests
- [x] Test nominal (60 records, 0 erreur)
- [x] Test erreur connexion
- [x] Test erreur validation
- [x] Test erreur processing
- [x] Vérification métriques Datadog

---

##  À Qui Ça Sert ?

### Cas d'Usage Réels

1. **Service RH** : Traiter automatiquement les relevés de présence
2. **Service Finance** : Consolider les rapports de ventes journaliers
3. **Service IT** : Analyser les logs de connexion
4. **Service Client** : Extraire les statistiques de satisfaction

### Exemple Concret Mercedes-Benz

Imaginons l'utilisation dans un contexte automobile :
- **Entrée** : Logs des capteurs de camions (température, vitesse, GPS)
- **Traitement** : Enrichissement avec données météo et trafic
- **Sortie** : Alertes prédictives de maintenance
- **Surveillance** : Dashboard temps réel du parc de véhicules

---

##  Livrables du Projet

### Ce Qui Est Fourni

-  **Code source complet** : Prêt à être exécuté
-  **Configuration Docker** : Déploiement en 1 commande
-  **Documentation détaillée** : Comment l'utiliser
-  **Exemples de données** : Pour tester immédiatement
-  **Logs et métriques** : Visibles dans Datadog

### Comment L'Utiliser

```bash
# 1. Télécharger le projet
git clone [repo]

# 2. Configurer votre clé Datadog
# Éditer le fichier .env

# 3. Lancer
docker compose up

# 4. Voir les résultats
# → Fichier : data/output/events_processed.csv
# → Dashboard : app.datadoghq.eu
```

---

##  Points Clés à Retenir

### En 3 Phrases

1.  **Un robot lit un fichier, ajoute des infos utiles, et crée un nouveau fichier**
2.  **Un système de surveillance (Datadog) vérifie que tout fonctionne bien**
3.  **Tout est empaqueté dans Docker pour fonctionner partout de la même façon**

### Pourquoi C'est Important

-  **Pour l'entreprise** : Gain de temps et fiabilité
-  **Pour l'apprentissage** : Comprendre les pipelines de données modernes
-  **Pour la carrière** : Compétences demandées en DevOps/Data Engineering

---

##  Auteur

**Juvet**  
DevOps Engineer – Mercedes-Benz Trucks Molsheim

*Projet réalisé dans le cadre du Bootcamp Observabilité & Data*  
*Période : 27 décembre 2025 → 19 janvier 2026*
