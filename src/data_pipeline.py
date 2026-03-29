import pandas as pd
import numpy as np
import os

# Configuration des chemins
DATA_RAW = r"data/raw"
OUTPUT_DIR = r"outputs"

# Fichiers sources
ACCOUNTS_FILE = os.path.join(DATA_RAW, "ravenstack_accounts.csv")
SUBS_FILE = os.path.join(DATA_RAW, "ravenstack_subscriptions.csv")
USAGE_FILE = os.path.join(DATA_RAW, "ravenstack_feature_usage.csv")
TICKETS_FILE = os.path.join(DATA_RAW, "ravenstack_support_tickets.csv")

def build_master_dataset():
    print("--- Début du Traitement des Données (Sprint 2 - Avancé) ---")
    
    # 1. Chargement
    df_accounts = pd.read_csv(ACCOUNTS_FILE)
    df_subs = pd.read_csv(SUBS_FILE)
    df_usage = pd.read_csv(USAGE_FILE)
    df_tickets = pd.read_csv(TICKETS_FILE)
    
    # Prétraitement des dates
    df_usage['usage_date'] = pd.to_datetime(df_usage['usage_date'])
    MAX_DATE = df_usage['usage_date'].max()

    # 2. Feature Engineering : Tendance d'Usage (Usage Trend)
    print("Calcul des tendances d'usage...")
    # Usage des 3 derniers mois (90 jours)
    cutoff_date = MAX_DATE - pd.Timedelta(days=90)
    recent_usage = df_usage[df_usage['usage_date'] >= cutoff_date]
    
    recent_agg = recent_usage.groupby('subscription_id')['usage_count'].sum().reset_index().rename(columns={'usage_count': 'recent_usage_3m'})
    
    # Usage historique (global)
    historical_agg = df_usage.groupby('subscription_id')['usage_count'].sum().reset_index().rename(columns={'usage_count': 'total_usage'})
    
    # Fusion et calcul du trend (ratio usage récent / total)
    # On pondère le total pour comparer 3 mois vs le reste (en mois)
    # On va faire simple : trend = (recent_3m / 3) / (total / total_months)
    usage_trends = historical_agg.merge(recent_agg, on='subscription_id', how='left').fillna(0)
    usage_trends['usage_trend'] = (usage_trends['recent_usage_3m'] / 3) / (usage_trends['total_usage'] / 24) # 24 mois de data
    
    # Agrégation finale de l'usage
    usage_agg = df_usage.groupby('subscription_id').agg({
        'usage_count': ['sum', 'mean'],
        'error_count': 'sum'
    })
    usage_agg.columns = ['_'.join(col).strip() for col in usage_agg.columns.values]
    usage_agg = usage_agg.merge(usage_trends[['subscription_id', 'usage_trend']], on='subscription_id', how='left')

    # 3. Agrégation des Tickets de Support
    print("Traitement des tickets de support...")
    tickets_agg = df_tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean',
        'escalation_flag': 'sum'
    }).rename(columns={'ticket_id': 'ticket_count'}).reset_index()
    
    # Imputation simple de la satisfaction moyenne (parmi les tickets avec score)
    mean_sat = df_tickets['satisfaction_score'].mean()
    tickets_agg['satisfaction_score'] = tickets_agg['satisfaction_score'].fillna(mean_sat)

    # 4. Consolidation finale
    print("Consolidation au niveau Account...")
    subs_enriched = df_subs.merge(usage_agg, on='subscription_id', how='left')
    
    account_usage = subs_enriched.groupby('account_id').agg({
        'usage_count_sum': 'sum',
        'error_count_sum': 'sum',
        'usage_trend': 'mean',
        'mrr_amount': 'sum',
        'churn_flag': 'max'
    }).reset_index()

    master_df = df_accounts.merge(account_usage, on='account_id', how='left')
    master_df = master_df.merge(tickets_agg, on='account_id', how='left')
    
    # Nettoyage
    numeric_master = master_df.select_dtypes(include=[np.number]).columns
    master_df[numeric_master] = master_df[numeric_master].fillna(0)
    
    # Résolution churn_flag
    if 'churn_flag_x' in master_df.columns:
        master_df['churn_flag'] = master_df['churn_flag_x']
        master_df.drop(columns=['churn_flag_x', 'churn_flag_y'], inplace=True, errors='ignore')

    # 5. Sauvegarde
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    master_df.to_csv(os.path.join(OUTPUT_DIR, "master_dataset.csv"), index=False)
    print(f"Dataset masterisé généré : {master_df.shape[0]} lignes.")

if __name__ == "__main__":
    build_master_dataset()
