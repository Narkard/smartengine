import pandas as pd
import os

# Configuration des chemins
RAW_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/raw/"
CLEANED_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/cleaned/"
FEATURES_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/features/"

if not os.path.exists(FEATURES_DIR):
    os.makedirs(FEATURES_DIR)

def build_features():
    """Création des variables dérivées."""
    print("--- 2. Feature Engineering (src/build_features.py) ---")
    
    # 1. Chargement
    sub = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_subscriptions.csv"))
    usage = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_feature_usage.csv"))
    support_cleaned = pd.read_csv(os.path.join(CLEANED_DIR, "support_cleaned.csv"))
    
    # 2. Usage Features
    usage_agg_sub = usage.groupby('subscription_id').agg({
        'usage_count': ['sum', 'mean'],
        'usage_duration_secs': ['sum', 'mean'],
        'error_count': 'sum'
    })
    usage_agg_sub.columns = ['usage_total', 'usage_avg', 'duration_total', 'duration_avg', 'total_errors']
    usage_agg_sub.reset_index(inplace=True)
    
    sub_map = sub[['subscription_id', 'account_id']].drop_duplicates()
    usage_agg = usage_agg_sub.merge(sub_map, on='subscription_id', how='inner')
    usage_agg = usage_agg.groupby('account_id').agg({
        'usage_total': 'sum',
        'usage_avg': 'mean',
        'duration_total': 'sum',
        'duration_avg': 'mean',
        'total_errors': 'sum'
    }).reset_index()
    
    # 3. Support Features (nb_tickets, nb_critiques, resolution_time)
    support_cleaned['is_critical'] = support_cleaned['priority'].apply(lambda x: 1 if x in ['high', 'urgent'] else 0)
    support_agg = support_cleaned.groupby('account_id').agg({
        'ticket_id': 'count',
        'is_critical': 'sum',
        'resolution_time_hours': 'mean',
        'satisfaction_score': 'mean'
    })
    support_agg.columns = ['nb_tickets', 'nb_critiques', 'avg_resolution_time', 'avg_satisfaction']
    support_agg.reset_index(inplace=True)
    
    # 4. Subscription Features
    sub_agg = sub.groupby('account_id').agg({
        'mrr_amount': 'max',
        'plan_tier': 'first',
        'billing_frequency': 'first'
    }).reset_index()
    sub_agg = pd.get_dummies(sub_agg, columns=['plan_tier', 'billing_frequency'], prefix=['plan', 'freq'])
    
    # 5. Sauvegarde
    usage_agg.to_csv(os.path.join(FEATURES_DIR, "usage_features.csv"), index=False)
    support_agg.to_csv(os.path.join(FEATURES_DIR, "support_features.csv"), index=False)
    sub_agg.to_csv(os.path.join(FEATURES_DIR, "sub_features.csv"), index=False)
    
    print("SUCCÈS : Features générées.")

if __name__ == "__main__":
    build_features()
