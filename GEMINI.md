# Projet smartEngine - Groupe 1

## Contexte
Nous construisons **smartEngine**, un système de prédiction de churn pour RavenStack, un SaaS B2B.

## Historique des Sprints
### Sprint 1 : Infrastructure & Cadrage (Terminé)
- **Action** : Configuration du dépôt, analyse du brief client, veille technologique.
- **Livrables** : Dossier de conception (Section 1), Rapport de veille, Backlog initial.

### Sprint 2 : Traitement des données (Terminé)
- **Action** : Nettoyage complet, Feature Engineering et génération de la table analytique.
- **Innovation** : Recalcul de la cible via `churn_events` pour pallier le manque de fiabilité du flag d'origine.
- **Livrables** :
    - `data/processed/analytics.csv` (Table finale)
    - `outputs/rapport-nettoyage.md` (Traçabilité)

### Sprint 3 : Modélisation & Évaluation (Terminé)
- **Action** : Entraînement de LogisticRegression, RandomForest et XGBoost.
- **Résultat** : Meilleur modèle identifié : **RandomForest** (F1-score : **0.81**).
- **Livrables** :
    - `src/train_model.py` (Entraînement)
    - `src/evaluate_model.py` (Évaluation)
    - `src/generate_scores.py` (Scoring)
    - `outputs/models/churn_model.joblib` (Modèle)
    - `outputs/scores.csv` (Scores et risques)
    - `outputs/evaluation_metrics.json` (Métriques)
    - `outputs/rapport-modele.md` (Rapport)

## Rôles Sprint 3
- **Scrum Master** : Quentin
- **Product Owner** : Maé
- **Développeurs IA** : Léo, Joanne, Sophie

## Conventions
- Scripts Python -> `/src/`
- Rapports -> `/outputs/`
- Données transformées -> `/data/processed/analytics.csv`
- Modèles -> `outputs/models/churn_model.joblib`
- Scores -> `outputs/scores.csv`
- Ne jamais modifier `/data/raw/`
- Tous les rapports sont en français

## Sprint en cours
Sprint 3 - Modélisation (Finalisation)
