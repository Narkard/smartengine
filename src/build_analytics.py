import pandas as pd
import os

# Configuration (Abstractions relatives)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CLEANED_DIR = os.path.join(PROCESSED_DIR, "cleaned")
FEATURES_DIR = os.path.join(PROCESSED_DIR, "features")
FINAL_DIR = PROCESSED_DIR

def build_analytics():
    print("--- Assemblage de la Table Analytique (analytics.csv) ---")
    
    # 1. Table de référence : accounts
    acc = pd.read_csv(os.path.join(CLEANED_DIR, "accounts_cleaned.csv"))
    
    # 2. Chargement des features enrichies
    sub_agg = pd.read_csv(os.path.join(FEATURES_DIR, "sub_features.csv"))
    usage_agg = pd.read_csv(os.path.join(FEATURES_DIR, "usage_features.csv"))
    support_agg = pd.read_csv(os.path.join(FEATURES_DIR, "support_features.csv"))
    
    # 3. Jointure graduelle
    print("Jointure des fichiers...")
    analytics = acc.merge(sub_agg, on='account_id', how='left')
    analytics = analytics.merge(usage_agg, on='account_id', how='left')
    analytics = analytics.merge(support_agg, on='account_id', how='left')
    
    # 4. Traitement de la variable cible (Recalculée via churn_events)
    # Justification : churnflag est jugé peu fiable (erreurs de saisie, délais de mise à jour).
    # churn_events est la source de vérité pour les résiliations réelles.
    print("Action : Recalcul de la cible via churn_events...")
    churn_events = pd.read_csv(os.path.join(CLEANED_DIR, "churn_cleaned.csv"))
    churned_accounts = churn_events['account_id'].unique()
    analytics['churn_flag'] = analytics['account_id'].isin(churned_accounts).astype(int)
    
    # 5. Encodage des dernières variables catégorielles
    analytics = pd.get_dummies(analytics, columns=['industry', 'plan_tier'], prefix=['ind', 'plan'])
    
    # 6. Gestion des valeurs nulles post-jointure (comptes sans usage ou support)
    analytics.fillna(0, inplace=True)
    
    # 7. Nettoyage des colonnes techniques non prédictives
    cols_to_drop = ['subscription_id']
    analytics = analytics.drop(columns=[c for c in cols_to_drop if c in analytics.columns])
    
    # 8. Sauvegarde finale
    output_path = os.path.join(FINAL_DIR, "analytics.csv")
    analytics.to_csv(output_path, index=False)
    
    print(f"SUCCÈS : Table analytique générée.")
    print(f"Dimensions : {analytics.shape[0]} lignes x {analytics.shape[1]} variables.")
    print(f"Cible (Churn) : {analytics['churn_flag'].sum()} cas positifs sur {len(analytics)}.")

if __name__ == "__main__":
    build_analytics()
