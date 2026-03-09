import pandas as pd
import joblib
import os
from datetime import datetime

# Chemins relatifs au script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "churn_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "..", "outputs", "master_dataset.csv")
OUTPUT_REPORT = os.path.join(BASE_DIR, "..", "outputs", "alerts_report.txt")

def generate_alerts():
    print("--- GENERATION DES ALERTES SMARTENGINE ---")
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(DATA_PATH):
        print("Erreur: Modèle ou dataset manquant.")
        return

    # Chargement
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    
    # Filtrer les actifs
    df_active = df[df['target_churn'] == 0].copy()
    
    # Prédiction
    drop_cols = ['account_id', 'account_name', 'signup_date', 'target_churn']
    X_predict = df_active.drop(columns=[col for col in drop_cols if col in df_active.columns], errors='ignore')
    
    probs = model.predict_proba(X_predict)[:, 1]
    df_active['churn_probability'] = probs
    
    # Filtrer les risques élevés (> 30%)
    high_risk = df_active[df_active['churn_probability'] > 0.3].sort_values(by='churn_probability', ascending=False)
    
    # Génération du rapport
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = [
        "===================================================",
        f"RAPPORT D'ALERTES SMARTENGINE - {timestamp}",
        "===================================================",
        f"Nombre de comptes scannés : {len(df_active)}",
        f"Nombre d'alertes générées  : {len(high_risk)}",
        "---------------------------------------------------",
        ""
    ]
    
    for _, row in high_risk.iterrows():
        risk_pct = round(row['churn_probability'] * 100, 1)
        line = f"ID: {row['account_id']} | Nom: {row.get('account_name', 'Inconnu')} | Risque: {risk_pct}% | MRR: {row.get('mrr_amount', 0)}$"
        report_lines.append(line)
        
        # Ajout des signaux spécifiques
        if row.get('ticket_count', 0) > 3:
            report_lines.append(f"  - ALERTE: Support élevé ({int(row['ticket_count'])} tickets)")
        if row.get('error_count', 0) > 10:
            report_lines.append(f"  - ALERTE: Erreurs techniques ({int(row['error_count'])} erreurs)")
            
    report_lines.append("\n===================================================")
    
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"Rapport d'alertes généré : {OUTPUT_REPORT}")

if __name__ == "__main__":
    generate_alerts()
