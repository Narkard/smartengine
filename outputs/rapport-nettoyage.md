# Rapport de Nettoyage des Données - Sprint 2 (Groupe 1)

Ce document détaille l'audit de qualité et les traitements appliqués aux données brutes de RavenStack pour garantir la fiabilité du modèle de prédiction du churn.

## 1. Analyse par Fichier CSV

### 1.1 ravenstack_accounts.csv
- **Problèmes identifiés** : Aucun. Les données sont structurellement saines.
- **Stratégie** : Conservation intégrale.
- **Résultat** : 500 lignes avant / 500 lignes après (100% conservé).

### 1.2 ravenstack_subscriptions.csv
- **Problèmes identifiés** : 
    - Valeurs manquantes : `end_date` (90.28%).
    - Outliers : Présence de valeurs MRR extrêmes (> percentile 99).
- **Stratégies choisies** : 
    - `end_date` : Conservation des valeurs nulles (signifiant un abonnement actif).
    - `mrr_amount` : **Winsorisation** au 99ème percentile.
- **Justification** : Le MRR extrême peut biaiser les moyennes de revenus. Le plafonnement permet de garder ces clients dans l'analyse sans fausser le modèle.
- **Résultat** : 5000 lignes avant / 5000 lignes après (100% conservé).

### 1.3 ravenstack_feature_usage.csv
- **Problèmes identifiés** : Absence de la colonne `account_id` (clé primaire du projet).
- **Stratégie** : Jointure via `subscription_id` puis agrégation par compte.
- **Justification** : Nécessaire pour ramener l'usage au niveau du client unique.
- **Résultat** : 25000 lignes avant / 25000 lignes après (100% conservé).

### 1.4 ravenstack_support_tickets.csv
- **Problèmes identifiés** : 
    - Valeurs manquantes : `satisfaction_score` (**41.25%**, soit 825 lignes).
- **Stratégie** : **Imputation par la médiane**.
- **Justification** : Supprimer 41% des tickets réduirait drastiquement la représentativité du support. La médiane est préférée à la moyenne car elle est moins sensible aux notes extrêmes.
- **Résultat** : 2000 lignes avant / 2000 lignes après (100% conservé).

### 1.5 ravenstack_churn_events.csv
- **Problèmes identifiés** : 
    - Valeurs manquantes : `feedback_text` (24.67%).
- **Stratégie** : Remplacement par une valeur par défaut ("No feedback provided").
- **Justification** : Préserve l'événement de churn tout en nettoyant les données pour les analyses textuelles futures.
- **Résultat** : 600 lignes avant / 600 lignes après (100% conservé).

## 2. Bilan Global de la Qualité

| Indicateur | Valeur |
| :--- | :--- |
| **Nombre de comptes initiaux** | 500 |
| **Nombre de comptes finaux** | 500 |
| **Taux de conservation des données** | **100%** |
| **Principale transformation** | Imputation massive du Support et Winsorisation MRR |

## 3. Conclusion
Les données sont désormais typées, complétées et prêtes pour la modélisation. La table analytique `data/processed/analytics.csv` contient 29 variables exploitables sans risque de biais majeur lié aux valeurs manquantes.

*Fait le 30 mars 2026 par l'équipe du Groupe 1.*
