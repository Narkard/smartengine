import pandas as pd
import joblib
import json
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, 
    recall_score, f1_score, roc_auc_score, classification_report
)

# Configuration des chemins (Abstractions relatives)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "processed", "analytics.csv")
MODEL_PATH = os.path.join(BASE_DIR, "outputs", "models", "churn_model.joblib")
METRICS_OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "evaluation_metrics.json")
REPORT_OUTPUT_PATH = os.path.join(BASE_DIR, "outputs", "rapport-modele.md")

def evaluate_model():
    print("--- Évaluation du Modèle ---")
    
    if not os.path.exists(DATA_PATH):
        print(f"Erreur : Le fichier {DATA_PATH} est introuvable.")
        return
    if not os.path.exists(MODEL_PATH):
        print(f"Erreur : Le fichier {MODEL_PATH} est introuvable.")
        return

    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    
    # Identifier la cible et les caractéristiques
    target = 'churn_flag'
    if target not in df.columns:
        print(f"Erreur : La colonne cible '{target}' est absente de analytics.csv")
        return

    # Utiliser les features attendues par le modèle
    X = df.drop(columns=[target], errors='ignore').select_dtypes(include=[np.number])
    X = X.drop(columns=['account_id'], errors='ignore')
    y = df[target]

    # 2. Recalculer le split test identique
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Prédictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    # 3. Calcul des métriques globales
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob) if y_prob is not None else "N/A"

    # 4. Feature Importances
    feature_importances = {}
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feat_names = X.columns
        feat_imp = sorted(zip(feat_names, importances), key=lambda x: x[1], reverse=True)
        for name, val in feat_imp[:10]:
            feature_importances[name] = float(val)

    # 5. Sauvegarde du résumé JSON
    summary = {
        "global_metrics": {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "auc_roc": float(auc) if isinstance(auc, float) else auc
        },
        "feature_importances": feature_importances
    }
    
    with open(METRICS_OUTPUT_PATH, 'w') as f:
        json.dump(summary, f, indent=4)

    # 6. Génération du Rapport Markdown
    report_content = f"""# Rapport de Performance du Modèle - Sprint 3

## Synthèse des Performances
- **Précision** : {prec:.4f}
- **Rappel (Recall)** : {rec:.4f}
- **F1-Score (Cible Churn)** : {f1:.4f}
- **AUC-ROC** : {auc if isinstance(auc, str) else f"{auc:.4f}"}

## Matrice de Confusion
```
{cm}
```

## Importance des Variables (Top 10)
"""
    for name, val in feature_importances.items():
        report_content += f"- **{name}** : {val:.4f}\n"

    with open(REPORT_OUTPUT_PATH, "w") as f:
        f.write(report_content)
    
    print(f"SUCCÈS : Métriques et rapport générés dans /outputs/")

if __name__ == "__main__":
    evaluate_model()
