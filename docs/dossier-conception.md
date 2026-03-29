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
Les données brutes ont été agrégées au niveau du compte (`account_id`). 
- **Usage** : Somme et moyenne des `usage_count`, `usage_duration_secs` et `error_count`.
- **Support** : Nombre de tickets par compte, temps moyen de résolution et score de satisfaction moyen.
- **Master Dataset** : Fusion de toutes les sources pour créer un dataset unique de 500 lignes (un par client).

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

