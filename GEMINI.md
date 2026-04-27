# Projet smartEngine - Groupe 1

## Contexte
Nous construisons **smartEngine**, un système de prédiction de churn pour RavenStack, un SaaS B2B.

## Historique des Sprints
### Sprint 1 : Infrastructure & Cadrage
- **Action** : Configuration du dépôt, analyse du brief client, veille technologique.
- **Livrables** : Dossier de conception (Section 1), Rapport de veille, Backlog initial.

### Sprint 2 : Traitement des données (Terminé)
- **Action** : Nettoyage complet, Feature Engineering et génération de la table analytique.
- **Innovation** : Recalcul de la cible via `churn_events` pour pallier le manque de fiabilité du flag d'origine.
- **Livrables** :
    - `data/processed/analytics.csv` (Table finale)
    - `outputs/rapport-nettoyage.md` (Traçabilité)
    - `.gemini/agents/data-engineer.md` (Agent spécialisé)

### Sprint 3 : Modélisation & Évaluation (Terminé)
- **Action** : Entraînement de LogisticRegression, RandomForest et XGBoost avec gestion du déséquilibre des classes.
- **Résultat** : Meilleur modèle identifié : **RandomForest** (F1-score : **0.81**).
- **Livrables** :
    - `src/train_model.py` (Script d'entraînement)
    - `outputs/models/churn_model.joblib` (Modèle sauvegardé)
    - `.gemini/agents/model-trainer.md` (Agent spécialisé)

## Sprint en cours
**Sprint 4 - Déploiement & Dashboarding** (À venir)
- Objectif : Créer une interface de visualisation et une API de prédiction.

## Rôles du Sprint 2
- **Scrum Master** : Maé
- **Product Owner** : Joanne
- **Développeurs IA** : Léo, Quentin, Sophie

## Conventions et Accès
- **Données** : Les fichiers bruts sont dans `/data/raw/` (lecture seule).
- **Pipeline** : L'exécution se fait via `src/clean_data.py` -> `src/build_features.py` -> `src/build_analytics.py`.
- **Rapports** : `/outputs/` pour les résultats opérationnels, `/docs/` pour la documentation stratégique.
- **Table analytique** : `data/processed/analytics.csv` (28 variables, 500 comptes).
