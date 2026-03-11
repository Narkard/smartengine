import pandas as pd
import numpy as np
import os
from datetime import timedelta

# Chemins des fichiers bruts
DATA_DIR = "../data/raw"
ACCOUNTS_PATH = os.path.join(DATA_DIR, "ravenstack_accounts.csv")
SUBS_PATH = os.path.join(DATA_DIR, "ravenstack_subscriptions.csv")
USAGE_PATH = os.path.join(DATA_DIR, "ravenstack_feature_usage.csv")
TICKETS_PATH = os.path.join(DATA_DIR, "ravenstack_support_tickets.csv")
CHURN_PATH = os.path.join(DATA_DIR, "ravenstack_churn_events.csv")

def explore_and_clean_data():
    print("--- SPRINT 2 : PIPELINE DE TRAITEMENT AVANCE ---")
    
    # 1. Chargement des données
    accounts = pd.read_csv(ACCOUNTS_PATH)
    subs = pd.read_csv(SUBS_PATH)
    usage = pd.read_csv(USAGE_PATH)
    tickets = pd.read_csv(TICKETS_PATH)
    
    # Conversion des dates
    usage['usage_date'] = pd.to_datetime(usage['usage_date'])
    tickets['submitted_at'] = pd.to_datetime(tickets['submitted_at'])
    
    # 2. Feature Engineering : Usage & Tendances
    print("Calcul des tendances d'usage...")
    max_date = usage['usage_date'].max()
    recent_limit = max_date - timedelta(days=60)
    
    # Usage total par abonnement
    usage_total = usage.groupby('subscription_id').agg({
        'usage_count': 'sum',
        'usage_duration_secs': 'sum',
        'error_count': 'sum'
    }).rename(columns={'usage_count': 'total_usage', 'error_count': 'total_errors', 'usage_duration_secs': 'total_duration'})
    
    # Usage récent (60 derniers jours)
    usage_recent = usage[usage['usage_date'] >= recent_limit].groupby('subscription_id').agg({
        'usage_count': 'sum'
    }).rename(columns={'usage_count': 'recent_usage'})
    
    usage_features = usage_total.join(usage_recent, how='left').fillna(0)
    # Variable de tendance : ratio usage récent / usage total
    usage_features['usage_trend'] = usage_features['recent_usage'] / (usage_features['total_usage'] + 1)
    
    # 3. Feature Engineering : Support & Satisfaction
    print("Traitement des tickets et scores de satisfaction...")
    # Imputation simple pour la satisfaction (moyenne)
    tickets['satisfaction_score'] = tickets['satisfaction_score'].fillna(tickets['satisfaction_score'].mean())
    
    tickets_features = tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'satisfaction_score': 'mean',
        'resolution_time_hours': 'mean',
        'escalation_flag': 'sum'
    }).rename(columns={'ticket_id': 'ticket_count'}).reset_index()
    
    # 4. Jointures et Finalisation
    print("Construction du dataset master enrichi...")
    
    # On garde le dernier abonnement par compte
    last_subs = subs.sort_values(by=['account_id', 'start_date']).drop_duplicates(subset=['account_id'], keep='last')
    
    # Fusion accounts + tickets
    dataset = accounts.merge(tickets_features, on='account_id', how='left')
    dataset.fillna({'ticket_count': 0, 'satisfaction_score': 3.0, 'resolution_time_hours': 0, 'escalation_flag': 0}, inplace=True)
    
    # Fusion avec abonnements et usage
    dataset = dataset.merge(last_subs[['account_id', 'subscription_id', 'plan_tier', 'mrr_amount', 'churn_flag']], on='account_id', how='left')
    dataset = dataset.merge(usage_features, on='subscription_id', how='left')
    
    # Nettoyage final des valeurs manquantes dues aux jointures
    dataset.fillna({
        'total_usage': 0, 'total_errors': 0, 'total_duration': 0,
        'recent_usage': 0, 'usage_trend': 0, 'mrr_amount': 0
    }, inplace=True)
    
    # Renommage target
    dataset.rename(columns={'churn_flag_y': 'target_churn'}, inplace=True)
    
    # 5. Sauvegarde
    os.makedirs("../outputs", exist_ok=True)
    dataset.to_csv("../outputs/master_dataset.csv", index=False)
    
    print(f"Dataset master généré : {dataset.shape[0]} lignes, {dataset.shape[1]} colonnes.")
    print("Nouvelles variables créées : [total_usage, total_errors, usage_trend, satisfaction_score, ticket_count]")

if __name__ == "__main__":
    explore_and_clean_data()
