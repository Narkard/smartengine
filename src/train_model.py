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
MODEL_DIR = os.path.join(BASE_DIR, "outputs", "models")
MODEL_PATH = os.path.join(MODEL_DIR, "churn_model.joblib")

def train_gbm_model():
    print("--- 🚀 Sprint 3 : Entraînement du Modèle (GBM) ---")
    
    if not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : {DATA_PATH} introuvable. Exécutez d'abord le pipeline.")
        return

    # 1. Chargement et Nettoyage
    df = pd.read_csv(DATA_PATH)
    
    # 1.1 Préparation de la cible (churn_flag est booléen)
    if 'churn_flag' in df.columns:
        y = df['churn_flag'].astype(int)
        target_col = 'churn_flag'
    elif 'target_churn' in df.columns:
        y = df['target_churn'].astype(int)
        target_col = 'target_churn'
    else:
        print("❌ Erreur : Colonne cible (churn_flag ou target_churn) introuvable.")
        return

    # Exclusion des colonnes d'identification et de la cible
    exclude = [
        'account_id', 'account_name', 'signup_date', 'country', 
        'referral_source', 'plan_tier_x', 'is_trial', target_col
    ]
    
    X = df.drop(columns=[c for c in exclude if c in df.columns])
    
    # 1.5 Gestion des valeurs manquantes (NaN)
    X = X.fillna(0)

    # 2. Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. Entraînement GBM
    print("Entraînement du GradientBoostingClassifier...")
    model = GradientBoostingClassifier(
        n_estimators=200, 
        learning_rate=0.05,
        max_depth=4,
        random_state=42
    )
    
    model.fit(X_train, y_train)

    # 4. Évaluation
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    print("\n✅ Évaluation du modèle :")
    print(classification_report(y_test, y_pred))
    
    # 5. Features Importances
    importances = model.feature_importances_
    feature_importance_df = pd.DataFrame({'feature': X.columns, 'importance': importances})
    top_features = feature_importance_df.sort_values(by='importance', ascending=False).head(5)
    print("\n🔍 Top 5 variables les plus importantes :")
    print(top_features)

    # 6. Sauvegarde
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    
    # Sauvegarde des métriques pour le rapport
    metrics = {
        "accuracy": report["accuracy"],
        "precision_churn": report["1"]["precision"],
        "recall_churn": report["1"]["recall"],
        "f1_churn": report["1"]["f1-score"],
        "top_features": top_features.to_dict(orient="records")
    }
    joblib.dump(metrics, os.path.join(MODEL_DIR, "evaluation_metrics.joblib"))
    
    print(f"\n💾 Modèle et métriques sauvegardés dans : {MODEL_DIR}")

if __name__ == "__main__":
    train_gbm_model()
