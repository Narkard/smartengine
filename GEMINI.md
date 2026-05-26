# Projet smartEngine - Groupe 1

## Contexte
Nous construisons **smartEngine**, un système de prédiction de churn pour RavenStack, un SaaS B2B. Les données brutes sont dans `/data/raw/`.

## Résumé des Sprints précédents
- **Sprint 1 (Découverte)** : Dépôt GitHub configuré, arborescence complète, GEMINI.md initialisé. Exploration des 5 CSV bruts, veille technique et cadrage (Dossier de conception).
- **Sprint 2 (Traitement)** : Nettoyage des données, gestion des valeurs manquantes, feature engineering, et production de la table analytique `data/processed/analytics.csv`.
- **Sprint 3 (Modélisation)** : Entraînement du modèle de scoring prédictif (RandomForest) avec une précision de 76% et validation des métriques.

## Sprint en cours
**Sprint 4 - Déploiement et soutenance**
- Objectifs : Déployer le dashboard interactif, automatiser les alertes, générer le fichier de priorisation des clients à risque et finaliser le dossier de conception.
- Tâches actuelles : Mise à jour de l'infrastructure, création de l'agent de déploiement, script `generate_priorisation.py`.

## Rôles du Sprint 4
- **Scrum Master** : Joanne
- **Développeurs IA** : Maé, Quentin, Léo, Sophie
- *(Product Owner en rotation selon l'équipe)*

## Conventions
- Scripts Python -> `/src/`
- Rapports et datasets générés -> `/outputs/`
- Table analytique consolidée -> `data/processed/analytics.csv`
- Agents IA -> `.gemini/agents/`
- Ne jamais modifier `/data/raw/`
- Tous les rapports sont rédigés en français.
