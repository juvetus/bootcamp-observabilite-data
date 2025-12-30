# 🐳 Azure Data Factory Pipeline - Docker Deployment

## Prérequis

- Docker Desktop installé
- Clé API Datadog

## 🚀 Démarrage Rapide

### 1. Configurer les variables d'environnement

Assurez-vous que votre fichier `.env` contient votre clé API :

```bash
DD_API_KEY=votre_cle_api_datadog
DD_SITE=datadoghq.eu
PIPELINE_NAME=docker-adf-pipeline
ENV=dev
SIMULATE_ERROR=false
ERROR_TYPE=processing
```

### 2. Lancer le pipeline avec Docker Compose

```bash
# Démarrer l'agent Datadog et le pipeline
docker-compose up

# Ou en arrière-plan
docker-compose up -d

# Voir les logs
docker-compose logs -f adf-pipeline
```

### 3. Arrêter les conteneurs

```bash
docker-compose down
```

## 🎮 Utilisation

### Exécution normale

```bash
docker-compose up adf-pipeline
```

### Simuler des erreurs

```bash
# Erreur de processing
SIMULATE_ERROR=true ERROR_TYPE=processing docker-compose up adf-pipeline

# Erreur de validation
SIMULATE_ERROR=true ERROR_TYPE=validation docker-compose up adf-pipeline

# Erreur de connexion
SIMULATE_ERROR=true ERROR_TYPE=connection docker-compose up adf-pipeline
```

### Réexécuter le pipeline

```bash
docker-compose restart adf-pipeline
```

### Reconstruire l'image après modification du code

```bash
docker-compose build adf-pipeline
docker-compose up adf-pipeline
```

## 📂 Volumes Montés

- `./data/output` → Fichiers CSV générés
- `./logs` → Logs du pipeline

## 🔍 Debugging

### Voir les logs en temps réel

```bash
# Logs du pipeline
docker-compose logs -f adf-pipeline

# Logs de l'agent Datadog
docker-compose logs -f dd-agent
```

### Inspecter un conteneur

```bash
docker exec -it adf-pipeline /bin/bash
```

### Vérifier le statut de l'agent Datadog

```bash
docker exec -it dd-agent-adf agent status
```

## 🌐 Réseau

Les conteneurs communiquent via le réseau `pipeline-network` :
- Pipeline → Agent Datadog (StatsD sur port 8125)
- Pipeline → API Datadog (HTTPS pour les logs)

## 📊 Métriques et Logs dans Datadog

Une fois lancé, vérifiez dans Datadog :

**Logs** :
```
service:adf-pipeline env:dev
```

**Métriques** :
```
pipeline.records_processed{pipeline:docker-adf-pipeline}
```

## 🔧 Personnalisation

### Modifier les variables d'environnement

Éditez `docker-compose.yml` ou créez un fichier `.env` :

```env
PIPELINE_NAME=mon-pipeline
ENV=production
```

### Ajouter des dépendances Python

1. Modifiez `requirements.txt`
2. Rebuild l'image : `docker-compose build`

## 🎯 Avantages du Déploiement Docker

✅ Isolation complète  
✅ Reproductibilité  
✅ Facile à orchestrer  
✅ Prêt pour Kubernetes  
✅ Monitoring intégré avec Datadog  

## 🚀 Prochaines Étapes

- Ajouter un scheduler (cron) pour exécutions périodiques
- Déployer sur Kubernetes avec Helm
- Intégrer CI/CD (GitHub Actions)
- Ajouter des health checks
