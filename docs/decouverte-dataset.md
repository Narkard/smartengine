# Fiche Collective d'Exploration du Dataset - RavenStack

Ce document synthétise les résultats de l'exploration des données réalisée par l'équipe pour le projet **smartEngine**.

## 1. Récapitulatif des fichiers CSV

| Nom du Fichier | Nombre de Lignes | Colonnes Clés | Observations Qualité |
| :--- | :--- | :--- | :--- |
| `ravenstack_accounts.csv` | 500 | `account_id`, `industry`, `plan_tier`, `churn_flag` | Données propres, aucune valeur manquante. |
| `ravenstack_churn_events.csv` | 600 | `reason_code`, `refund_amount_usd`, `feedback_text` | 148 valeurs manquantes dans `feedback_text`. |
| `ravenstack_feature_usage.csv` | 25 000 | `usage_count`, `usage_duration_secs`, `error_count` | Dataset volumineux, pas de valeurs manquantes. |
| `ravenstack_subscriptions.csv` | 5 000 | `mrr_amount`, `billing_frequency`, `auto_renew_flag` | 4 514 valeurs manquantes pour `end_date` (normal pour abos actifs). |
| `ravenstack_support_tickets.csv` | 2 000 | `priority`, `resolution_time_hours`, `satisfaction_score` | **825 valeurs manquantes** pour `satisfaction_score`. |

## 2. Variables Clés pour la Prédiction du Churn

L'équipe a identifié les variables suivantes comme étant les plus prometteuses pour le modèle de scoring :

1.  **Indicateurs d'Usage** : `usage_count` et `usage_duration_secs` (une baisse soudaine d'activité est un signal fort).
2.  **Satisfaction Client** : `satisfaction_score` et `ticket_count` (les clients mécontents ou sollicitant trop le support sont à risque). 
3.  **Santé Financière** : `mrr_amount` et `auto_renew_flag` (l'impact financier et le mode de renouvellement).
4.  **Expérience Utilisateur** : `error_count` (les frictions techniques peuvent mener au départ).

## 3. Questions Métier à Explorer

1.  Existe-t-il une corrélation entre le secteur d'activité (`industry`) et le taux de churn ?
2.  Le type de plan (`plan_tier`) influence-t-il la fidélité des clients ?
3.  Quel est le délai moyen de résolution des tickets pour les clients qui finissent par churner ?
4.  Une désactivation de l'auto-renouvellement précède-t-elle systématiquement le churn ?
5.  Les erreurs techniques (`error_count`) sont-elles concentrées sur certaines fonctionnalités spécifiques ?

---
*Dernière mise à jour : 29 mars 2026*
