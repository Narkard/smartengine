import pandas as pd
import joblib
import json
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, 
    recall_score, f1_score, roc_auc_score, classification_report
)

def evaluate_model():
    # 1. Chargement des fichiers
    data_path = 'data/processed/analytics.csv'
    model_path = 'outputs/models/churn_model.joblib'
    metrics_output_path = 'outputs/evaluation_metrics.json'
    
    if not os.path.exists(data_path):
        print(f"Erreur : Le fichier {data_path} est introuvable.")
        return
    if not os.path.exists(model_path):
        print(f"Erreur : Le fichier {model_path} est introuvable.")
        return

    df = pd.read_csv(data_path)
    model = joblib.load(model_path)
    
    # Identifier la cible et les caractéristiques
    target = 'target_churn'
    if target not in df.columns:
        print(f"Erreur : La colonne cible '{target}' est absente de analytics.csv")
        return

    # Utiliser les features attendues par le modèle
    if hasattr(model, 'feature_names_in_'):
        features = model.feature_names_in_.tolist()
    else:
        # Fallback si feature_names_in_ n'est pas dispo (ex: si ce n'est pas un Pipeline sklearn récent)
        exclude = [target, 'account_id', 'account_name', 'signup_date', 'subscription_id', 'start_date', 'end_date']
        features = [col for col in df.columns if col not in exclude]
    
    X = df[features]
    y = df[target]

    # 2. Recalculer le split test identique
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Prédictions
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None

    # 3. Affichage des métriques globales
    print("=== ÉVALUATION GLOBALE ===")
    cm = confusion_matrix(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, pos_label=True)
    rec = recall_score(y_test, y_pred, pos_label=True)
    f1 = f1_score(y_test, y_pred, pos_label=True)
    auc = roc_auc_score(y_test, y_prob) if y_prob is not None else "N/A"

    print(f"Matrice de Confusion :\n{cm}")
    print(f"Accuracy  : {acc:.4f}")
    print(f"Precision : {prec:.4f} (classe Churn)")
    print(f"Recall    : {rec:.4f} (classe Churn)")
    print(f"F1-score  : {f1:.4f} (classe Churn)")
    print(f"AUC-ROC   : {auc}")
    print("-" * 30)

    # 4. Analyse des biais par sous-groupe
    bias_metrics = {}
    subgroups = ['industry', 'country', 'plan_tier'] # plan_tier utilisé pour 'plan'
    
    print("=== ANALYSE DES BIAIS ===")
    for col in subgroups:
        if col in df.columns:
            print(f"\nBiais par {col} :")
            bias_metrics[col] = {}
            # On utilise l'index de X_test pour filtrer les données originales
            test_indices = X_test.index
            df_test = df.loc[test_indices]
            
            for group_val in df_test[col].unique():
                group_mask = (df_test[col] == group_val)
                y_test_group = y_test[group_mask]
                y_pred_group = y_pred[group_mask]
                
                if len(y_test_group) > 0:
                    # Recall et Precision pour la classe True (churn)
                    # zero_division=0 pour éviter les warnings si un groupe n'a pas de prédictions positives
                    g_rec = recall_score(y_test_group, y_pred_group, pos_label=True, zero_division=0)
                    g_prec = precision_score(y_test_group, y_pred_group, pos_label=True, zero_division=0)
                    
                    bias_metrics[col][str(group_val)] = {
                        "recall": float(g_rec),
                        "precision": float(g_prec),
                        "sample_size": int(len(y_test_group))
                    }
                    print(f"  - {group_val:15} | Recall: {g_rec:.4f} | Precision: {g_prec:.4f} | N: {len(y_test_group)}")
        else:
            print(f"\nColonne '{col}' absente pour l'analyse des biais.")

    # 5. Feature Importances
    feature_importances = {}
    print("\n=== IMPORTANCE DES CARACTÉRISTIQUES ===")
    
    # On cherche l'estimateur final dans le pipeline
    if hasattr(model, 'steps'):
        final_estimator = model.steps[-1][1]
    else:
        final_estimator = model
    
    if hasattr(final_estimator, 'feature_importances_'):
        importances = final_estimator.feature_importances_
        
        # Tentative de récupération des noms de features
        feat_names = features
        # Si le pipeline a un préprocesseur qui change le nombre de colonnes
        if hasattr(model, 'get_feature_names_out'):
            try:
                feat_names = model.get_feature_names_out()
            except:
                pass
        
        if len(importances) == len(feat_names):
            feat_imp = sorted(zip(feat_names, importances), key=lambda x: x[1], reverse=True)
            for name, val in feat_imp[:10]: # Top 10
                feature_importances[name] = float(val)
                print(f"{name:25}: {val:.4f}")
        else:
            print(f"Note: {len(importances)} importances trouvées pour {len(feat_names)} noms de colonnes. Affichage brut sans mapping.")
            for i, val in enumerate(importances[:10]):
                print(f"Feature {i:20}: {val:.4f}")
    else:
        print("Feature importances non disponibles pour ce type de modèle.")

    # 6. Sauvegarde du résumé JSON
    summary = {
        "global_metrics": {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "auc_roc": float(auc) if isinstance(auc, float) else auc
        },
        "bias_analysis": bias_metrics,
        "feature_importances": feature_importances
    }
    
    os.makedirs(os.path.dirname(metrics_output_path), exist_ok=True)
    with open(metrics_output_path, 'w') as f:
        json.dump(summary, f, indent=4)
    
    print(f"\nRésumé des métriques sauvegardé dans {metrics_output_path}")

if __name__ == "__main__":
    evaluate_model()
