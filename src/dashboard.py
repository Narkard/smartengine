import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="smartEngine - Customer Success Dashboard", layout="wide")

# Chemins
DATA_PATH = "outputs/master_dataset.csv"

def load_data():
    if not os.path.exists(DATA_PATH):
        st.error("Dataset introuvable. Exécutez d'abord le pipeline.")
        return None
    return pd.read_csv(DATA_PATH)

st.title("🚀 smartEngine - Pilotage de la Rétention")

data = load_data()

if data is not None:
    # --- FILTRES ---
    st.sidebar.header("Filtres")
    industry_filter = st.sidebar.multiselect("Industrie", options=data['industry'].unique(), default=data['industry'].unique())
    plan_filter = st.sidebar.multiselect("Plan Tier", options=data['plan_tier'].unique(), default=data['plan_tier'].unique())

    filtered_data = data[(data['industry'].isin(industry_filter)) & (data['plan_tier'].isin(plan_filter))]
    
    # --- KPI TOP ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Clients Totaux", len(filtered_data))
    with col2:
        st.metric("MRR Total", f"{filtered_data['mrr_amount'].sum():,.0f} $")
    with col3:
        churn_count = filtered_data['churn_flag'].sum()
        st.metric("Clients Churnés", int(churn_count))
    with col4:
        churn_rate = (filtered_data['churn_flag'].sum() / len(filtered_data)) * 100
        st.metric("Taux de Churn", f"{churn_rate:.1f}%")

    # --- GRAPHIQUES ---
    st.markdown("---")
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Usage vs MRR (par Industrie)")
        fig_scatter = px.scatter(filtered_data, x="usage_count_sum", y="mrr_amount", color="industry", 
                                 size="seats", hover_name="account_id", title="Corrélation Usage/Revenu")
        st.plotly_chart(fig_scatter, use_container_width=True)

    with g2:
        st.subheader("Distribution du Taux de Churn par Industrie")
        churn_by_ind = filtered_data.groupby('industry')['churn_flag'].mean().reset_index()
        fig_bar = px.bar(churn_by_ind, x='industry', y='churn_flag', title="Taux de Churn (%)", color='industry')
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- TABLEAU D'ALERTES ---
    st.markdown("---")
    st.subheader("🚩 Comptes à Surveiller (Baisse de Satisfaction ou Usage Faible)")
    
    # Heuristique simple pour l'alerte
    mean_usage = filtered_data['usage_count_sum'].mean()
    alerts_table = filtered_data[(filtered_data['satisfaction_score'] < 3) | (filtered_data['usage_count_sum'] < mean_usage * 0.5)]
    alerts_table = alerts_table.sort_values(by='mrr_amount', ascending=False)

    st.dataframe(
        alerts_table[['account_id', 'industry', 'plan_tier', 'mrr_amount', 'usage_count_sum', 'satisfaction_score', 'churn_flag']],
        use_container_width=True,
        hide_index=True
    )

    st.info("💡 Les comptes affichés ci-dessus présentent soit un score de satisfaction faible (< 3), soit un usage inférieur à 50% de la moyenne.")
