# Dictionnaire des Données - smartEngine

Ce document détaille la structure des données brutes de RavenStack utilisées pour la prédiction du churn.

## 1. Comptes (`ravenstack_accounts.csv`)
Données signalétiques sur les entreprises clientes.
- `account_id` (object) : Identifiant unique du compte.
- `account_name` (object) : Nom de l'entreprise.
- `industry` (object) : Secteur d'activité (EdTech, FinTech, etc.).
- `country` (object) : Pays d'origine.
- `signup_date` (object/date) : Date d'inscription.
- `referral_source` (object) : Origine de l'acquisition (organic, partner, etc.).
- `plan_tier` (object) : Niveau de service (Basic, Pro, Enterprise).
- `seats` (int64) : Nombre de licences (sièges) utilisateur.
- `is_trial` (bool) : Compte en période d'essai ou non.
- `churn_flag` (bool) : Indicateur de résiliation historique.

## 2. Abonnements (`ravenstack_subscriptions.csv`)
Historique contractuel et financier.
- `subscription_id` (object) : Identifiant de l'abonnement.
- `account_id` (object) : Lien vers le compte.
- `start_date` / `end_date` (date) : Période de validité.
- `mrr_amount` (int64) : Revenu Mensuel Récurrent (MRR) en USD.
- `billing_frequency` (object) : Fréquence de facturation (monthly, annual).
- `auto_renew_flag` (bool) : Renouvellement automatique activé.
- `churn_flag` (bool) : Indique si cet abonnement spécifique a fini par un churn.

## 3. Utilisation des fonctionnalités (`ravenstack_feature_usage.csv`)
Données comportementales quotidiennes.
- `usage_id` (object) : Identifiant de l'événement.
- `subscription_id` (object) : Lien vers l'abonnement.
- `feature_name` (object) : Nom de la fonctionnalité utilisée.
- `usage_count` (int64) : Nombre d'utilisations.
- `usage_duration_secs` (int64) : Temps passé sur la fonctionnalité (secondes).
- `error_count` (int64) : Nombre d'erreurs rencontrées.

## 4. Tickets de Support (`ravenstack_support_tickets.csv`)
Interactions avec le service client.
- `ticket_id` (object) : Identifiant du ticket.
- `account_id` (object) : Lien vers le compte.
- `resolution_time_hours` (float64) : Délai de résolution.
- `satisfaction_score` (float64) : Note de satisfaction (1-5).
- `escalation_flag` (bool) : Indique si le ticket a été escaladé.

## 5. Événements de Churn (`ravenstack_churn_events.csv`)
Détails sur les résiliations.
- `churn_event_id` (object) : Identifiant de l'événement de churn.
- `reason_code` (object) : Raison invoquée (pricing, support, budget, etc.).
- `feedback_text` (object) : Commentaire libre laissé par le client.
