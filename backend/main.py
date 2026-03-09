from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
import os

app = FastAPI(
    title="smartEngine API",
    description="API de prédiction de churn B2B",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement du modèle de Machine Learning au démarrage
MODEL_PATH = "churn_model.pkl"
DATA_PATH = "../outputs/master_dataset.csv"

model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

@app.get("/api/health")
def health_check():
    return {
        "status": "ok", 
        "message": "smartEngine API is running",
        "model_loaded": model is not None
    }

@app.get("/api/accounts/risk")
def get_at_risk_accounts():
    """
    Simule une requête sur la base des clients actuels 
    et retourne les comptes avec une probabilité de churn > 50%
    """
    if not os.path.exists(DATA_PATH) or model is None:
        raise HTTPException(status_code=503, detail="Modèle non entrainé ou dataset manquant.")
        
    df = pd.read_csv(DATA_PATH)
    
    # Exclure ceux qui ont DÉJÀ churn, on cherche la prédiction sur les actifs
    df_active = df[df['target_churn'] == 0].copy()
    
    # On simule la donnée du jour en récupérant les info brutes
    drop_cols = ['account_id', 'account_name', 'signup_date', 'target_churn']
    X_predict = df_active.drop(columns=[col for col in drop_cols if col in df_active.columns], errors='ignore')
    
    # On sort les probabilités de la classe 1 (Churn)
    churn_probabilities = model.predict_proba(X_predict)[:, 1]
    
    df_active['churn_probability'] = churn_probabilities
    
    # Filtre sur "À risque" (seuil à 30% pour correspondre aux alertes critiques)
    at_risk = df_active[df_active['churn_probability'] > 0.3].sort_values(by='churn_probability', ascending=False)
    
    # Formattage de la réponse avec explicabilité simple
    results = []
    for _, row in at_risk.iterrows():
        # Détection "naïve" des signaux basés sur les seuils
        signals = []
        if row.get('ticket_count', 0) > 3: signals.append("Tickets support élevés")
        if row.get('error_count', 0) > 10: signals.append("Erreurs techniques fréquentes")
        if row.get('usage_count', 0) < 50: signals.append("Faible utilisation plateforme")
        
        results.append({
            "account_id": str(row['account_id']),
            "account_name": row.get('account_name', f"Compte {row['account_id'][:8]}"),
            "mrr": float(row.get('mrr_amount', 0)),
            "tickets": int(row.get('ticket_count', 0)),
            "churn_risk_percent": round(row['churn_probability'] * 100, 1),
            "signals": signals if signals else ["Signal faible global"]
        })
        
    return {"at_risk_accounts": results, "total_scanned": len(df_active)}

@app.get("/api/stats/overview")
def get_dashboard_stats():
    """
    Renvoie les KPI globaux pour le haut du dashboard.
    """
    if not os.path.exists(DATA_PATH):
         return {"error": "Dataset non généré."}
         
    df = pd.read_csv(DATA_PATH)
    total_mrr = df[df['target_churn'] == 0]['mrr_amount'].sum()
    total_churned = df[df['target_churn'] == 1]['account_id'].count()
    
    return {
        "total_active_accounts": len(df[df['target_churn'] == 0]),
        "active_mrr": float(total_mrr),
        "total_churned": int(total_churned)
    }

