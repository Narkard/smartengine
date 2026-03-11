# smartEngine - Système de prédiction de Churn

## Contexte
Projet réalisé pour **RavenStack**, un SaaS B2B, dans le cadre du module "Scoring prédictif et Marketing". L'objectif est de construire un système intelligent capable de prédire le taux d'attrition (churn) des clients.

## Structure du Projet
Le dépôt est organisé selon la méthodologie du Sprint 1 :
- `.gemini/agents/` : Contient les agents IA spécialisés.
- `data/` : Dossier des données (ignoré par Git). **Note :** Créer un sous-dossier `raw/` et y placer les CSV clients.
- `docs/` : Documentation (Veille, Brief, Dossier de conception, Standups).
- `outputs/` : Rapports et datasets générés (ignoré par Git).
- `src/` : Scripts Python et pipeline de données (ignoré par Git).
- `GEMINI.md` : Fiche de contexte pour l'outil d'orchestration.

## Installation et Utilisation

### Prérequis
- Node.js (v18+)
- Python (3.11+)
- Gemini CLI : `npm install -g @google/gemini-cli`

### Démarrage
1. Cloner le dépôt : `git clone https://github.com/Narkard/smartengine.git`
2. Créer votre branche : `git checkout -b votre-prenom`
3. Lancer l'outil : `gemini`

### Agents disponibles
Pour explorer les données :
```bash
gemini --agent .gemini/agents/data-explorer.md
```

## Équipe
- **Groupe X**
- Product Owner : [Nom]
- Scrum Master : [Nom]
- Développeurs IA : [Noms]
