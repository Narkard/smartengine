import pandas as pd
import joblib
import os
from datetime import datetime

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "src", "churn_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "outputs", "master_dataset.csv")
OUTPUT_REPORT = os.path.join(BASE_DIR, "outputs", "alerts_report.txt")

def generate_alerts():
    print("--- 🔔 Sprint 4 : Génération des Alertes de Churn ---")
    
    if not os.path.exists(MODEL_PATH) or not os.path.exists(DATA_PATH):
        print(f"❌ Erreur : Modèle ou dataset manquant.\nModèle: {MODEL_PATH}\nDataset: {DATA_PATH}")
        return

    # 1. Chargement
    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATA_PATH)
    
    # 2. Filtrer les clients qui n'ont pas encore churné (actifs)
    # Dans notre dataset, churn_flag est la cible historique. 
    # Pour simuler des alertes, on prédit sur tout le monde ou on imagine que ce sont des données fraîches.
    df_active = df[df['churn_flag'] == False].copy()
    
    if len(df_active) == 0:
        print("⚠️ Aucun client actif trouvé pour la prédiction.")
        return

    # 3. Préparation des données pour le modèle
    exclude = ['account_id', 'account_name', 'signup_date', 'country', 'referral_source', 'churn_flag']
    X_predict = df_active.drop(columns=[c for c in exclude if c in df_active.columns])
    
    # 4. Prédiction des probabilités
    # GradientBoosting a une méthode predict_proba
    probs = model.predict_proba(X_predict)[:, 1]
    df_active['churn_probability'] = probs
    
    # 5. Définition du seuil d'alerte (ex: 15% car le modèle est conservateur)
    threshold = 0.15
    high_risk = df_active[df_active['churn_probability'] >= threshold].sort_values(by='churn_probability', ascending=False)
    
    # 6. Génération du rapport textuel
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = [
        "===================================================",
        f"🚨 RAPPORT D'ALERTES SMARTENGINE - {timestamp}",
        "===================================================",
        f"Nombre de clients analysés : {len(df_active)}",
        f"Nombre d'alertes générées (Seuil > {threshold*100}%) : {len(high_risk)}",
        "---------------------------------------------------",
        ""
    ]
    
    for _, row in high_risk.iterrows():
        risk_pct = round(row['churn_probability'] * 100, 1)
        line = f"ID: {row['account_id']} | Risque: {risk_pct}% | MRR: {row.get('mrr_amount', 0)}$"
        report_lines.append(line)
        
        # Diagnostics simples basés sur les features importantes
        if row.get('error_count_mean', 0) > df['error_count_mean'].mean():
            report_lines.append(f"  -> SIGNAL: Taux d'erreurs élevé ({round(row['error_count_mean'], 2)})")
        if row.get('ticket_count', 0) > 2:
            report_lines.append(f"  -> SIGNAL: Volume de tickets important ({int(row['ticket_count'])})")
        report_lines.append("")
            
    report_lines.append("\n===================================================")
    
    os.makedirs(os.path.dirname(OUTPUT_REPORT), exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
        
    print(f"✅ Rapport d'alertes généré : {OUTPUT_REPORT}")
    print(f"📈 Top risque : {high_risk['account_id'].iloc[0]} avec {round(high_risk['churn_probability'].iloc[0]*100, 1)}%")

if __name__ == "__main__":
    generate_alerts()
