# Rapport de Nettoyage des Données - Sprint 2

Ce rapport documente la qualité des données brutes et les décisions de nettoyage prises pour la construction de la table analytique.

## Bilan par Fichier CSV

| Fichier | Problème identifié | Stratégie de traitement | Justification |
| :--- | :--- | :--- | :--- |
| `accounts.csv` | Données propres | Aucune action | Qualité initiale élevée. |
| `churn_events.csv` | Valeurs manquantes (feedback) | Suppression des orphelins | Données non critiques pour le modèle. |
| `feature_usage.csv` | Clé account_id absente | Jointure via subscription_id | Seul moyen de lier l'usage aux comptes. |
| `support_tickets.csv` | 825 satisfaction_score nuls | Imputation par la moyenne | Évite de perdre 40% des tickets de support. |
| `subscriptions.csv` | end_date nul pour abos actifs | Remplissage par "Active" | Normalité métier. |

## Bilan Global
- **Données conservées** : 100% des comptes (500/500).
- **Taux de perte** : 0% après imputation.
- **Table analytique finale** : `data/processed/analytics.csv`

*Dernière mise à jour : 30 mars 2026*
