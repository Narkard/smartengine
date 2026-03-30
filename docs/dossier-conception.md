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

### 2.1 Nettoyage et Agrégation
Les données brutes ont été nettoyées (imputation par la médiane pour le support, winsorisation du MRR) et agrégées par compte.

### 2.2 Feature Engineering (Variables clés)
Nous avons créé des variables comportementales pour capturer les signaux de churn :
- **Usage Trend (30j)** : Variation de l'usage entre le dernier mois et la moyenne historique. Un score négatif indique une baisse d'activité, signal fort de désengagement.
- **Engagement (Recency)** : Nombre de jours depuis la dernière action. Plus ce chiffre est élevé, plus le risque de churn augmente.
- **Ratio Critique (Support)** : Part des tickets "Urgent/High" dans le total des tickets. Un client qui n'a que des problèmes graves est plus susceptible de partir.
- **Diversité d'usage** : Nombre de fonctionnalités différentes utilisées. Un client qui n'utilise qu'une seule feature tire moins de valeur du produit.

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

