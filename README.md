# smartEngine - RavenStack Churn Prediction

Système intelligent de prédiction de churn pour RavenStack (SaaS B2B).

## Description du Projet
smartEngine aide les équipes Customer Success de RavenStack à identifier les comptes à risque de résiliation en utilisant des techniques de machine learning sur les données d'usage, de support et d'abonnement.

## Structure du Dépôt
- `.gemini/agents/` : Définitions des agents IA spécialisés.
- `data/raw/` : Données brutes de RavenStack (CSV).
- `docs/` : Documentation du projet (Brief client, Dossier de conception, Veille).
- `outputs/` : Rapports générés et datasets masterisés.
- `src/` : Scripts Python (Pipeline, Entraînement, Alertes).

## Installation
1. Installer les dépendances : `pip install -r src/requirements.txt`
2. Installer Gemini CLI : `npm install -g @google/gemini-cli`

## Utilisation
1. **Pipeline de données** : `python3 src/data_pipeline.py`
2. **Entraînement du modèle** : `python3 src/train_model.py`
3. **Génération d'alertes** : `python3 src/generate_alerts.py`

## Équipe (Groupe X)
- **Product Owner** : [Nom]
- **Scrum Master** : [Nom]
- **Développeurs IA** : Sophie, [Nom]
