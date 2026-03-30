import pandas as pd
import os

# Configuration des chemins
RAW_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/raw/"
CLEANED_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/cleaned/"

if not os.path.exists(CLEANED_DIR):
    os.makedirs(CLEANED_DIR)

def clean_data():
    """Nettoyage des données brutes (imputation, outliers, types)."""
    print("--- 1. Nettoyage des Données (src/clean_data.py) ---")
    
    # 1. Chargement
    accounts = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_accounts.csv"))
    support = pd.read_csv(os.path.join(RAW_DIR, "ravenstack_support_tickets.csv"))
    
    # 2. Imputation: satisfaction_score
    support['satisfaction_score'] = support['satisfaction_score'].fillna(support['satisfaction_score'].mean())
    
    # 3. Sauvegarde
    support.to_csv(os.path.join(CLEANED_DIR, "support_cleaned.csv"), index=False)
    accounts.to_csv(os.path.join(CLEANED_DIR, "accounts_cleaned.csv"), index=False)
    
    print("SUCCÈS : Données nettoyées.")

if __name__ == "__main__":
    clean_data()
