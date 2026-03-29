import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

def train_churn_model():
    print("--- Début de la Modélisation Avancée (Sprint 3 - Tuning) ---")
    
    # 1. Chargement du dataset masterisé
    df = pd.read_csv("outputs/master_dataset.csv")
    
    # 2. Préparation des features
    features = [
        'seats', 'is_trial', 'usage_count_sum', 'usage_trend', 
        'error_count_sum', 'mrr_amount', 
        'ticket_count', 'resolution_time_hours', 'satisfaction_score', 
        'escalation_flag'
    ]
    
    X = df[features].copy()
    y = df['churn_flag'].astype(int)
    
    # Conversion des booléens en entiers
    X['is_trial'] = X['is_trial'].astype(int)
    
    # 3. Split Train/Test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Optimisation par GridSearch
    print("Recherche des meilleurs hyperparamètres (GridSearch)...")
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 10, None],
        'min_samples_split': [2, 5],
        'class_weight': ['balanced', 'balanced_subsample']
    }
    
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, scoring='f1', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    print(f"Meilleurs paramètres : {grid_search.best_params_}")
    
    # 5. Évaluation
    y_pred = best_model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print("\n--- Performances du Modèle Optimisé ---")
    print(f"Précision (Accuracy) : {acc:.2f}")
    print("\nRapport de Classification :")
    print(classification_report(y_test, y_pred))
    
    print("\nMatrice de Confusion :")
    print(confusion_matrix(y_test, y_pred))
    
    # 6. Importance des variables
    importances = pd.DataFrame({
        'variable': features,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n--- Importance des Variables (Top 5) ---")
    print(importances.head(5))
    
    # 7. Sauvegarde
    os.makedirs("src", exist_ok=True)
    joblib.dump(best_model, "src/churn_model.pkl")
    print("\nModèle optimisé sauvegardé dans : src/churn_model.pkl")

if __name__ == "__main__":
    train_churn_model()
