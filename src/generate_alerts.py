import pandas as pd
import joblib
import os
from datetime import datetime

def generate_risk_alerts():
    print("--- Génération des Alertes de Risque (Sprint 4) ---")
    
    # 1. Chargement
    DATA_PATH = "outputs/master_dataset.csv"
    MODEL_PATH = "src/churn_model.pkl"
    
    if not os.path.exists(DATA_PATH) or not os.path.exists(MODEL_PATH):
        print("Erreur : Dataset ou modèle introuvable.")
        return

    df = pd.read_csv(DATA_PATH)
    model = joblib.load(MODEL_PATH)
    
    # 2. Préparation des features
    features = [
        'seats', 'is_trial', 'usage_count_sum', 'usage_trend', 
        'error_count_sum', 'mrr_amount', 
        'ticket_count', 'resolution_time_hours', 'satisfaction_score', 
        'escalation_flag'
    ]
    
    # Filtrer uniquement les clients actifs (churn_flag == 0)
    active_clients = df[df['churn_flag'] == 0].copy()
    
    if active_clients.empty:
        print("Aucun client actif à analyser.")
        return

    X = active_clients[features].copy()
    X['is_trial'] = X['is_trial'].astype(int)
    
    # 3. Prédiction de probabilité
    # On utilise predict_proba pour avoir un score fin
    probs = model.predict_proba(X)[:, 1]
    active_clients['churn_probability'] = probs
    
    # 4. Identification des comptes à haut risque
    # Seuil arbitraire de 0.6 pour l'alerte
    high_risk_threshold = 0.6
    alerts = active_clients[active_clients['churn_probability'] >= high_risk_threshold].sort_values(by='churn_probability', ascending=False)
    
    # 5. Rapport
    os.makedirs("outputs", exist_ok=True)
    report_path = f"outputs/alerts_{datetime.now().strftime('%Y%m%d')}.txt"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"RAPPORT D'ALERTES CHURN - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
        f.write("="*50 + "\n")
        f.write(f"Seuil de risque : {high_risk_threshold}\n")
        f.write(f"Nombre de comptes à risque identifiés : {len(alerts)}\n\n")
        
        for _, row in alerts.iterrows():
            f.write(f"- Compte : {row['account_id']} | Industrie : {row['industry']}\n")
            f.write(f"  Probabilité : {row['churn_probability']:.2%}\n")
            f.write(f"  MRR exposé : {row['mrr_amount']}$\n")
            f.write(f"  Tendance usage : {row['usage_trend']:.2f}\n")
            f.write("-" * 30 + "\n")
            
    print(f"Alertes générées : {len(alerts)} comptes à risque.")
    print(f"Rapport sauvegardé dans : {report_path}")

if __name__ == "__main__":
    generate_risk_alerts()
