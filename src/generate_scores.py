import pandas as pd
import numpy as np
import os
import joblib

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "churn_model.joblib")
FEATURES_PATH = os.path.join(BASE_DIR, "outputs", "models", "model_features.joblib")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "scores.csv")

def generate_scores():
    print("--- Génération des Scores de Churn ---")
    
    # 1. Chargement du modèle et des features
    if not os.path.exists(MODEL_PATH) or not os.path.exists(FEATURES_PATH):
        print("Erreur : Modèle ou liste de features introuvable. Lancez train_model.py d'abord.")
        return
        
    model = joblib.load(MODEL_PATH)
    features = joblib.load(FEATURES_PATH)
    
    # 2. Chargement des données
    df = pd.read_csv(DATA_PATH)
    
    # 3. Préparation des données pour la prédiction
    # On utilise exactement les mêmes features qu'à l'entraînement
    X = df[features]
    
    # 4. Calcul des probabilités
    # predict_proba renvoie [prob_0, prob_1]
    probabilities = model.predict_proba(X)[:, 1]
    
    # 5. Création du fichier de scores
    results = pd.DataFrame({
        'account_id': df['account_id'],
        'churn_probability': probabilities
    })
    
    # Ajout du niveau de risque selon les seuils du PO
    def get_risk_level(prob):
        if prob >= 0.65: return 'High'
        elif prob >= 0.35: return 'Medium'
        else: return 'Low'
        
    results['risk_level'] = results['churn_probability'].apply(get_risk_level)
    
    # 6. Sauvegarde
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"SUCCÈS : Scores générés dans {OUTPUT_PATH}")
    print(results['risk_level'].value_counts())

if __name__ == "__main__":
    generate_scores()
