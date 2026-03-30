import pandas as pd
import numpy as np
import os

# Configuration
RAW_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/raw/"
CLEANED_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/cleaned/"
FEATURES_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/features/"

if not os.path.exists(FEATURES_DIR):
    os.makedirs(FEATURES_DIR)

def build_features():
    print("--- 4.3 Feature Engineering Avancé ---")
    
    # 1. Chargement
    sub = pd.read_csv(os.path.join(CLEANED_DIR, "subscriptions_cleaned.csv"), parse_dates=['start_date'])
    usage = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_feature_usage.csv"), parse_dates=['usage_date'])
    support = pd.read_csv(os.path.join(CLEANED_DIR, "support_cleaned.csv"), parse_dates=['submitted_at'])
    ref_date = usage['usage_date'].max()

    # --- CATEGORIE 1 : USAGE & ENGAGEMENT ---
    print("Traitement de l'usage et de l'engagement...")
    usage = usage.sort_values(['subscription_id', 'usage_date'])
    
    # Recence de l'usage (Engagement)
    last_usage = usage.groupby('subscription_id')['usage_date'].max()
    usage_recency = (ref_date - last_usage).dt.days.rename('days_since_last_usage')
    
    # Tendance d'usage sur les 2 derniers mois (Signal fort de churn)
    # On compare la moyenne du dernier mois vs moyenne globale
    last_month_date = ref_date - pd.Timedelta(days=30)
    usage_recent = usage[usage['usage_date'] >= last_month_date].groupby('subscription_id')['usage_count'].mean()
    usage_global = usage.groupby('subscription_id')['usage_count'].mean()
    usage_trend = (usage_recent / usage_global - 1).rename('usage_trend_30d')
    
    # Diversité des fonctionnalités utilisées
    feature_diversity = usage.groupby('subscription_id')['feature_name'].nunique().rename('nb_unique_features')

    usage_features = pd.concat([usage_recency, usage_trend, feature_diversity], axis=1).fillna(0)
    
    # Mapping vers account_id
    sub_map = sub[['subscription_id', 'account_id']].drop_duplicates()
    usage_agg = usage_features.merge(sub_map, on='subscription_id', how='inner')
    usage_agg = usage_agg.groupby('account_id').mean(numeric_only=True).reset_index()

    # --- CATEGORIE 2 : SUPPORT ---
    print("Traitement du support client...")
    support['is_critical'] = support['priority'].apply(lambda x: 1 if x in ['high', 'urgent'] else 0)
    
    support_agg = support.groupby('account_id').agg({
        'ticket_id': 'count',
        'is_critical': 'sum',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean'
    }).rename(columns={'ticket_id': 'total_tickets', 'is_critical': 'nb_critical_tickets'})
    
    # Ratio de tickets critiques
    support_agg['critical_ratio'] = support_agg['nb_critical_tickets'] / support_agg['total_tickets']
    support_agg.reset_index(inplace=True)

    # --- CATEGORIE 3 : FINANCIER & TEMPOREL ---
    print("Traitement financier et temporel...")
    # Ancienneté
    sub['seniority_months'] = ((ref_date - sub['start_date']).dt.days / 30).astype(int)
    
    # Saisonnalité (Mois d'inscription)
    sub['signup_month'] = sub['start_date'].dt.month
    
    sub_agg = sub.groupby('account_id').agg({
        'seniority_months': 'max',
        'signup_month': 'first',
        'mrr_amount': 'mean',
        'upgrade_flag': 'sum'
    }).rename(columns={'upgrade_flag': 'nb_upgrades'})
    sub_agg.reset_index(inplace=True)

    # --- SAUVEGARDE ---
    usage_agg.to_csv(os.path.join(FEATURES_DIR, "usage_features.csv"), index=False)
    support_agg.to_csv(os.path.join(FEATURES_DIR, "support_features.csv"), index=False)
    sub_agg.to_csv(os.path.join(FEATURES_DIR, "sub_features.csv"), index=False)
    
    print(f"SUCCÈS : {usage_agg.shape[1] + support_agg.shape[1] + sub_agg.shape[1] - 3} nouvelles features générées.")

if __name__ == "__main__":
    build_features()
