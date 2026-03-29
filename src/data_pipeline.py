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
CHURN_FILE = os.path.join(DATA_RAW, "ravenstack_churn_events.csv")

def build_master_dataset():
    print("--- Début du Traitement des Données (Sprint 2) ---")
    
    # 1. Chargement
    print("Chargement des fichiers CSV...")
    df_accounts = pd.read_csv(ACCOUNTS_FILE)
    df_subs = pd.read_csv(SUBS_FILE)
    df_usage = pd.read_csv(USAGE_FILE)
    df_tickets = pd.read_csv(TICKETS_FILE)
    
    # 2. Agrégation de l'Usage (Feature Engineering)
    print("Agrégation des données d'utilisation...")
    usage_agg = df_usage.groupby('subscription_id').agg({
        'usage_count': ['sum', 'mean', 'max'],
        'usage_duration_secs': 'sum',
        'error_count': 'sum'
    })
    usage_agg.columns = ['_'.join(col).strip() for col in usage_agg.columns.values]
    usage_agg = usage_agg.reset_index()

    # 3. Agrégation des Tickets de Support
    print("Agrégation des tickets de support...")
    tickets_agg = df_tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean',
        'escalation_flag': 'sum'
    }).rename(columns={'ticket_id': 'ticket_count'}).reset_index()

    # 4. Enrichissement des Abonnements
    print("Enrichissement des abonnements avec l'usage...")
    subs_enriched = df_subs.merge(usage_agg, on='subscription_id', how='left')
    numeric_cols = subs_enriched.select_dtypes(include=[np.number]).columns
    subs_enriched[numeric_cols] = subs_enriched[numeric_cols].fillna(0)

    # 5. Consolidation au niveau Compte (Account)
    print("Consolidation au niveau Account...")
    # On prend la moyenne des métriques d'usage par compte (si plusieurs abos)
    account_usage = subs_enriched.groupby('account_id').agg({
        'usage_count_sum': 'sum',
        'usage_count_mean': 'mean',
        'usage_duration_secs_sum': 'sum',
        'error_count_sum': 'sum',
        'mrr_amount': 'sum',
        'churn_flag': 'max' # Si un des abos a churn, le compte est marqué
    }).reset_index()

    master_df = df_accounts.merge(account_usage, on='account_id', how='left')
    master_df = master_df.merge(tickets_agg, on='account_id', how='left')
    
    # Résolution des doublons churn_flag
    if 'churn_flag_x' in master_df.columns:
        master_df['churn_flag'] = master_df['churn_flag_x']
        master_df.drop(columns=['churn_flag_x', 'churn_flag_y'], inplace=True, errors='ignore')
    
    # Nettoyage final
    numeric_master = master_df.select_dtypes(include=[np.number]).columns
    master_df[numeric_master] = master_df[numeric_master].fillna(0)
    
    # 6. Sauvegarde
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "master_dataset.csv")
    master_df.to_csv(output_path, index=False)
    
    print(f"Dataset masterisé généré : {master_df.shape[0]} lignes, {master_df.shape[1]} colonnes.")
    print(f"Fichier sauvegardé dans : {output_path}")

if __name__ == "__main__":
    build_master_dataset()
