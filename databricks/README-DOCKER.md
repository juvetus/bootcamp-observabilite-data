# 🚀 Databricks Spark Job - Docker

## ❌ Problème Windows

PySpark ne fonctionne pas nativement sur Windows car il utilise des composants Unix.

## ✅ Solution : Docker

### Lancer le job Spark

```bash
# Construire l'image
docker-compose build

# Exécuter le job
docker-compose up

# Voir les résultats
ls output/truck_metrics/
```

### Alternative : WSL

Si vous préférez utiliser WSL :

```bash
# Dans WSL (Ubuntu)
cd /mnt/c/DevOps/Bootcamp-Observabilite/databricks

# Installer les dépendances
pip install -r requirements.txt

# Lancer le job
python3 scripts/spark_job.py
```

## 📊 Résultats

Les fichiers Parquet seront générés dans `output/truck_metrics/`
