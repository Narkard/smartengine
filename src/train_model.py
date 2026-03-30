import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = "../outputs/master_dataset.csv"
MODEL_PATH = "churn_model.pkl"

def train_model():
    print("--- ENTRAINEMENT DU MODELE DE CHURN ---")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("master_dataset.csv introuvable. Exécutez data_pipeline.py d'abord.")
    
    df = pd.read_csv(DATA_PATH)
    
    # Feature engineering basique (Nettoyage de valeurs non utiles à l'apprentissage brut)
    # Ex: account_id n'a pas de pouvoir prédictif
    drop_cols = ['account_id', 'account_name', 'signup_date']
    df_clean = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')
    
    # Séparation Target et Features
    if 'target_churn' not in df_clean.columns:
        # Fallback pour sécuriser la présence du label
        raise ValueError("Colonne cible 'target_churn' absente.")
    
    X = df_clean.drop('target_churn', axis=1)
    y = df_clean['target_churn'].astype(int)  # 0 or 1
    
    # Identification des types de colonnes
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    numeric_features = X.select_dtypes(exclude=['object', 'bool']).columns.tolist()
    
    # Préparation du Pipeline (Preprocessing + Model)
    numeric_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
        
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Entraînement
    model.fit(X_train, y_train)
    
    # Prédictions et Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    
    print(f"Accuracy sur Test Set : {acc:.2%}")
    print("\nRapport de classification:\n", classification_report(y_test, y_pred))
    
    # Sauvegarde du modèle complet (inclus le preprocessor)
    joblib.dump(model, MODEL_PATH)
    print(f"\nModèle enregistré sous : {MODEL_PATH}")

if __name__ == "__main__":
    train_model()
