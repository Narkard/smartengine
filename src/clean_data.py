import pandas as pd
import numpy as np
import os

# Configuration des chemins (Abstractions relatives)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
CLEANED_DIR = os.path.join(PROCESSED_DIR, "cleaned")

if not os.path.exists(CLEANED_DIR):
    os.makedirs(CLEANED_DIR)

def clean_data():
    print("--- Démarrage du Nettoyage des Données (Conformité Kit 2) ---")
    
    # 1. Chargement
    acc = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_accounts.csv"))
    sub = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_subscriptions.csv"))
    usage = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_feature_usage.csv"))
    support = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_support_tickets.csv"))
    churn = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_churn_events.csv"))

    # Exclusion explicite de churn_flag (source jugée non fiable)
    print("Action : Exclusion de churn_flag des sources initiales...")
    if 'churn_flag' in acc.columns:
        acc = acc.drop(columns=['churn_flag'])
    if 'churn_flag' in sub.columns:
        sub = sub.drop(columns=['churn_flag'])

    # 2. Traitement des Types Incorrects (Dates)
    print("Action : Conversion des colonnes temporelles...")
    sub['start_date'] = pd.to_datetime(sub['start_date'], errors='coerce')
    sub['end_date'] = pd.to_datetime(sub['end_date'], errors='coerce')
    support['submitted_at'] = pd.to_datetime(support['submitted_at'], errors='coerce')
    
    # 3. Traitement des Valeurs Manquantes (Imputation)
    # Satisfaction Score : 41% de manquants. On impute par la médiane pour ne pas biaiser par les extrêmes.
    print("Action : Imputation du satisfaction_score par la médiane...")
    med_sat = support['satisfaction_score'].median()
    support['satisfaction_score'] = support['satisfaction_score'].fillna(med_sat)
    
    # Feedback Text : On remplace par "N/A" car c'est une donnée textuelle.
    churn['feedback_text'] = churn['feedback_text'].fillna("No feedback provided")

    # 4. Traitement des Incohérences Inter-fichiers
    # Vérifier si tous les comptes de subscriptions existent dans accounts
    print("Action : Vérification des orphelins...")
    orphans = sub[~sub['account_id'].isin(acc['account_id'])]
    if not orphans.empty:
        print(f"Alerte : {len(orphans)} abonnements sans compte parent supprimés.")
        sub = sub[sub['account_id'].isin(acc['account_id'])]

    # 5. Outliers (Winsorisation sur le MRR)
    # On plafonne le MRR au 99ème percentile pour éviter que des comptes géants ne faussent les moyennes
    q99 = sub['mrr_amount'].quantile(0.99)
    sub['mrr_amount'] = sub['mrr_amount'].clip(upper=q99)

    # 6. Sauvegarde des fichiers nettoyés
    acc.to_csv(os.path.join(CLEANED_DIR, "accounts_cleaned.csv"), index=False)
    sub.to_csv(os.path.join(CLEANED_DIR, "subscriptions_cleaned.csv"), index=False)
    usage.to_csv(os.path.join(CLEANED_DIR, "usage_cleaned.csv"), index=False)
    support.to_csv(os.path.join(CLEANED_DIR, "support_cleaned.csv"), index=False)
    churn.to_csv(os.path.join(CLEANED_DIR, "churn_cleaned.csv"), index=False)
    
    print(f"SUCCÈS : Données nettoyées et prêtes dans {CLEANED_DIR}")

if __name__ == "__main__":
    clean_data()
