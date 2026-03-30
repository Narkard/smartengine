import pandas as pd
import os

# Configuration des chemins
CLEANED_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/cleaned/"
FEATURES_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/features/"
FINAL_DIR = "C:/Users/leola/Desktop/Projet smartEngine/data/processed/"

def build_analytics():
    """Jointure finale vers la table analytique."""
    print("--- 3. Construction de la Table Analytique (src/build_analytics.py) ---")
    
    # 1. Chargement
    acc = pd.read_csv(os.path.join(CLEANED_DIR, "accounts_cleaned.csv"))
    usage_agg = pd.read_csv(os.path.join(FEATURES_DIR, "usage_features.csv"))
    support_agg = pd.read_csv(os.path.join(FEATURES_DIR, "support_features.csv"))
    sub_agg = pd.read_csv(os.path.join(FEATURES_DIR, "sub_features.csv"))
    
    # 2. Jointure
    master = acc.merge(sub_agg, on='account_id', how='left')
    master = master.merge(usage_agg, on='account_id', how='left')
    master = master.merge(support_agg, on='account_id', how='left')
    
    # 3. Encodage Industrie
    master = pd.get_dummies(master, columns=['industry'], prefix='ind')
    
    # 4. Nettoyage final
    master.fillna(0, inplace=True)
    
    # 5. Sauvegarde conforme au Kit 2 (analytics.csv)
    output_path = os.path.join(FINAL_DIR, "analytics.csv")
    master.to_csv(output_path, index=False)
    
    print(f"SUCCÈS : Table analytique générée ({master.shape[0]} lignes, {master.shape[1]} colonnes)")
    print(f"Fichier : {output_path}")

if __name__ == "__main__":
    build_analytics()
