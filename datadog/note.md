# 📊 Datadog – Observabilité Infrastructure & Containers

---

## 📋 Résumé Exécutif

Ce document présente la mise en place d'un système de surveillance informatique complet pour garantir le bon fonctionnement de serveurs et d'applications.

**Ce qui a été réalisé :**

1. **Surveillance des serveurs** 🖥️
   - Installation d'un "agent" (programme de surveillance) sur le serveur
   - Mesure en temps réel de l'utilisation du processeur, de la mémoire et du disque dur
   - Création d'alertes automatiques quand les ressources atteignent des seuils critiques (ex: CPU > 80%)

2. **Surveillance d'une application Flask** 🐍
   - Instrumentation d'une application web Python pour tracer son comportement
   - Détection automatique des ralentissements et des erreurs
   - Corrélation entre les logs (journaux) et les performances

3. **Tableaux de bord** 📊
   - Interface visuelle pour voir en un coup d'œil l'état de santé du système
   - Graphiques des métriques importantes avec seuils d'alerte colorés
   - Historique des événements pour comprendre les incidents

**Bénéfices :**
- Détection rapide des problèmes avant qu'ils n'impactent les utilisateurs
- Capacité à diagnostiquer les causes racines d'une panne
- Visibilité complète sur l'infrastructure et les applications

---

## 🎯 Objectif

Mettre en place une solution d'observabilité avec Datadog afin de :
- superviser les ressources système (CPU, mémoire, disque)
- monitorer les containers Docker
- configurer des alertes pertinentes
- construire un dashboard exploitable en contexte production

---

## 📸 Captures d'écran

### Dashboard Datadog

Le dashboard personnalisé regroupe l'ensemble des métriques critiques pour l'observabilité de l'infrastructure :

#### Vue d'ensemble
![Dashboard Datadog](./images/dashboard.png)

#### Container CPU Usage
Surveillance de l'utilisation CPU par container Docker avec seuils d'alerte (saturation à 80%, alerte haute à 60%).

![Container CPU Usage](./images/container-cpu-usage.png)

#### Container Memory Usage
Monitoring de la consommation mémoire des containers avec calcul du ratio utilisation/limite et détection des risques de saturation.

![Container Memory Usage](./images/container-memory-usage.png)

#### Disk Usage
Suivi de l'utilisation disque par device sur l'hôte `juvet-rancher` avec seuil critique à 95%.

![Disk Usage](./images/disk-usage.png)

#### Host Memory Usage
Analyse de la mémoire système avec indication du niveau critique (80%) et zone d'avertissement (warning).

![Host Memory Usage](./images/host-memory-usage.png)

#### Host CPU Usage (User vs System)
Comparaison entre CPU utilisateur et CPU système pour identifier les goulots d'étranglement.

![Host CPU Usage](./images/host-cpu-usage.png)

### Agent Status
![Agent Status](./images/agent-status.png)

---

## 🌍 Contexte

- **Outil** : Datadog (Agent v7)
- **Environnement** :
   - Ubuntu 24.04 LTS
   - WSL2
   - Rancher Desktop (Docker + Kubernetes local)
- **Périmètre observé** :
   - Host Docker (`juvet-rancher`)
   - Containers locaux
- **Datadog Site** : `datadoghq.eu`

---

## ⚙️ Implémentation

### Installation de l'agent Datadog (Docker)

L'agent Datadog a été déployé sous forme de container Docker, solution la plus adaptée à un environnement WSL / Rancher Desktop.

```bash
docker run -d --name dd-agent \
   -e DD_API_KEY=<API_KEY> \
   -e DD_SITE=datadoghq.eu \
   -e DD_HOSTNAME=juvet-rancher \
   -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true \
   -e DD_NETWORK_ENABLED=false \
   -v /var/run/docker.sock:/var/run/docker.sock:ro \
   -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
   -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
   gcr.io/datadoghq/agent:7
```

**Choix techniques :**
- Agent Docker plutôt que bare-metal pour éviter les problèmes de hostname sous WSL
- Désactivation du network check (`DD_NETWORK_ENABLED=false`) pour éviter l'erreur `/host/proc/net/dev`
- Hostname forcé pour cohérence dashboards / alertes

### Vérification de l'agent

```bash
docker exec -it dd-agent agent status
```

**Résultat :**
- Agent connecté à Datadog
- Métriques système collectées
- Containers détectés
- Events Docker visibles

---

## 📊 Dashboard Datadog

Création d'un dashboard personnalisé avec une approche progressive :

### Widgets implémentés
- CPU Usage (%) avec threshold
- CPU Saturation (%) via formule
- Memory Usage
- Memory Saturation
- Disk Usage
- Container Restarts
- Event Stream (Docker & Agent)

**Objectif** : passer de la métrique brute à une lecture claire des incidents.

---

## 🚨 Alerting

### Monitor CPU – High Usage

- **Métrique** : `system.cpu.user`
- **Scope** : `host:juvet-rancher`
- **Condition** : > 80 % sur 5 minutes
- **Options** :
   - Require full window
   - Pas d'alerte en cas de données manquantes

**Message :**
```
High CPU usage detected on {{host.name}}
CPU usage has been above 80% for more than 5 minutes.
```

---

## 📌 Résultat

- Supervision complète de l'hôte Docker
- Visibilité claire sur l'activité des containers
- Alertes pertinentes et exploitables
- Corrélation métriques / événements facilitant le diagnostic

**Livrables :**
- Dashboard Datadog
- Widgets avec seuils
- Monitor CPU
- Captures d'écran associées

---

## 🧠 Ce que j'ai appris

### Concepts clés
- Observabilité vs monitoring
- Architecture de l'agent Datadog
- Métriques infrastructure et containers
- Construction de dashboards orientés exploitation

### Bonnes pratiques
- Définir des seuils réalistes
- Ajouter du contexte via les événements
- Adapter l'agent à l'environnement (WSL, Docker)
- Nommer clairement dashboards et alertes

### Points à approfondir
- APM et traces distribuées
- Centralisation des logs
- Intégration Kubernetes avancée
- Alertes multi-dimensionnelles

---

# 📝 Application Flask – APM et Observabilité Applicative

## Objectif

Mettre en place une observabilité complète (APM, Logs, Metrics) pour une application Flask conteneurisée avec Datadog.

---

## Stack technique

* Python 3.11 / Flask
* Docker & Docker Compose
* Datadog Agent (APM, Logs, Runtime Metrics)

---

## Application

Endpoints exposés :

* `/` : endpoint nominal
* `/slow` : requête lente simulée
* `/error` : génération d'une erreur 500

---

## 📸 Captures Datadog

### APM – Service Flask
![APM Service](images/apm-service.png)

### Traces
![Trace Flask](images/trace.png)

### Runtime Metrics
![Runtime Metrics](images/runtime-metrics.png)

### Dashboard
![Dashboard](images/dashboard.png)

---

## Instrumentation Datadog

### Dépendances

```txt
flask
ddtrace
```

### Commande de lancement

```bash
ddtrace-run python app.py
```

### Variables Datadog clés

```env
DD_SERVICE=flask-demo-bootcamp
DD_ENV=dev
DD_VERSION=1.0
DD_AGENT_HOST=dd-agent
DD_TRACE_AGENT_PORT=8126
DD_TRACE_ENABLED=true
DD_LOGS_INJECTION=true
DD_RUNTIME_METRICS_ENABLED=true
DD_RUNTIME_METRICS_RUNTIME_ID_ENABLED=true
DD_PROFILING_ENABLED=true
```

---

## Datadog Agent

Fonctionnalités actives :

* APM (traces)
* Logs Docker
* Runtime Metrics Python

Vérification :

```bash
docker exec -it dd-agent agent status
```

---

## Observabilité obtenue

### APM

* Traces par endpoint Flask
* Flamegraph et Waterfall
* Détection automatique des erreurs 500
* Mesures de latence (P95)

### Logs

* Logs applicatifs Flask
* Corrélation Logs ↔ Traces (trace_id)

### Runtime Metrics

* CPU Python
* Garbage Collection
* Context Switches
* Corrélation directe avec les traces

---

## Dashboards

Indicateurs suivis :

* Nombre de requêtes
* Taux d'erreur
* Latence P95
* Erreurs par statut HTTP

---

## Résultat

L'application est entièrement observable :

* Détection rapide des erreurs
* Analyse de performance par trace
* Diagnostic facilité via logs corrélés

---

## Conclusion

Ce projet valide la mise en place d'une chaîne d'observabilité moderne avec Datadog sur une application Python Flask.

---

📌 **Prochaines étapes possibles**

* Création de SLO
* Mise en place d'alertes (monitors)
* Ajout du profiling continu


## 🌍 Contexte

- **Outil** : Datadog (Agent v7)
- **Environnement** :
   - Ubuntu 24.04 LTS
   - WSL2
   - Rancher Desktop (Docker + Kubernetes local)
- **Périmètre observé** :
   - Host Docker (`juvet-rancher`)
   - Containers locaux
- **Datadog Site** : `datadoghq.eu`

---

## ⚙️ Implémentation

### Installation de l'agent Datadog (Docker)

L'agent Datadog a été déployé sous forme de container Docker, solution la plus adaptée à un environnement WSL / Rancher Desktop.

```bash
docker run -d --name dd-agent \
   -e DD_API_KEY=<API_KEY> \
   -e DD_SITE=datadoghq.eu \
   -e DD_HOSTNAME=juvet-rancher \
   -e DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true \
   -e DD_NETWORK_ENABLED=false \
   -v /var/run/docker.sock:/var/run/docker.sock:ro \
   -v /sys/fs/cgroup/:/host/sys/fs/cgroup:ro \
   -v /var/lib/docker/containers:/var/lib/docker/containers:ro \
   gcr.io/datadoghq/agent:7
```

**Choix techniques :**
- Agent Docker plutôt que bare-metal pour éviter les problèmes de hostname sous WSL
- Désactivation du network check (`DD_NETWORK_ENABLED=false`) pour éviter l'erreur `/host/proc/net/dev`
- Hostname forcé pour cohérence dashboards / alertes

### Vérification de l'agent

```bash
docker exec -it dd-agent agent status
```

**Résultat :**
- Agent connecté à Datadog
- Métriques système collectées
- Containers détectés
- Events Docker visibles

---

## 📊 Dashboard Datadog

Création d'un dashboard personnalisé avec une approche progressive :

### Widgets implémentés
- CPU Usage (%) avec threshold
- CPU Saturation (%) via formule
- Memory Usage
- Memory Saturation
- Disk Usage
- Container Restarts
- Event Stream (Docker & Agent)

**Objectif** : passer de la métrique brute à une lecture claire des incidents.

---

## 🚨 Alerting

### Monitor CPU – High Usage

- **Métrique** : `system.cpu.user`
- **Scope** : `host:juvet-rancher`
- **Condition** : > 80 % sur 5 minutes
- **Options** :
   - Require full window
   - Pas d'alerte en cas de données manquantes

**Message :**
```
High CPU usage detected on {{host.name}}
CPU usage has been above 80% for more than 5 minutes.
```

---

## 📌 Résultat

- Supervision complète de l'hôte Docker
- Visibilité claire sur l'activité des containers
- Alertes pertinentes et exploitables
- Corrélation métriques / événements facilitant le diagnostic

**Livrables :**
- Dashboard Datadog
- Widgets avec seuils
- Monitor CPU
- Captures d'écran associées

---

## 🧠 Ce que j'ai appris

### Concepts clés
- Observabilité vs monitoring
- Architecture de l'agent Datadog
- Métriques infrastructure et containers
- Construction de dashboards orientés exploitation

### Bonnes pratiques
- Définir des seuils réalistes
- Ajouter du contexte via les événements
- Adapter l'agent à l'environnement (WSL, Docker)
- Nommer clairement dashboards et alertes

### Points à approfondir
- APM et traces distribuées
- Centralisation des logs
- Intégration Kubernetes avancée
- Alertes multi-dimensionnelles
