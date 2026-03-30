import pandas as pd
import numpy as np
import os

# Configuration des chemins
RAW_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/raw/"
PROCESSED_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/"

if not os.path.exists(PROCESSED_DIR):
    os.makedirs(PROCESSED_DIR)

def load_data():
    """Charge les 5 fichiers CSV de RavenStack."""
    accounts = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_accounts.csv"))
    subscriptions = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_subscriptions.csv"))
    feature_usage = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_feature_usage.csv"))
    support_tickets = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_support_tickets.csv"))
    churn_events = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_churn_events.csv"))
    return accounts, subscriptions, feature_usage, support_tickets, churn_events

def process_data():
    print("--- Démarrage du Traitement des Données (Sprint 2) ---")
    acc, sub, usage, support, churn = load_data()

    # 1. Feature Engineering: Usage
    # On agrège d'abord par subscription_id (seule clé dispo dans usage)
    usage_agg_sub = usage.groupby('subscription_id').agg({
        'usage_count': ['sum', 'mean'],
        'usage_duration_secs': ['sum', 'mean'],
        'error_count': 'sum'
    })
    usage_agg_sub.columns = ['usage_total', 'usage_avg', 'duration_total', 'duration_avg', 'total_errors']
    usage_agg_sub.reset_index(inplace=True)

    # On lie ensuite l'usage à l'account_id via le fichier subscriptions
    sub_map = sub[['subscription_id', 'account_id']].drop_duplicates()
    usage_agg = usage_agg_sub.merge(sub_map, on='subscription_id', how='inner')
    
    # Agrégation finale par compte (au cas où un compte a plusieurs abonnements)
    usage_agg = usage_agg.groupby('account_id').agg({
        'usage_total': 'sum',
        'usage_avg': 'mean',
        'duration_total': 'sum',
        'duration_avg': 'mean',
        'total_errors': 'sum'
    }).reset_index()

    # 2. Feature Engineering: Support
    # Imputation du score de satisfaction par la moyenne
    support['satisfaction_score'] = support['satisfaction_score'].fillna(support['satisfaction_score'].mean())
    
    # Calcul du ratio de tickets résolus
    support['is_resolved'] = support['status'].apply(lambda x: 1 if x == 'resolved' else 0)
    
    support_agg = support.groupby('account_id').agg({
        'ticket_id': 'count',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean',
        'is_resolved': 'mean'
    })
    support_agg.columns = ['nb_tickets', 'avg_resolution_time', 'avg_satisfaction', 'resolution_rate']
    support_agg.reset_index(inplace=True)

    # 3. Feature Engineering: Subscriptions & Encoding
    # Encodage des variables catégorielles (Plan)
    sub_agg = sub.groupby('account_id').agg({
        'mrr_amount': 'max',
        'plan_tier': 'first',
        'billing_frequency': 'first'
    }).reset_index()
    
    # One-Hot Encoding simplifié
    sub_agg = pd.get_dummies(sub_agg, columns=['plan_tier', 'billing_frequency'], prefix=['plan', 'freq'])

    # 4. Jointure du Master Dataset
    master = acc.merge(sub_agg, on='account_id', how='left')
    master = master.merge(usage_agg, on='account_id', how='left')
    master = master.merge(support_agg, on='account_id', how='left')
    
    # Encodage de l'industrie
    master = pd.get_dummies(master, columns=['industry'], prefix='ind')

    # Gestion des valeurs nulles après jointure (comptes sans usage ou support)
    master.fillna(0, inplace=True)

    # 5. Label de Churn (Cible)
    # Le churn_flag est déjà dans accounts, mais on peut enrichir avec churn_events si besoin
    # Ici on garde le churn_flag binaire (0 ou 1)

    # Sauvegarde
    output_path = os.path.join(PROCESSED_DIR, "master_dataset.csv")
    master.to_csv(output_path, index=False)
    print(f"SUCCÈS : Master Dataset généré ({master.shape[0]} lignes, {master.shape[1]} colonnes)")
    print(f"Fichier disponible dans : {output_path}")

if __name__ == "__main__":
    process_data()
