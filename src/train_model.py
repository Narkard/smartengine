import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.ensemble import GradientBoostingClassifier

DATA_PATH = "../outputs/master_dataset.csv"
MODEL_PATH = "churn_model.pkl"

def train_gbm_model():
    print("--- SPRINT 3 : ENTRAINEMENT GRADIENT BOOSTING ---")
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("master_dataset.csv introuvable.")
    
    df = pd.read_csv(DATA_PATH)
    
    # Nettoyage
    drop_cols = ['account_id', 'account_name', 'signup_date', 'subscription_id', 'country', 'referral_source']
    X = df.drop(columns=[col for col in drop_cols if col in df.columns], errors='ignore')
    
    y = X['target_churn'].astype(int)
    X = X.drop('target_churn', axis=1)
    
    # Preprocessing
    categorical_features = X.select_dtypes(include=['object', 'bool']).columns.tolist()
    numeric_features = X.select_dtypes(exclude=['object', 'bool']).columns.tolist()
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Gradient Boosting (on peut ajuster sample_weight manuellement si besoin)
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # On peut donner plus de poids à la classe 1 pendant le fit
    # Mais le GBM de sklearn n'a pas class_weight. On utilise sample_weight.
    weights = np.where(y_train == 1, 10, 1) # Poids 10 pour le churn
    
    print("Entraînement du modèle GBM avec sample weights...")
    model.fit(X_train, y_train, classifier__sample_weight=weights)
    
    # Evaluation
    y_pred = model.predict(X_test)
    print(f"Accuracy : {accuracy_score(y_test, y_pred):.2%}")
    print("\nMatrice de confusion :")
    print(confusion_matrix(y_test, y_pred))
    print("\nRapport de classification :")
    print(classification_report(y_test, y_pred))
    
    # Sauvegarde
    joblib.dump(model, MODEL_PATH)
    print(f"\nModèle GBM enregistré : {MODEL_PATH}")

if __name__ == "__main__":
    train_gbm_model()
