import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "outputs", "master_dataset.csv")
MODEL_DIR = os.path.join(BASE_DIR, "src")
MODEL_PATH = os.path.join(MODEL_DIR, "churn_model.pkl")

def train_gbm_model():
    print("--- 🚀 Sprint 3 : Entraînement du Modèle (GBM) ---")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : {DATA_PATH} introuvable.")
        return

    # 1. Chargement et Nettoyage
    df = pd.read_csv(DATA_PATH)
    
    # Exclusion des IDs et dates
    exclude = ['account_id', 'account_name', 'signup_date', 'country', 'referral_source']
    X = df.drop(columns=[c for c in exclude if c in df.columns] + ['churn_flag'])
    y = df['churn_flag'].astype(int)

    # 2. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Entraînement GBM
    print("Entraînement du GradientBoostingClassifier...")
    # On utilise un learning_rate plus faible et on augmente n_estimators
    model = GradientBoostingClassifier(
        n_estimators=200, 
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )
    
    model.fit(X_train, y_train)

    # 4. Évaluation
    # On peut aussi jouer sur le seuil de décision si nécessaire
    y_pred = model.predict(X_test)
    print("\n✅ Évaluation du modèle :")
    print(classification_report(y_test, y_pred))
    
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    # 5. Features Importances
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': importances})
    print("\n🔍 Top 5 variables :")
    print(feature_importance_df.sort_values(by='importance', ascending=False).head(5))

    # 6. Sauvegarde
    joblib.dump(model, MODEL_PATH)
    print(f"\n💾 Modèle sauvegardé dans : {MODEL_PATH}")

if __name__ == "__main__":
    train_gbm_model()
