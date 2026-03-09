import pandas as pd
import numpy as np
import os
import json

# Chemins des fichiers bruts
DATA_DIR = "../data/raw"
ACCOUNTS_PATH = os.path.join(DATA_DIR, "ravenstack_accounts.csv")
SUBS_PATH = os.path.join(DATA_DIR, "ravenstack_subscriptions.csv")
USAGE_PATH = os.path.join(DATA_DIR, "ravenstack_feature_usage.csv")
TICKETS_PATH = os.path.join(DATA_DIR, "ravenstack_support_tickets.csv")
CHURN_PATH = os.path.join(DATA_DIR, "ravenstack_churn_events.csv")

def explore_and_clean_data():
    print("--- DEBUT DE L'ANALYSE ---")
    
    # 1. Chargement des données
    accounts = pd.read_csv(ACCOUNTS_PATH)
    subs = pd.read_csv(SUBS_PATH)
    usage = pd.read_csv(USAGE_PATH)
    tickets = pd.read_csv(TICKETS_PATH)
    churn = pd.read_csv(CHURN_PATH)
    
    # 2. Agrégation des comportements au niveau des abonnements et comptes
    print("Agregation de l'usage...")
    # On calcule le volume d'utilisation, la durée et les erreurs par abonnement
    usage_agg = usage.groupby('subscription_id').agg({
        'usage_count': 'sum',
        'usage_duration_secs': 'sum',
        'error_count': 'sum'
    }).reset_index()
    
    # Jointure des abonnements et de leur usage, avec ajout de la variable cible
    # Pour déterminer si un abo a churn, on regarde son churn_flag.
    subs_enriched = subs.merge(usage_agg, on='subscription_id', how='left')
    subs_enriched.fillna({'usage_count': 0, 'usage_duration_secs': 0, 'error_count': 0}, inplace=True)
    
    print("Agregation des tickets...")
    tickets_agg = tickets.groupby('account_id').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean',
        'escalation_flag': 'sum'
    }).rename(columns={'ticket_id': 'ticket_count'}).reset_index()
    
    # 3. Construction des données comptes
    accounts_enriched = accounts.merge(tickets_agg, on='account_id', how='left')
    accounts_enriched.fillna({'ticket_count': 0, 'resolution_time_hours': 0, 'escalation_flag': 0}, inplace=True)
    
    # Ajout du revenu total de l'abonnement en cours (ou dernier connu) par account
    active_subs = subs_enriched.sort_values(by=['account_id', 'start_date']).drop_duplicates(subset=['account_id'], keep='last')
    dataset = accounts_enriched.merge(active_subs[['account_id', 'mrr_amount', 'usage_count', 'error_count', 'churn_flag']], on='account_id', how='inner')
    
    dataset.rename(columns={'churn_flag_y': 'target_churn'}, inplace=True)
    
    print(f"Dataset d'entrainement construit : {dataset.shape[0]} comptes, {dataset.shape[1]} variables.")
    
    # 4. Identification basique des signaux précurseurs (corrélations simples)
    correlations = dataset[['target_churn', 'mrr_amount', 'usage_count', 'error_count', 'ticket_count', 'escalation_flag']].corr()['target_churn'].sort_values()
    print("\nCorrélations avec le churn (Signaux précurseurs) :")
    print(correlations)

    # 5. Sauvegarde des datasets masterisés dans outputs
    os.makedirs("../outputs", exist_ok=True)
    dataset.to_csv("../outputs/master_dataset.csv", index=False)
    print("\nDataset master enregistré dans /outputs/master_dataset.csv")

if __name__ == "__main__":
    explore_and_clean_data()
