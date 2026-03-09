# Contexte du Projet : smartEngine

## 1. Présentation du Client et du Projet
**Client** : RavenStack (SaaS B2B proposant une plateforme de gestion de projets pour les équipes tech).  
**Projet** : **smartEngine**, un système intelligent de prédiction de churn (attrition client).  
**Objectif Principal** : Anticiper la résiliation des abonnements mensuels et annuels pour réduire la perte de MRR (Monthly Recurring Revenue). Le système identifiera les signaux comportementaux précurseurs et alertera les équipes Customer Success.

## 2. Mission et Livrables Attendus
L'ensemble de la chaîne de valeur data doit être couverte à travers des agents IA :
- Analyser et nettoyer les données brutes.
- Identifier les signaux précurseurs du churn.
- Construire un modèle de scoring prédictif.
- Déployer ce scoring via un dashboard interactif pour les équipes Customer Success.
- Automatiser des alertes pour les comptes à risque élevé.

## 3. Données (Dossier `/data/raw/`)
RavenStack fournit un dataset synthétique relationnel, simulant l'activité de sa plateforme.  
**Il est formellement interdit de modifier les fichiers contenus dans `/data/raw/`.**

Le dataset est composé de 5 fichiers CSV interconnectés :
- **accounts.csv** (~500 lignes) : Données des comptes clients (secteur, pays, plan de base). *Clé primaire : account_id*.
- **subscriptions.csv** (~5 000 lignes) : Historique des abonnements, MRR/ARR, upgrades et downgrades. *Lié à accounts*.
- **feature_usage.csv** (~25 000 lignes) : Utilisation des fonctionnalités, temps passé, erreurs. *Lié à subscriptions*.
- **support_tickets.csv** (~2 000 lignes) : Historique des tickets de support, temps de résolution et satisfaction. *Lié à accounts*.
- **churn_events.csv** (~600 lignes) : Dates, motifs de résiliation et feedbacks. *Lié à accounts*.

## 4. Organisation et Conventions
- **Dépôt distant** : [https://github.com/Narkard/smartengine](https://github.com/Narkard/smartengine) utilisation via MCP Github.
- **Méthodologie** : AI Agents Orchestration et framework Scrum.
- **Sprint Actuel** : Sprint 1 - Découverte et mise en place.
- **Langue** : Tous les livrables et rapports doivent être rédigés en **français**.

### Arborescence et Conventions de Fichiers (`GEMINI.md`)
- `/backend/` : Dépendances et source de l'API (ex. FastAPI/Flask, Data Science).
- `/frontend/` : Interface utilisateur Vue.js.
- `/outputs/` : Rapports générés par les agents.
- `/data/raw/` : Données brutes (lecture seule).
- `/docs/` : Dossiers de conception, de veille et comptes-rendus de standup.
- `/.gemini/agents/` : Fichiers agents spécifiques aux tâches.

## 5. Stack Technique Actuelle
*(Note : Définie spécifiquement pour le sprint actuel)*
- **Orchestration** : Gravity (Agents IA)
- **Backend & Data Science** : Python (API), pandas, scikit-learn
- **Frontend / Data Viz** : Interface Vue.js
- **Versioning** : Git / GitHub utilisation via MCP Github.
