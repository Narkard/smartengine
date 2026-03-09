<script setup>
import { ref, onMounted } from 'vue'

const apiUrl = 'http://localhost:8000/api/health'
const backendStatus = ref('Vérification...')
const isBackendOnline = ref(false)

onMounted(async () => {
  try {
    const response = await fetch(apiUrl)
    const data = await response.json()
    if (data.status === 'ok') {
      backendStatus.value = 'En ligne'
      isBackendOnline.value = true
    } else {
      backendStatus.value = 'Erreur'
    }
  } catch (error) {
    backendStatus.value = 'Hors ligne'
    isBackendOnline.value = false
  }
})
</script>

<template>
  <div class="landing-container">
    <header class="hero">
      <div class="hero-content">
        <h1 class="gradient-text">smartEngine</h1>
        <p class="subtitle">Le système intelligent de prédiction de churn B2B pour RavenStack.</p>
        
        <div class="status-badge" :class="{ 'online': isBackendOnline, 'offline': !isBackendOnline }">
          <span class="indicator"></span>
          Backend API : {{ backendStatus }}
        </div>
      </div>
    </header>

    <main class="features-grid">
      <div class="feature-card">
        <div class="icon">📊</div>
        <h3>Analyse des Données</h3>
        <p>Traitement complet de nos 5 bases de données PostgreSQL : comptes, abonnements, usages et support.</p>
      </div>
      
      <div class="feature-card">
        <div class="icon">🤖</div>
        <h3>AI & Scoring</h3>
        <p>Modèles prédictifs Scikit-learn embarqués pour identifier les signaux faibles d'attrition.</p>
      </div>
      
      <div class="feature-card">
        <div class="icon">⚡</div>
        <h3>Alertes Temps Réel</h3>
        <p>Tableau de bord interactif pour l'équipe Customer Success de RavenStack et actions priorisées.</p>
      </div>
    </main>

    <footer class="sprint-info">
      Sprint 1 : Découverte et mise en place &bull; Équipe Data Marketing
    </footer>
  </div>
</template>

<style scoped>
.landing-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0d1117;
  color: #c9d1d9;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.hero {
  padding: 6rem 2rem 4rem;
  text-align: center;
  background: radial-gradient(circle at top, #1f2937 0%, #0d1117 70%);
  border-bottom: 1px solid #30363d;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.gradient-text {
  font-size: 4.5rem;
  font-weight: 800;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -2px;
}

.subtitle {
  font-size: 1.5rem;
  color: #8b949e;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid #30363d;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.indicator {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #8b949e;
}

.online { border-color: rgba(46, 160, 67, 0.4); background: rgba(46, 160, 67, 0.1); color: #3fb950; }
.online .indicator { background: #3fb950; box-shadow: 0 0 10px rgba(63, 185, 80, 0.5); }
.offline { border-color: rgba(248, 81, 73, 0.4); background: rgba(248, 81, 73, 0.1); color: #f85149; }
.offline .indicator { background: #f85149; box-shadow: 0 0 10px rgba(248, 81, 73, 0.5); }

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
  flex: 1;
}

.feature-card {
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 12px;
  padding: 2rem;
  text-align: left;
  transition: transform 0.2s, border-color 0.2s;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: #8b949e;
}

.icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.25rem;
  color: #fff;
  margin-top: 0;
  margin-bottom: 1rem;
}

.feature-card p {
  color: #8b949e;
  line-height: 1.5;
  margin: 0;
}

.sprint-info {
  text-align: center;
  padding: 2rem;
  color: #8b949e;
  font-size: 0.9rem;
  border-top: 1px solid #30363d;
  background: #161b22;
}
</style>
