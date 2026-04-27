import pandas as pd
import numpy as np
import os
import joblib
import json
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "churn_model.joblib")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

def evaluate():
    print("--- Évaluation du Modèle ---")
    
    # 1. Chargement
    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation (même split que l'entraînement)
    target = 'churn_flag'
    X = df.drop(columns=[target], errors='ignore').select_dtypes(include=[np.number])
    X = X.drop(columns=['account_id'], errors='ignore')
    y = df[target]
    
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.20, stratify=y, random_state=42)
    
    # 3. Prédictions
    y_pred = model.predict(X_test)
    
    # 4. Métriques
    metrics = {
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "total_samples": len(y_test)
    }
    
    # Sauvegarde JSON
    with open(os.path.join(OUTPUT_DIR, "evaluation_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=4)
    
    # 5. Rapport Markdown
    report_content = f"""# Rapport de Performance du Modèle - Sprint 3

## Synthèse des Performances
- **Précision** : {metrics['precision']:.4f}
- **Rappel (Recall)** : {metrics['recall']:.4f}
- **F1-Score (Cible Churn)** : {metrics['f1_score']:.4f}

## Matrice de Confusion
```
{confusion_matrix(y_test, y_pred)}
```

## Détails par Classe
```
{classification_report(y_test, y_pred)}
```
"""
    with open(os.path.join(OUTPUT_DIR, "rapport-modele.md"), "w") as f:
        f.write(report_content)
    
    print("SUCCÈS : Métriques et rapport générés dans /outputs/")

if __name__ == "__main__":
    evaluate()
