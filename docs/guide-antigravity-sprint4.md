# Guide d'utilisation - smartEngine Sprint 4 (Déploiement)

Ce guide détaille l'utilisation des livrables produits lors du Sprint 4 du projet smartEngine : le dashboard interactif et le générateur d'alertes de risque de churn.

## 1. Dashboard Interactif (Streamlit)

Le dashboard permet aux équipes Customer Success (CS) de visualiser l'état de santé du portefeuille client et d'identifier rapidement les comptes à risque.

### Prérequis
Assurez-vous que le dataset consolidé a bien été généré lors du Sprint 2 et se trouve à l'emplacement suivant :
`outputs/master_dataset.csv`

### Lancement
Pour démarrer l'application Streamlit, exécutez la commande suivante depuis la racine du projet :

```bash
streamlit run src/dashboard.py
```

### Fonctionnalités
- **Vue d'ensemble (KPIs)** : Nombre total de clients, MRR (Revenu Récurrent Mensuel) total, nombre de comptes à risque (tendance d'usage < 0.8), et taux de churn actuel.
- **Filtres interactifs** : Filtrage par industrie et par niveau de plan (Tier) via la barre latérale.
- **Graphiques d'analyse** :
  - *Distribution de la Tendance d'Usage* : Permet de comparer visuellement les tendances d'usage entre les clients actifs et ceux ayant churné.
  - *MRR par Industrie* : Répartition du revenu.
- **Tableau d'Alertes** : Liste dynamique des comptes actifs (non churnés) présentant un risque immédiat (tendance d'usage inférieure à 0.8).

## 2. Générateur d'Alertes de Risque

Ce script utilise le modèle de Machine Learning entraîné lors du Sprint 3 pour prédire la probabilité de churn des clients actuellement actifs et générer un rapport d'alerte.

### Prérequis
- Dataset consolidé : `outputs/master_dataset.csv`
- Modèle entraîné : `src/churn_model.pkl`

### Exécution
Pour générer le rapport d'alertes, exécutez le script suivant :

```bash
python src/generate_alerts.py
```

### Résultat
Le script analyse les clients actifs, calcule leur probabilité de churn à l'aide de `predict_proba`, et filtre ceux dont la probabilité dépasse le seuil de **0.6 (60%)**.

Un rapport est généré dans le dossier `outputs/` sous le format `alerts_YYYYMMDD.txt` (ex: `alerts_20260526.txt`). Ce rapport textuel contient pour chaque compte à risque :
- L'ID du compte et son industrie.
- La probabilité de churn estimée par le modèle.
- Le MRR exposé (revenu en danger).
- La tendance d'usage actuelle.
