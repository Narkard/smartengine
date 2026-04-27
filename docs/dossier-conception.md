# Dossier de Conception - smartEngine

## 1. Cadrage du Projet

### 1.1 Contexte Métier
RavenStack est un SaaS B2B confronté à un enjeu de rétention client. Chaque départ (churn) entraîne une perte de revenu récurrent mensuel (MRR). Le projet smartEngine doit permettre d'anticiper ces départs.

### 1.2 Objectifs
- Prédire la probabilité de churn pour chaque compte.
- Prioriser les actions des équipes Customer Success (CS).
- Automatiser les notifications pour les comptes à haut risque.

### 1.3 Contraintes RGPD et Éthique
En conformité avec le RGPD et la loi Informatique et Libertés :
- **Minimisation des données** : Seules les données nécessaires à la prédiction du churn sont collectées et traitées.
- **Article 22** : L'utilisation d'un score automatisé doit rester une aide à la décision pour les équipes CS et non une décision entièrement automatisée ayant des impacts juridiques majeurs.
- **Transparence** : Les critères influençant le score doivent être explicables pour éviter les "boîtes noires" et les biais algorithmiques.

### 1.4 Choix des Outils
- **Gestionnaire de version** : GitHub pour la collaboration distribuée.
- **Orchestration IA** : Gemini CLI pour la génération de code et l'analyse automatisée.
- **Data Science** : Python, pandas et scikit-learn pour le pipeline de données et la modélisation.
- **Dashboarding** : Streamlit pour une interface légère et rapide à déployer.
- **Automatisation** : n8n pour les alertes de risque.

---
## 2. Traitement des données (Sprint 2)

### 2.1 État des données brutes et nettoyage
Avant traitement, les données présentaient plusieurs anomalies :
- **churn_flag** : Incohérent entre les sources (110 vs 352 événements réels).
- **support_tickets** : 41% de valeurs manquantes pour le `satisfaction_score`.
- **subscriptions** : Présence d'outliers extrêmes sur le MRR (comptes tests ou erreurs de saisie).

**Stratégies choisies :**
- **Imputation** : Médiane pour les scores de satisfaction (robuste aux extrêmes).
- **Winsorisation** : Clipping du MRR au 99ème percentile.
- **Exclusion** : Suppression radicale de la colonne `churn_flag` d'origine pour éviter toute pollution du modèle.

### 2.2 Construction de la table analytique
La table `analytics.csv` est construite par jointures successives à partir du référentiel `accounts_cleaned.csv` :
- **Granularité** : Une ligne par `account_id`.
- **Méthode de jointure** : `left join` systématique pour conserver tous les comptes, même ceux n'ayant pas encore utilisé le produit ou ouvert de tickets.
- **Cible (Target)** : Recalculée via la présence ou non dans `churn_cleaned.csv`.

### 2.3 Feature Engineering (Détails et Justification)
| Feature | Source | Justification Métier |
| :--- | :--- | :--- |
| `usage_trend_30d` | Usage | Capture le désengagement progressif avant le churn effectif. |
| `days_since_last_usage` | Usage | Mesure l'inactivité immédiate (signal d'alerte critique). |
| `critical_ratio` | Support | Identifie les comptes en situation de tension technique majeure. |
| `nb_unique_features` | Usage | Mesure l'adoption du produit (stickiness). |
| `seniority_months` | Sub | Distingue le churn précoce (onboarding raté) du churn mature. |
| `nb_upgrades` | Sub | Indique la satisfaction et la croissance du compte (anti-churn). |

### 2.4 Retour d'expérience sur l'Agent de Traitement
L'agent `data-engineer` a été configuré pour automatiser ces tâches. 
- **Points forts** : Excellente gestion des types temporels et des chemins relatifs. 
- **Ajustements nécessaires** : L'agent a dû être explicitement instruit d'ignorer le `churn_flag` d'origine, qu'il avait tendance à conserver par défaut. La séparation en trois scripts (`clean`, `build`, `analytics`) a permis une meilleure traçabilité.

---
### 2.3 Tâche de recherche : Théorie du Feature Engineering

**Importance vs Algorithme** : Le feature engineering est souvent plus crucial que le choix du modèle car il fournit la "matière première". Un algorithme sophistiqué sur des données pauvres (brutes) performera moins bien qu'un modèle simple sur des features riches et intelligentes qui isolent les signaux métiers.

**Variables de Tendance** : Elles se calculent en comparant une fenêtre temporelle récente à une fenêtre de référence passée. Exemple : `(Moyenne_Mois_N / Moyenne_Mois_N-1) - 1`.

**Encodage des variables** :
- **One-Hot Encoding** : Création d'une colonne binaire par catégorie. À utiliser pour les variables nominales sans ordre (ex: Secteur d'activité).
- **Label Encoding** : Conversion en entiers (1, 2, 3). À utiliser pour les variables ordinales (ex: Plan Starter < Pro < Enterprise).

**Normalisation vs Standardisation** :
- **Normalisation** : Ramène les valeurs entre [0, 1]. Utile pour les algorithmes basés sur la distance (K-Means, KNN).
- **Standardisation** : Centre les données (moyenne 0, écart-type 1). Préférable pour les modèles linéaires et les réseaux de neurones.
- *Note : Les arbres de décision (Random Forest) n'en ont généralement pas besoin.*

## 3. Modélisation (Sprint 3)
### 3.1 Algorithme
Utilisation d'un **RandomForestClassifier** pour sa robustesse et sa capacité à gérer les variables non-linéaires.
### 3.2 Performance
Le modèle atteint une précision de **76%**. On note une importance forte des variables d'usage (`usage_count_mean`) et de support (`resolution_time_hours`).

## 4. Déploiement (Sprint 4)
### 4.1 Dashboard
Développement d'une interface **Streamlit** permettant :
- Visualisation des KPIs (MRR, Taux de Churn).
- Analyse de la corrélation Usage/Revenu.
- Tableau d'alertes dynamique pour les équipes Customer Success.

*Dernière mise à jour : 29 mars 2026*

