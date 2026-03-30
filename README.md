# smartEngine - Système de prédiction de Churn

## Contexte
Projet réalisé pour **RavenStack**, un SaaS B2B, dans le cadre du module "Scoring prédictif et Marketing". L'objectif est de construire un système intelligent capable de prédire le taux d'attrition (churn) des clients.

## Statut du Projet
- **Sprint 1 : Exploration et Cadrage (Terminé ✅)**
- **Sprint 2 : Préparation des données (Terminé ✅)**
- **Sprint 3 : Modélisation (À venir)**

## Structure du Projet
Le dépôt est organisé selon la méthodologie du Sprint 1 & 2 :
- `.gemini/agents/` : Contient les agents IA spécialisés.
- `data/` : Dossier des données. Les CSV bruts sont dans `data/raw/`.
- `docs/` : Documentation (Veille, Brief, Dossier de conception, Standups).
- `outputs/` : Contient le `master_dataset.csv` généré.
- `src/` : Scripts Python (Pipeline de données, Entraînement).
- `GEMINI.md` : Fiche de contexte pour l'outil d'orchestration.

## Installation et Utilisation

### Prérequis
- Node.js (v18+)
- Python (3.11+)
- Gemini CLI : `npm install -g @google/gemini-cli`

### Démarrage
1. Cloner le dépôt : `git clone https://github.com/Narkard/smartengine.git`
2. Créer votre branche : `git checkout -b Sophie`
3. Lancer l'outil : `gemini`

### Agents disponibles
Pour traiter les données :
```bash
gemini --agent .gemini/agents/data-processor.md
```

## Équipe
- **Groupe X**
- Product Owner : [Nom]
- Scrum Master : [Nom]
- Développeurs IA : Sophie, [Nom]
