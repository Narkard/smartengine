import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_DIR = os.path.join(BASE_DIR, "outputs", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "churn_model.joblib")

def train_gbm_model():
    print("--- 🚀 Sprint 3 : Entraînement du Modèle (GBM) ---")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : {DATA_PATH} introuvable. Exécutez d'abord les scripts du Sprint 2.")
        return

    # 1. Chargement et Nettoyage
    df = pd.read_csv(DATA_PATH)
    
    # Exclusion des IDs, noms, dates et colonnes non-numériques ou redondantes
    exclude = [
        'account_id', 'account_name', 'signup_date', 'country', 
        'referral_source', 'plan_tier_x', 'is_trial', 'churn_flag'
    ]
    X = df.drop(columns=[c for c in exclude if c in df.columns] + ['target_churn'])
    y = df['target_churn'].astype(int)
    
    # 1.5 Gestion des valeurs manquantes (NaN)
    X = X.fillna(0)

    # 2. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Entraînement GBM
    print("Entraînement du GradientBoostingClassifier sur analytics.csv...")
    model = GradientBoostingClassifier(
        n_estimators=200, 
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )
    
    model.fit(X_train, y_train)

    # 4. Évaluation
    y_pred = model.predict(X_test)
    print("\n✅ Évaluation du modèle :")
    print(classification_report(y_test, y_pred))
    
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    # 5. Features Importances
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': importances})
    print("\n🔍 Top 5 variables les plus importantes :")
    print(feature_importance_df.sort_values(by='importance', ascending=False).head(5))

    # 6. Sauvegarde
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"\n💾 Modèle sauvegardé dans : {MODEL_PATH}")

if __name__ == "__main__":
    train_gbm_model()
