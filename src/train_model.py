import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import f1_score, classification_report

# Configuration des chemins (Abstractions relatives)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_DIR = os.path.join(BASE_DIR, "outputs", "models")

def train_model():
    print("--- Démarrage de l'Entraînement des Modèles ---")
    
    # 1. Chargement des données
    if not os.path.exists(DATA_PATH):
        print(f"Erreur : Le fichier {DATA_PATH} est introuvable.")
        return
    
    df = pd.read_csv(DATA_PATH)
    
    # 2. Séparation X et y
    # On garde uniquement les colonnes numériques pour l'entraînement
    target = 'churn_flag'
    X = df.drop(columns=[target], errors='ignore').select_dtypes(include=[np.number])
    # On s'assure de ne pas garder d'identifiants même s'ils sont numériques (si présents)
    cols_to_drop = ['account_id']
    X = X.drop(columns=[c for c in cols_to_drop if c in X.columns], errors='ignore')
    y = df[target]
    
    # 3. Split Train/Test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    
    # 4. Calcul du ratio Churn/Non-Churn
    churn_count = y_train.sum()
    non_churn_count = len(y_train) - churn_count
    ratio = non_churn_count / churn_count
    
    print(f"Distribution dans le jeu d'entraînement :")
    print(f" - Non-Churn : {non_churn_count}")
    print(f" - Churn     : {churn_count}")
    print(f" - Ratio (Neg/Pos) : {ratio:.2f}")

    # 5. Entraînement des modèles
    models = {
        "LogisticRegression": LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42),
        "RandomForest": RandomForestClassifier(class_weight='balanced', random_state=42),
        "XGBoost": XGBClassifier(scale_pos_weight=ratio, random_state=42, use_label_encoder=False, eval_metric='logloss')
    }
    
    best_f1 = 0
    best_model = None
    best_model_name = ""
    
    for name, model in models.items():
        print(f"\nEntraînement de {name}...")
        model.fit(X_train, y_train)
        
        # Prédiction et évaluation
        y_pred = model.predict(X_test)
        current_f1 = f1_score(y_test, y_pred)
        
        print(f"Score F1 (Churn) : {current_f1:.4f}")
        
        if current_f1 > best_f1:
            best_f1 = current_f1
            best_model = model
            best_model_name = name

    # 6. Sauvegarde du meilleur modèle
    print(f"\n--- RÉSULTAT FINAL ---")
    print(f"Meilleur modèle identifié : {best_model_name} (F1 = {best_f1:.4f})")
    
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        
    model_output_path = os.path.join(MODEL_DIR, "churn_model.joblib")
    joblib.dump(best_model, model_output_path)
    
    # Sauvegarde des colonnes pour le déploiement futur
    joblib.dump(list(X.columns), os.path.join(MODEL_DIR, "model_features.joblib"))
    
    print(f"SUCCÈS : Modèle sauvegardé dans {model_output_path}")

if __name__ == "__main__":
    train_model()
