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

## État d'avancement

### ✅ Sprint 1 : Initialisation (Terminé)
- Mise en place de l'arborescence et de la stack technique.
- Rédaction du brief client et du dossier de conception initial.
- Veille technologique sur la stack (Gemini CLI, Scikit-Learn, n8n).

### ✅ Sprint 2 : Traitement des données (Terminé)
- Création du pipeline automatisé (`src/data_pipeline.py`).
- Feature Engineering : Agrégation de l'usage, ratio de support client et encodage catégoriel.
- Génération du **Master Dataset** (500 clients, 25+ features) prêt pour le ML.

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

## Backlog du Projet
Le suivi des tâches et la gestion du backlog sont effectués sur l'outil suivant :
- **Lien du Backlog** : [GitHub Projects](https://github.com/Narkard/smartengine/projects)

## Équipe - Groupe X
- **Product Owner** : [Nom de l'étudiant]
- **Scrum Master** : [Nom de l'étudiant]
- **Développeurs IA** : [Prénom 1], [Prénom 2]
