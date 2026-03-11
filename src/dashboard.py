import streamlit as st
import pandas as pd
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="smartEngine - RavenStack Dashboard", layout="wide")

# Chemins
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "churn_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "..", "outputs", "master_dataset.csv")

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

def load_model():
    return joblib.load(MODEL_PATH)

# Titre
st.title("🛡️ smartEngine Dashboard")
st.markdown("Système de prédiction de churn pour les équipes **Customer Success** de RavenStack.")

# Chargement
try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.stop()

# Sidebar - Filtres
st.sidebar.header("Filtres")
industry_filter = st.sidebar.multiselect("Industrie", options=df['industry'].unique(), default=df['industry'].unique())
plan_filter = st.sidebar.multiselect("Plan", options=df['plan_tier'].unique(), default=df['plan_tier'].unique())

df_filtered = df[(df['industry'].isin(industry_filter)) & (df['plan_tier'].isin(plan_filter))]

# Scoring
drop_cols = ['account_id', 'account_name', 'signup_date', 'subscription_id', 'country', 'referral_source', 'target_churn']
X_predict = df_filtered.drop(columns=[col for col in drop_cols if col in df_filtered.columns], errors='ignore')

# Probabilités
probs = model.predict_proba(X_predict)[:, 1]
df_filtered['churn_risk_score'] = (probs * 100).round(1)

# --- KPIs ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Comptes analysés", len(df_filtered))
with col2:
    high_risk_count = len(df_filtered[df_filtered['churn_risk_score'] > 50])
    st.metric("Alertes (Risque > 50%)", high_risk_count, delta_color="inverse")
with col3:
    avg_risk = df_filtered['churn_risk_score'].mean().round(1)
    st.metric("Risque Moyen", f"{avg_risk}%")

# --- Liste des comptes à risque ---
st.subheader("⚠️ Liste de priorité des comptes à risque")
high_risk_df = df_filtered[df_filtered['churn_risk_score'] > 30].sort_values(by='churn_risk_score', ascending=False)
st.dataframe(high_risk_df[['account_id', 'account_name', 'industry', 'churn_risk_score', 'mrr_amount', 'ticket_count']], use_container_width=True)

# --- Graphiques ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Analyse du Risque par Industrie")
    fig, ax = plt.subplots()
    sns.barplot(data=df_filtered, x='industry', y='churn_risk_score', ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col_right:
    st.subheader("Lien Usage vs Risque")
    fig, ax = plt.subplots()
    sns.scatterplot(data=df_filtered, x='total_usage', y='churn_risk_score', hue='plan_tier', ax=ax)
    st.pyplot(fig)

# --- Recommandations ---
st.subheader("💡 Recommandations Stratégiques")
st.info("""
1.  **Industrie DevTools** : Vigilance renforcée. C'est le secteur avec le risque le plus élevé. Planifier un 'Business Review' trimestriel.
2.  **Support réactif** : Les comptes ayant plus de 5 tickets support sans score de satisfaction (`satisfaction_score`) renseigné doivent être contactés par un CSM.
3.  **Engagement** : Proposer une formation gratuite aux comptes dont le `usage_trend` est inférieur à 0.1 sur les 30 derniers jours.
""")
