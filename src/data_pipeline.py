import pandas as pd
import numpy as np
import os

# Configuration des chemins (chemins relatifs à la racine du projet)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Fichiers sources
ACCOUNTS_PATH = os.path.join(DATA_DIR, "ravenstack_accounts.csv")
SUBS_PATH = os.path.join(DATA_DIR, "ravenstack_subscriptions.csv")
USAGE_PATH = os.path.join(DATA_DIR, "ravenstack_feature_usage.csv")
TICKETS_PATH = os.path.join(DATA_DIR, "ravenstack_support_tickets.csv")
CHURN_PATH = os.path.join(DATA_DIR, "ravenstack_churn_events.csv")

def run_pipeline():
    print("--- Démarrage du Pipeline de Données (Sprint 2) ---")
    
    # 1. Chargement des données
    print("Chargement des fichiers CSV...")
    try:
        accounts = pd.read_csv(ACCOUNTS_PATH)
        subs = pd.read_csv(SUBS_PATH)
        usage = pd.read_csv(USAGE_PATH)
        tickets = pd.read_csv(TICKETS_PATH)
        # churn_events = pd.read_csv(CHURN_PATH) # Utile pour analyse qualitative, mais target est déjà dans accounts/subs
    except FileNotFoundError as e:
        print(f"Erreur : Fichier manquant. {e}")
        return

    # 2. Nettoyage et Imputation
    print("Nettoyage des données...")
    # Imputation du satisfaction_score par la moyenne
    mean_sat = tickets['satisfaction_score'].mean()
    tickets['satisfaction_score'] = tickets['satisfaction_score'].fillna(mean_sat)
    
    # Gestion des dates
    usage['usage_date'] = pd.to_datetime(usage['usage_date'])
    subs['start_date'] = pd.to_datetime(subs['start_date'])
    
    # 3. Feature Engineering - Usage
    print("Feature Engineering : Usage...")
    # Agrégation par compte (via subscription_id)
    # D'abord on joint usage et subs pour avoir l'account_id
    usage_with_account = usage.merge(subs[['subscription_id', 'account_id']], on='subscription_id', how='left')
    
    usage_agg = usage_with_account.groupby('account_id').agg({
        'usage_count': ['sum', 'mean', 'std'],
        'usage_duration_secs': ['sum', 'mean'],
        'error_count': ['sum', 'mean'],
        'is_beta_feature': 'sum'
    })
    usage_agg.columns = ['_'.join(col).strip() for col in usage_agg.columns.values]
    usage_agg = usage_agg.reset_index()

    # 4. Feature Engineering - Support
    print("Feature Engineering : Support...")
    tickets_agg = tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean',
        'escalation_flag': 'sum',
        'first_response_time_minutes': 'mean'
    }).rename(columns={'ticket_id': 'ticket_count'}).reset_index()

    # 5. Feature Engineering - Abonnements
    print("Feature Engineering : Abonnements...")
    # On prend le dernier état de l'abonnement par compte
    latest_subs = subs.sort_values('start_date').groupby('account_id').tail(1)
    
    # 6. Fusion finale (Master Dataset)
    print("Construction du Master Dataset...")
    master = accounts.merge(usage_agg, on='account_id', how='left')
    master = master.merge(tickets_agg, on='account_id', how='left')
    master = master.merge(latest_subs[['account_id', 'mrr_amount', 'billing_frequency', 'auto_renew_flag', 'seats']], on='account_id', how='left')

    # Remplissage des valeurs manquantes après fusion (ex: clients sans tickets)
    cols_to_zero = [col for col in master.columns if 'sum' in col or 'count' in col or 'flag' in col]
    master[cols_to_zero] = master[cols_to_zero].fillna(0)
    
    # Imputation pour les colonnes de moyennes/std
    for col in master.columns:
        if master[col].isnull().any():
            master[col] = master[col].fillna(master[col].mean() if master[col].dtype != 'object' else 'Unknown')

    # 7. Encodage des variables catégorielles
    # industry, plan_tier, billing_frequency
    master = pd.get_dummies(master, columns=['industry', 'plan_tier', 'billing_frequency'], drop_first=True)

    # 8. Sauvegarde
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    master_path = os.path.join(OUTPUT_DIR, "master_dataset.csv")
    master.to_csv(master_path, index=False)
    
    print(f"✅ Pipeline terminé. Dataset : {master.shape[0]} lignes, {master.shape[1]} colonnes.")
    print(f"📂 Fichier enregistré : {master_path}")

if __name__ == "__main__":
    run_pipeline()
