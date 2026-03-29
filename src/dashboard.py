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
        # Alerte si trend < 0.8 (baisse de 20%)
        high_risk = len(filtered_data[(filtered_data['usage_trend'] < 0.8) & (filtered_data['churn_flag'] == 0)])
        st.metric("Comptes à Risque", high_risk)
    with col4:
        churn_rate = (filtered_data['churn_flag'].sum() / len(filtered_data)) * 100
        st.metric("Taux de Churn", f"{churn_rate:.1f}%")

    # --- GRAPHIQUES ---
    st.markdown("---")
    g1, g2 = st.columns(2)

    with g1:
        st.subheader("Distribution de la Tendance d'Usage")
        fig_trend = px.histogram(filtered_data, x="usage_trend", color="churn_flag", 
                                 title="Score de Tendance (1.0 = Stable)",
                                 labels={'usage_trend': 'Usage Trend', 'churn_flag': 'Churn'})
        fig_trend.add_vline(x=0.8, line_dash="dash", line_color="red")
        st.plotly_chart(fig_trend, use_container_width=True)

    with g2:
        st.subheader("MRR par Industrie")
        fig_pie = px.pie(filtered_data, values='mrr_amount', names='industry', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TABLEAU D'ALERTES ---
    st.markdown("---")
    st.subheader("🚩 Liste des Comptes Prioritaires (Faible Usage)")
    
    alerts_table = filtered_data[(filtered_data['usage_trend'] < 0.8) & (filtered_data['churn_flag'] == 0)]
    alerts_table = alerts_table.sort_values(by='usage_trend')

    st.dataframe(
        alerts_table[['account_id', 'industry', 'plan_tier', 'mrr_amount', 'usage_trend', 'satisfaction_score']],
        column_config={
            "usage_trend": st.column_config.ProgressColumn("Tendance Usage", min_value=0, max_value=1.5, format="%.2f"),
        },
        use_container_width=True,
        hide_index=True
    )

    st.info("💡 Les comptes affichés ci-dessus présentent soit un score de satisfaction faible (< 3), soit un usage inférieur à 50% de la moyenne.")
