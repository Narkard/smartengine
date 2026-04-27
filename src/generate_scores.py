import pandas as pd
import numpy as np
import os
import joblib

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "outputs", "master_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "churn_model.joblib")
OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "scores.csv")

def generate_scores():
    print("--- 🚀 Génération des scores de churn ---")
    
    # 1. Chargement des données et du modèle
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : {DATA_PATH} introuvable.")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Erreur : {MODEL_PATH} introuvable.")
        return

    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation des features (même logique que train_model.py)
    # On identifie la cible pour l'exclure
    target_col = 'churn_flag' if 'churn_flag' in df.columns else 'target_churn'
    
    exclude = [
        'account_id', 'account_name', 'signup_date', 'country', 
        'referral_source', 'plan_tier_x', 'is_trial', target_col
    ]
    X = df.drop(columns=[c for c in exclude if c in df.columns])
    X = X.fillna(0)
    
    # S'assurer que les colonnes correspondent au modèle
    model_features = model.feature_names_in_
    X = X[model_features]

    # 3. Calcul des probabilités
    print(f"Calcul des probabilités pour {len(df)} comptes...")
    # predict_proba renvoie [prob_0, prob_1]
    scores = model.predict_proba(X)[:, 1]
    
    # 4. Construction du DataFrame final
    results = pd.DataFrame({
        'account_id': df['account_id'],
        'churn_score': scores
    })
    
    # Définition des niveaux de risque
    def get_risk_level(score):
        if score >= 0.65:
            return 'High'
        elif score >= 0.35:
            return 'Medium'
        else:
            return 'Low'
    
    results['risk_level'] = results['churn_score'].apply(get_risk_level)
    
    # 5. Sauvegarde
    results.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Scores sauvegardés dans : {OUTPUT_PATH}")
    
    # 6. Distribution des risques
    print("\n📊 Distribution des niveaux de risque :")
    dist = results['risk_level'].value_counts()
    perc = results['risk_level'].value_counts(normalize=True) * 100
    
    for level in ['High', 'Medium', 'Low']:
        count = dist.get(level, 0)
        p = perc.get(level, 0)
        print(f"- {level}: {count} ({p:.1f}%)")

if __name__ == "__main__":
    generate_scores()
