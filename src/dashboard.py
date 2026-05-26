import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import shap
import matplotlib.pyplot as plt
import os

# --- Configuration de la page ---
st.set_page_config(page_title="RavenStack - Churn Dashboard", layout="wide")

# --- Chargement des données ---
@st.cache_data
def load_data():
    # Définition des chemins relatifs
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prio_path = os.path.join(base_dir, 'outputs', 'priorisation.csv')
    analytics_path = os.path.join(base_dir, 'data', 'processed', 'analytics.csv')
    model_path = os.path.join(base_dir, 'outputs', 'models', 'churn_model.joblib')
    features_path = os.path.join(base_dir, 'outputs', 'models', 'model_features.joblib')
    
    # Chargement
    prio_df = pd.read_csv(prio_path)
    analytics_df = pd.read_csv(analytics_path)
    
    # Fusionner pour avoir le profil complet dans le dashboard
    df = pd.merge(prio_df, analytics_df.drop(columns=['MRR', 'churn_flag', 'churn_score', 'risk_level'], errors='ignore'), on='account_id', how='left')
    
    # Reconstruire la colonne 'plan' à partir des colonnes One-Hot
    df['plan'] = 'Basic'
    if 'plan_Pro' in df.columns:
        df.loc[df['plan_Pro'] == True, 'plan'] = 'Pro'
    if 'plan_Enterprise' in df.columns:
        df.loc[df['plan_Enterprise'] == True, 'plan'] = 'Enterprise'
        
    model = joblib.load(model_path)
    features = joblib.load(features_path)
    
    return df, model, features

try:
    df, model, features = load_data()
except Exception as e:
    st.error(f"Erreur lors du chargement des données. Veuillez vérifier que l'étape 4 a bien été exécutée. Détail : {e}")
    st.stop()

# --- Palette daltonisme-friendly (Orange / Bleu) ---
COLOR_MAP = {
    'Q1 - Priorité maximale': '#d95f02', # Orange fort
    'Q2 - Action automatisée': '#fc8d62', # Orange clair
    'Q3 - Surveillance': '#7570b3', # Bleu/Violet
    'Q4 - Aucune action': '#1f78b4'  # Bleu clair
}

st.title("🛡️ Dashboard de Pilotage de la Rétention - RavenStack")

# --- Navigation par onglets ---
tab1, tab2, tab3 = st.tabs(["📊 Vue 1 : Portefeuille", "🎯 Vue 2 : Priorisation", "🔍 Vue 3 : Fiche compte"])

# ==========================================
# VUE 1 : PORTEFEUILLE
# ==========================================
with tab1:
    st.header("Vue d'ensemble du Portefeuille")
    
    # KPIs
    col1, col2, col3 = st.columns(3)
    
    nb_comptes = len(df)
    taux_churn = (len(df[df['risk_level'] == 'High']) / nb_comptes) * 100
    mrr_risque = df[df['risk_level'] == 'High']['MRR'].sum()
    
    col1.metric("Total des comptes", f"{nb_comptes}")
    col2.metric("Comptes à risque élevé (%)", f"{taux_churn:.1f} %")
    col3.metric("MRR total à risque", f"${mrr_risque:,.2f}")
    
    st.divider()
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.subheader("Distribution des scores de churn")
        fig_hist = px.histogram(
            df, x="churn_score", nbins=20, 
            color_discrete_sequence=['#1f78b4'],
            labels={"churn_score": "Score de Churn", "count": "Nombre de comptes"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col_plot2:
        st.subheader("Répartition par quadrant d'action")
        fig_pie = px.pie(
            df, names="quadrant", 
            color="quadrant", color_discrete_map=COLOR_MAP,
            hole=0.4
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

# ==========================================
# VUE 2 : PRIORISATION
# ==========================================
with tab2:
    st.header("Matrice de Priorisation")
    
    # Filtres
    st.sidebar.header("Filtres de Priorisation")
    quadrants_selected = st.sidebar.multiselect("Filtrer par Quadrant", options=df['quadrant'].unique(), default=df['quadrant'].unique())
    plans_selected = st.sidebar.multiselect("Filtrer par Plan", options=df['plan'].unique(), default=df['plan'].unique())
    score_min, score_max = st.sidebar.slider("Score de churn", 0.0, 1.0, (0.0, 1.0))
    mrr_min, mrr_max = st.sidebar.slider("MRR ($)", float(df['MRR'].min()), float(df['MRR'].max()), (float(df['MRR'].min()), float(df['MRR'].max())))
    
    # Application des filtres
    mask = (
        (df['quadrant'].isin(quadrants_selected)) &
        (df['plan'].isin(plans_selected)) &
        (df['churn_score'] >= score_min) & (df['churn_score'] <= score_max) &
        (df['MRR'] >= mrr_min) & (df['MRR'] <= mrr_max)
    )
    filtered_df = df[mask]
    
    # Scatter Plot
    fig_scatter = px.scatter(
        filtered_df, x="churn_score", y="MRR", color="quadrant",
        hover_data=['account_id', 'action_recommandee'],
        color_discrete_map=COLOR_MAP,
        labels={"churn_score": "Score de Churn", "MRR": "Revenu Mensuel (MRR)"},
        title="Cartographie des Comptes (Risque vs Valeur)"
    )
    # Ajouter des lignes pour marquer les seuils (ex: 0.5 pour le score)
    fig_scatter.add_vline(x=0.5, line_dash="dash", line_color="gray")
    median_mrr = df['MRR'].median()
    fig_scatter.add_hline(y=median_mrr, line_dash="dash", line_color="gray", annotation_text="Médiane MRR")
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tableau
    st.subheader(f"Liste des comptes ({len(filtered_df)} trouvés)")
    cols_to_show = ['account_id', 'churn_score', 'risk_level', 'MRR', 'plan', 'quadrant', 'action_recommandee']
    st.dataframe(filtered_df[cols_to_show], use_container_width=True)

# ==========================================
# VUE 3 : FICHE COMPTE & SHAP
# ==========================================
with tab3:
    st.header("Analyse Détaillée d'un Compte")
    
    # Sélection du compte
    account_list = df.sort_values(by="churn_score", ascending=False)['account_id'].tolist()
    selected_account = st.selectbox("Rechercher un compte (Triés par risque décroissant) :", account_list)
    
    if selected_account:
        acc_data = df[df['account_id'] == selected_account].iloc[0]
        
        col_profil, col_score = st.columns([1, 1])
        
        with col_profil:
            st.subheader("Profil du Compte")
            st.write(f"**Identifiant :** {acc_data['account_id']}")
            st.write(f"**Plan :** {acc_data['plan']}")
            st.write(f"**MRR :** ${acc_data['MRR']:.2f}")
            st.write(f"**Ancienneté :** {acc_data.get('seniority_months', 'N/A')} mois")
            st.write(f"**Usage (Tendance 30j) :** {acc_data.get('usage_trend_30d', 'N/A')}")
            st.write(f"**Usage (Dernier usage) :** il y a {acc_data.get('days_since_last_usage', 'N/A')} jours")
            st.write(f"**Tickets ouverts :** {acc_data.get('total_tickets', 'N/A')}")
            
            # Affichage mis en évidence de l'action
            st.info(f"**Quadrant :** {acc_data['quadrant']}")
            st.warning(f"💡 **Action Recommandée :** {acc_data['action_recommandee']}")
            
        with col_score:
            st.subheader("Niveau d'Alerte")
            # Jauge non technique
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = acc_data['churn_score'] * 100,
                title = {'text': "Probabilité de départ (%)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': COLOR_MAP.get(acc_data['quadrant'], "gray")},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 100], 'color': "gainsboro"}
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)
            
        st.divider()
        
        # Explicabilité avec SHAP
        st.subheader("Pourquoi ce score ? (Facteurs d'influence)")
        
        with st.spinner("Analyse des facteurs en cours..."):
            try:
                # Préparer les données pour SHAP
                X_acc = pd.DataFrame([acc_data[features]])
                
                # Créer l'explainer
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_acc)
                
                # Extraction des valeurs SHAP de manière robuste (List, Explanation ou Array)
                if hasattr(shap_values, "values"): # Nouvelles versions de SHAP (Explanation object)
                    shap_vals = shap_values.values[0]
                elif isinstance(shap_values, list): # Anciennes versions, modèle comme RandomForest
                    shap_vals = shap_values[1][0]
                else: # Modèles comme XGBoost
                    shap_vals = shap_values[0]
                
                # Si multiclasse (ex: 2D array de forme (n_features, 2))
                if len(shap_vals.shape) > 1:
                    shap_vals = shap_vals[:, 1]
                
                # S'assurer que le tableau est strictement 1D
                shap_vals = np.ravel(np.array(shap_vals))
                
                # Extraire les 5 facteurs les plus impactants
                shap_df = pd.DataFrame({
                    'Facteur': features,
                    'Impact': shap_vals
                })
                
                # Valeur absolue pour trouver les plus importants, puis on garde le signe pour l'affichage
                shap_df['Impact_Abs'] = shap_df['Impact'].abs()
                top_5 = shap_df.sort_values(by='Impact_Abs', ascending=False).head(5)
                top_5 = top_5.sort_values(by='Impact', ascending=True) # Pour avoir les négatifs en bas, positifs en haut
                
                # Graphique en barres horizontal
                fig_shap, ax = plt.subplots(figsize=(8, 4))
                
                # Couleurs : Orange si ça augmente le risque, Bleu si ça le diminue
                colors = ['#d95f02' if x > 0 else '#1f78b4' for x in top_5['Impact']]
                
                ax.barh(top_5['Facteur'], top_5['Impact'], color=colors)
                ax.set_xlabel("Impact sur le score (Orange = Augmente le risque, Bleu = Diminue)")
                ax.set_title("Top 5 des facteurs d'influence pour ce compte")
                
                # Retirer les bordures pour un style plus épuré
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                st.pyplot(fig_shap)
                
            except Exception as e:
                st.error(f"Impossible de générer l'analyse des facteurs d'influence. Détail technique : {e}")
