# Projet smartEngine - Groupe [X] (Sprint 2)

## Rôles du Sprint 2
- **Product Owner** : [Nouveau Nom] (précédemment : [Ancien Nom])
- **Scrum Master** : [Nouveau Nom] (précédemment : [Ancien Nom])
- **Développeur IA** : Sophie

## Résumé du Sprint 1 (Bilan)
- Infrastructure Git initialisée sur la branche Sophie.
- Exploration initiale du dataset RavenStack effectuée.
- Brief client et veille outils documentés.
- Dossier de conception Section 1 (Cadrage) finalisée.

## Objectifs du Sprint 2
- Nettoyage rigoureux des données brutes.
- Feature engineering pour capturer les signaux de churn.
- Production de la table analytique finale : `data/processed/analytics.csv`.

## Conventions
- Granularité de la table analytique : une ligne par `account_id`.
- Scripting modulaire : `clean_data.py`, `build_features.py`, `build_analytics.py`.
- Rapports de nettoyage dans `/outputs/`.
