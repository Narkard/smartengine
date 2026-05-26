import pandas as pd
import os

def main():
    # Chemins des fichiers
    scores_path = 'outputs/scores.csv'
    analytics_path = 'data/processed/analytics.csv'
    output_path = 'outputs/priorisation.csv'

    print("Chargement des données...")
    
    # 1. Charge outputs/scores.csv
    df_scores = pd.read_csv(scores_path)
    
    # 2. Charge data/processed/analytics.csv et extrait le MRR
    # La colonne pour le MRR s'appelle 'mrr_amount' dans analytics.csv
    df_analytics = pd.read_csv(analytics_path, usecols=['account_id', 'mrr_amount'])
    df_analytics.rename(columns={'mrr_amount': 'MRR'}, inplace=True)
    
    # 3. Fusionne les deux tables sur account_id
    df_merged = pd.merge(df_scores, df_analytics, on='account_id', how='left')
    
    # 4. Calcule la médiane du MRR et crée la colonne value_level
    mrr_median = df_merged['MRR'].median()
    df_merged['value_level'] = df_merged['MRR'].apply(lambda x: 'high' if x >= mrr_median else 'low')
    
    # 5. Affecte un quadrant
    def get_quadrant(row):
        is_high_risk = row['risk_level'] == 'High'
        is_high_value = row['value_level'] == 'high'
        
        if is_high_risk and is_high_value:
            return 'Q1 - Priorité maximale'
        elif is_high_risk and not is_high_value:
            return 'Q2 - Action automatisée'
        elif not is_high_risk and is_high_value:
            return 'Q3 - Surveillance'
        else:
            return 'Q4 - Aucune action'
            
    df_merged['quadrant'] = df_merged.apply(get_quadrant, axis=1)
    
    # 6. Ajoute la colonne action_recommandee
    action_map = {
        'Q1 - Priorité maximale': 'Appel CSM direct sous 24h',
        'Q2 - Action automatisée': 'Email automatisé de relance',
        'Q3 - Surveillance': 'Fidélisation douce, surveillance',
        'Q4 - Aucune action': 'Aucune action prioritaire'
    }
    df_merged['action_recommandee'] = df_merged['quadrant'].map(action_map)
    
    # 7. Exporte outputs/priorisation.csv
    columns_to_export = ['account_id', 'churn_score', 'risk_level', 'MRR', 'value_level', 'quadrant', 'action_recommandee']
    df_export = df_merged[columns_to_export]
    
    # S'assure que le dossier de sortie existe
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_export.to_csv(output_path, index=False)
    
    # 8. Affiche un résumé
    print("\n--- Résumé de la priorisation ---")
    print(f"Médiane MRR utilisée : {mrr_median:.2f}")
    print("\nNombre de comptes par quadrant :")
    print(df_export['quadrant'].value_counts().to_string())
    print("\nExport terminé avec succès :", output_path)

if __name__ == "__main__":
    main()
