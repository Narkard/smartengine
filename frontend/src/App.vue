<script setup>
import { ref, onMounted, computed } from 'vue'

const apiUrl = 'http://localhost:8000/api'
const backendStatus = ref('Vérification...')
const isBackendOnline = ref(false)

const stats = ref({
  total_active_accounts: 0,
  active_mrr: 0,
  total_churned: 0
})

const atRiskAccounts = ref([])
const isLoading = ref(true)

const fetchDashboardData = async () => {
  isLoading.value = true
  try {
    // 1. Check Santé de l'API
    const healthRes = await fetch(`${apiUrl}/health`)
    if (healthRes.ok) {
      backendStatus.value = 'En ligne'
      isBackendOnline.value = true
    }

    // 2. Fetch Statistiques
    const statsRes = await fetch(`${apiUrl}/stats/overview`)
    if (statsRes.ok) {
      stats.value = await statsRes.json()
    }

    // 3. Fetch Comptes à risque
    const riskRes = await fetch(`${apiUrl}/accounts/risk`)
    if (riskRes.ok) {
      const riskData = await riskRes.json()
      atRiskAccounts.value = riskData.at_risk_accounts
    }
  } catch (error) {
    backendStatus.value = 'Hors ligne'
    isBackendOnline.value = false
    console.error("Erreur connexion API Backend:", error)
  } finally {
    isLoading.value = false
  }
}

const formatCurrency = (value) => {
  return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(value)
}

const getRiskColor = (percent) => {
  if (percent > 70) return '#f85149' // Rouge vif pour risques imminents
  if (percent > 40) return '#d29922' // Orange/Jaune pour risque modéré
  return '#3fb950' // Vert pour risque faible/sous contrôle
}

onMounted(() => {
  fetchDashboardData()
})
</script>

<template>
  <div class="dashboard-wrap">
    <!-- Header -->
    <header class="topbar">
      <div class="logo">
        <span class="gradient-text">smartEngine</span>
        <span class="badge">Customer Success Dashboard</span>
      </div>
      <div class="status-badge" :class="{ 'online': isBackendOnline, 'offline': !isBackendOnline }">
        <span class="indicator"></span> API: {{ backendStatus }}
      </div>
    </header>

    <main class="dashboard-content" v-if="!isLoading">
      
      <!-- KPI Cards -->
      <section class="kpi-grid">
        <div class="kpi-card">
          <h4>Comptes Actifs</h4>
          <p class="kpi-value">{{ stats.total_active_accounts }}</p>
        </div>
        <div class="kpi-card">
          <h4>MRR Actif (Prevision)</h4>
          <p class="kpi-value highlight">{{ formatCurrency(stats.active_mrr) }}</p>
        </div>
        <div class="kpi-card">
          <h4>Résiliations constatées</h4>
          <p class="kpi-value danger">{{ stats.total_churned }}</p>
        </div>
      </section>

      <!-- Alertes Risques Churn -->
      <section class="risk-section">
        <div class="section-header">
          <h2>🚨 Comptes à risque élevé</h2>
          <span class="count-badge">{{ atRiskAccounts.length }} comptes identifiés par l'IA</span>
        </div>
        
        <div class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>ID Compte</th>
                <th>Nom du Compte</th>
                <th>MRR Menacé</th>
                <th>Tickets Support</th>
                <th>Probabilité de Churn</th>
                <th>Action Recommandée</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="acc in atRiskAccounts" :key="acc.account_id">
                <td class="dimmed">{{ acc.account_id.substring(0,8) }}</td>
                <td class="fw-bold">{{ acc.account_name }}</td>
                <td>{{ formatCurrency(acc.mrr) }}</td>
                <td>
                  <span class="small-badge" :class="{'bad': acc.tickets > 5}">{{ acc.tickets }} alertes</span>
                </td>
                <td>
                  <div class="risk-bar-container">
                    <div class="risk-bar" :style="{ width: acc.churn_risk_percent + '%', backgroundColor: getRiskColor(acc.churn_risk_percent) }"></div>
                  </div>
                  <span class="risk-pct" :style="{ color: getRiskColor(acc.churn_risk_percent) }">{{ acc.churn_risk_percent }}%</span>
                </td>
                <td>
                  <button class="action-btn">Contacter</button>
                </td>
              </tr>
              <tr v-if="atRiskAccounts.length === 0">
                <td colspan="6" class="text-center dimmed py-4">Aucun compte à risque détecté.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <div v-else class="loader-container">
      <div class="spinner"></div>
      <p>Analyse de la base de données par l'IA en cours...</p>
    </div>
  </div>
</template>

<style scoped>
.dashboard-wrap {
  min-height: 100vh;
  background-color: #0d1117;
  color: #c9d1d9;
  font-family: 'Inter', -apple-system, sans-serif;
  display: flex;
  flex-direction: column;
  width: 100%;
}

/* Header */
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #161b22;
  border-bottom: 1px solid #30363d;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.gradient-text {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.badge {
  background: rgba(88, 166, 255, 0.1);
  color: #58a6ff;
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 12px;
  border: 1px solid rgba(88, 166, 255, 0.2);
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.85rem;
}
.indicator { width: 8px; height: 8px; border-radius: 50%; }
.online { color: #3fb950; }
.online .indicator { background: #3fb950; box-shadow: 0 0 8px rgba(63, 185, 80, 0.8); }
.offline { color: #f85149; }
.offline .indicator { background: #f85149; }

/* Grid & Layout */
.dashboard-content {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  box-sizing: border-box;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.kpi-card {
  background: #1c2128;
  border: 1px solid #30363d;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: left;
}

.kpi-card h4 {
  color: #8b949e;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.5rem 0;
}

.kpi-value {
  font-size: 2.5rem;
  font-weight: 700;
  color: #c9d1d9;
  margin: 0;
}
.kpi-value.highlight { color: #58a6ff; }
.kpi-value.danger { color: #f85149; }

/* Table Section */
.section-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-header h2 { margin: 0; font-size: 1.5rem; color: #fff; }
.count-badge {
  background: rgba(248, 81, 73, 0.15);
  color: #f85149;
  padding: 4px 10px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.85rem;
}

.table-container {
  overflow-x: auto;
  background: #1c2128;
  border: 1px solid #30363d;
  border-radius: 10px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.data-table th, .data-table td {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #30363d;
}

.data-table th {
  background: #161b22;
  color: #8b949e;
  font-weight: 600;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.data-table tbody tr:hover { background: rgba(240, 246, 252, 0.04); }
.data-table tbody tr:last-child td { border-bottom: none; }

.fw-bold { font-weight: 600; color: #fff; }
.dimmed { color: #8b949e; }
.text-center { text-align: center; }
.py-4 { padding-top: 2rem; padding-bottom: 2rem; }

.small-badge {
  background: rgba(139, 148, 158, 0.15);
  color: #8b949e;
  padding: 3px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
}
.small-badge.bad {
  background: rgba(210, 153, 34, 0.15);
  color: #d29922;
}

/* Risk Bar */
.risk-bar-container {
  width: 100px;
  height: 6px;
  background: #30363d;
  border-radius: 4px;
  display: inline-block;
  margin-right: 10px;
  overflow: hidden;
  vertical-align: middle;
}
.risk-bar {
  height: 100%;
  border-radius: 4px;
}
.risk-pct {
  font-weight: 600;
  font-size: 0.9rem;
  vertical-align: middle;
}

/* Buttons */
.action-btn {
  background-color: transparent;
  color: #58a6ff;
  border: 1px solid rgba(88, 166, 255, 0.4);
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.85rem;
  transition: all 0.2s;
}
.action-btn:hover {
  background: rgba(88, 166, 255, 0.1);
  border-color: #58a6ff;
}

/* Loader */
.loader-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  flex: 1;
  color: #8b949e;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(88, 166, 255, 0.1);
  border-left-color: #58a6ff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin { 100% { transform: rotate(360deg); } }
</style>

