# ☁️ Azure Data Factory – Automatisation du Traitement de Données

---

## 📋 Résumé Simple

**Imaginez une usine de traitement de données** : des informations brutes entrent d'un côté, elles sont nettoyées et enrichies au milieu, puis ressortent propres et utilisables de l'autre côté. C'est exactement ce que fait ce projet !

### 🎬 L'Analogie de la Chaîne de Production

Pensez à une **chaîne de montage automobile** :
1. 🚗 **Entrée** : Les pièces brutes arrivent (nos fichiers CSV)
2. 🔧 **Transformation** : Les ouvriers assemblent et ajoutent des composants (notre script Python)
3. ✅ **Sortie** : Une voiture complète sort de la chaîne (fichier enrichi)
4. 📊 **Contrôle qualité** : Des inspecteurs vérifient chaque étape (Datadog)

---

## 🎯 Ce Qui a Été Fait

### 1. Création d'un Robot de Traitement de Données 🤖

**En termes simples** : Un programme qui lit automatiquement un fichier Excel (CSV), ajoute des informations utiles, et crée un nouveau fichier.

**Exemple concret** :
- **Avant** : `alice, login, 10:00`
- **Après** : `alice, login, 10:00, traité le 30/12/2025 à 13:00, par pipeline-adf`

C'est comme un tampon qui marque "Vu et vérifié" sur chaque ligne du document.

### 2. Installation d'un Système de Surveillance 👁️

**Datadog** = Un tableau de bord comme celui d'une voiture qui montre :
- ⏱️ Combien de temps ça prend
- 📊 Combien de lignes ont été traitées
- ✅ Si tout s'est bien passé ou s'il y a eu des erreurs
- 🔔 Des alertes si quelque chose ne va pas

### 3. Mise en Boîte avec Docker 📦

**Docker** = Une boîte magique qui contient tout le nécessaire pour faire fonctionner notre robot :
- Le programme Python (le cerveau)
- Les outils nécessaires (les mains)
- La configuration (le mode d'emploi)

**Avantage** : On peut transporter cette boîte partout et elle fonctionnera de la même manière !

---

## 🌍 Le Contexte Technique (Vulgarisé)

### Les Outils Utilisés

| Outil | Analogie | À Quoi Ça Sert |
|-------|----------|-----------------|
| **Python** | Le chef cuisinier | Suit la recette pour transformer les données |
| **CSV** | Un tableau Excel | Format simple pour stocker des données |
| **Datadog** | Caméras de surveillance | Surveille que tout fonctionne bien |
| **Docker** | Boîte hermétique | Garantit que ça marche partout pareil |
| **Azure Data Factory** | Usine dans le cloud | Version professionnelle hébergée chez Microsoft |

---

## 🔄 Comment Ça Marche ?

### Le Processus en 3 Étapes

```
📥 ENTRÉE                    🔧 TRAITEMENT                    📤 SORTIE
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
- ⏰ **date_traitement** : Quand le fichier a été traité (pour traçabilité)
- 🏷️ **source_pipeline** : Quel robot a fait le travail (pour l'audit)

---

## 📊 Les Métriques : Voir Ce Qui Se Passe

### Tableau de Bord (Dashboard)

Imaginez le **compteur kilométrique d'une voiture** qui affiche :

| 🎯 Métrique | 📝 Signification | 🔢 Exemple |
|------------|-----------------|-----------|
| **Records traités** | Nombre de lignes lues | 60 lignes |
| **Durée** | Temps pour tout traiter | 0.25 seconde |
| **Taux de succès** | Pourcentage sans erreur | 100% ✅ |
| **Vitesse** | Lignes par seconde | 240 lignes/sec |
| **Erreurs** | Nombre de problèmes | 0 erreur |

### Graphiques Visuels

Dans Datadog, vous voyez des **graphiques en temps réel** comme :
- 📈 Une courbe de la vitesse de traitement
- 🍩 Un camembert des types d'événements (login vs logout vs error)
- 🚦 Des feux tricolores : vert = OK, rouge = problème

---

## 🚨 Système d'Alerte Intelligent

### Comment Ça Fonctionne ?

C'est comme une **alarme incendie** dans un bâtiment :

1. **Situation normale** 🟢
   - Le pipeline tourne
   - Tout fonctionne bien
   - Indicateurs au vert

2. **Alerte warning** 🟡
   - Le traitement prend plus de 5 secondes (normalement < 1s)
   - → Email ou SMS envoyé : "⚠️ Performance dégradée"

3. **Alerte critique** 🔴
   - Le pipeline échoue complètement
   - → Notification immédiate : "🚨 Pipeline en échec, intervention requise"

### Tests de Simulation d'Erreurs

Le système peut **simuler des pannes** pour tester les alertes :

| Type d'Erreur | Simulation | Réaction du Système |
|---------------|------------|---------------------|
| **Connexion** | Le fichier n'est pas accessible | ❌ Arrêt immédiat + alerte |
| **Validation** | Une ligne a un format invalide | ⚠️ Ligne ignorée + warning |
| **Traitement** | Bug dans le code | ❌ Arrêt + stacktrace dans les logs |

---

## 🐳 Le Déploiement Docker

### Pourquoi Docker ?

**Analogie** : Docker = Un **conteneur de transport maritime**

Sans Docker :
- ❌ "Ça marche sur mon PC mais pas sur le serveur"
- ❌ "Il manque une bibliothèque Python"
- ❌ "La version n'est pas la bonne"

Avec Docker :
- ✅ Tout est emballé dans le conteneur
- ✅ Fonctionne partout de la même façon
- ✅ Facile à démarrer : `docker compose up`

### Architecture Docker

```
🐳 Conteneur 1 : Agent Datadog
   → Collecte les métriques
   → Envoie à Datadog Cloud
   
🐳 Conteneur 2 : Pipeline Python
   → Lit le CSV
   → Transforme les données
   → Envoie les stats à l'agent
   
🌐 Réseau Docker
   → Les 2 conteneurs communiquent
```

---

## 📸 Images Suggérées

### 1. Architecture Simplifiée
Un schéma avec 3 boîtes et des flèches :
```
[📄 CSV Entrée] → [🤖 Robot Python] → [📄 CSV Sortie]
                        ↓
                   [📊 Datadog]
```

### 2. Avant/Après
Capture côte à côte des fichiers CSV pour montrer la transformation

### 3. Dashboard Datadog
Tableau de bord coloré avec graphiques et indicateurs

### 4. Logs dans le Terminal
Terminal avec messages "Pipeline started" et "Pipeline finished successfully"

---

## ✅ Résultats Concrets

### Performance

🎯 **60 lignes traitées en 0.25 seconde**
- Équivalent de 240 lignes par seconde
- Temps de traitement moyen : 0.01 ms par ligne
- 100% de réussite

### Fiabilité

🛡️ **Système robuste avec 3 niveaux de protection** :
1. **Vérification avant traitement** : Le fichier existe-t-il ?
2. **Contrôle pendant** : Chaque ligne est-elle valide ?
3. **Validation après** : Le fichier de sortie est-il correct ?

### Traçabilité

📋 **Chaque exécution est identifiée** :
- ID unique : `exec:8469c7c5`
- Tous les logs et métriques sont liés
- Permet de retrouver ce qui s'est passé à un moment précis

---

## 🎓 Ce Que Ce Projet Démontre

### Compétences Techniques

1. **Automatisation** : Créer des processus qui tournent seuls
2. **Qualité** : Vérifier et valider les données
3. **Surveillance** : Savoir ce qui se passe en temps réel
4. **Containerisation** : Empaqueter une application pour la production

### Valeur Business

💰 **ROI (Retour sur Investissement)** :
- **Temps gagné** : Plus besoin de traiter manuellement
- **Fiabilité** : Moins d'erreurs humaines
- **Rapidité** : 240 lignes/seconde vs traitement manuel
- **Visibilité** : On sait toujours où on en est

### Évolutivité

🚀 **Prêt pour la mise à l'échelle** :
- ✅ Fonctionne sur 60 lignes
- ✅ Peut traiter 60 000 lignes
- ✅ Peut être déployé sur Azure Cloud
- ✅ Peut tourner 24/7 automatiquement

---

## 🔄 Migration vers Azure Cloud

### La Prochaine Étape

Ce projet **local** (sur votre ordinateur) est la **maquette** d'un système **production** (dans le cloud).

**Analogie** : C'est comme construire une **maquette de pont** avant de construire le vrai pont !

### Correspondance Local → Cloud

| 🏠 Version Locale | ☁️ Version Cloud Azure |
|-------------------|----------------------|
| Script Python sur PC | Azure Data Factory |
| Fichier CSV local | Azure Blob Storage |
| Docker local | Azure Container Instances |
| Datadog Dashboard | Azure Monitor |

**Le code reste le même**, seul l'environnement change !

---

## 👥 À Qui Ça Sert ?

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

## 📦 Livrables du Projet

### Ce Qui Est Fourni

- ✅ **Code source complet** : Prêt à être exécuté
- ✅ **Configuration Docker** : Déploiement en 1 commande
- ✅ **Documentation détaillée** : Comment l'utiliser
- ✅ **Exemples de données** : Pour tester immédiatement
- ✅ **Logs et métriques** : Visibles dans Datadog

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

## 🎯 Points Clés à Retenir

### En 3 Phrases

1. 🤖 **Un robot lit un fichier, ajoute des infos utiles, et crée un nouveau fichier**
2. 📊 **Un système de surveillance (Datadog) vérifie que tout fonctionne bien**
3. 📦 **Tout est empaqueté dans Docker pour fonctionner partout de la même façon**

### Pourquoi C'est Important

- 💼 **Pour l'entreprise** : Gain de temps et fiabilité
- 🎓 **Pour l'apprentissage** : Comprendre les pipelines de données modernes
- 🚀 **Pour la carrière** : Compétences demandées en DevOps/Data Engineering

---

## 👤 Auteur

**Juvet**  
DevOps Engineer – Mercedes-Benz Trucks Molsheim

*Projet réalisé dans le cadre du Bootcamp Observabilité & Data*  
*Période : 27 décembre 2025 → 4 janvier 2026*
