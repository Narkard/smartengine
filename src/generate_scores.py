import pandas as pd
import numpy as np
import os
import joblib

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "churn_model.joblib")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "scores.csv")

def generate_scores():
    print("--- Génération des Scores de Risque ---")
    
    # 1. Chargement
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation
    target = 'churn_flag'
    X = df.drop(columns=[target], errors='ignore').select_dtypes(include=[np.number])
    X = X.drop(columns=['account_id'], errors='ignore')
    
    # 3. Calcul des probabilités
    # La probabilité de churn est la deuxième colonne de predict_proba
    scores = model.predict_proba(X)[:, 1]
    
    # 4. Création du DataFrame de sortie
    results = pd.DataFrame({
        'account_id': df['account_id'],
        'churn_score': np.round(scores, 4)
    })
    
    # 5. Définition des niveaux de risque
    def get_risk_level(score):
        if score < 0.3: return "Low"
        elif score < 0.7: return "Medium"
        else: return "High"
        
    results['risk_level'] = results['churn_score'].apply(get_risk_level)
    
    # 6. Sauvegarde
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"SUCCÈS : Scores générés pour {len(results)} comptes dans {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_scores()
