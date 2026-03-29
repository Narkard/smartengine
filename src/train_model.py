import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

def train_churn_model():
    print("--- Début de la Modélisation (Sprint 3) ---")
    
    # 1. Chargement du dataset masterisé
    df = pd.read_csv("outputs/master_dataset.csv")
    
    # 2. Préparation des features
    # On exclut les IDs et la cible
    # On simplifie pour cette version (pas d'encodage des colonnes catégorielles complexes)
    # On utilise 'churn_flag' comme cible (y)
    
    features = [
        'seats', 'is_trial', 'usage_count_sum', 'usage_count_mean', 
        'usage_duration_secs_sum', 'error_count_sum', 'mrr_amount', 
        'ticket_count', 'resolution_time_hours', 'satisfaction_score', 
        'escalation_flag'
    ]
    
    X = df[features].copy()
    y = df['churn_flag']
    
    # Conversion des booléens en entiers
    X['is_trial'] = X['is_trial'].astype(int)
    
    # 3. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Entraînement
    print("Entraînement du modèle RandomForest...")
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    # 5. Évaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("\n--- Performances du Modèle ---")
    print(f"Précision (Accuracy) : {acc:.2f}")
    print("\nRapport de Classification :")
    print(classification_report(y_test, y_pred))
    
    # 6. Importance des variables
    importances = pd.DataFrame({
        'variable': features,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n--- Importance des Variables ---")
    print(importances)
    
    # 7. Sauvegarde
    os.makedirs("src", exist_ok=True)
    joblib.dump(model, "src/churn_model.pkl")
    print("\nModèle sauvegardé dans : src/churn_model.pkl")

if __name__ == "__main__":
    train_churn_model()
