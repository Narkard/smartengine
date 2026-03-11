# Rapport de Veille Outils - Sprint 1

Ce rapport présente les outils de la stack technique imposée pour le projet smartEngine.

## 1. Gemini CLI
- **Présentation** : Outil d'interface en ligne de commande permettant d'orchestrer des agents IA.
- **Rôle dans le projet** : Interface principale pour diriger les agents qui génèrent et exécutent le code du projet.
- **Avantages** : Automatisation, capacité d'interaction directe avec le système de fichiers, gain de productivité.
- **Limites** : Nécessite une connexion internet, dépendance aux modèles LLM.
- **Alternatives** : Cursor, GitHub Copilot.

## 2. Python / pandas
- **Présentation** : Langage de programmation polyvalent et bibliothèque de manipulation de données.
- **Rôle dans le projet** : Traitement, nettoyage et analyse des données clients (SaaS RavenStack).
- **Avantages** : Écosystème riche, manipulations de tableaux (DataFrames) très performantes.
- **Limites** : Consommation mémoire importante sur de très gros volumes de données.
- **Alternatives** : R, Julia, Polars.

## 3. scikit-learn
- **Présentation** : Bibliothèque Python de référence pour le machine learning.
- **Rôle dans le projet** : Construction du modèle de scoring prédictif pour le churn.
- **Avantages** : Simple, vaste choix d'algorithmes, excellente documentation.
- **Limites** : Non optimisé pour le deep learning ou les données massives distribuées.
- **Alternatives** : TensorFlow, PyTorch, XGBoost.

## 4. Streamlit
- **Présentation** : Framework Python permettant de créer rapidement des applications web pour la data.
- **Rôle dans le projet** : Déploiement du dashboard interactif pour les équipes Customer Success.
- **Avantages** : Pas besoin de compétences en JS/HTML/CSS, déploiement très rapide.
- **Limites** : Personnalisation de l'UI plus rigide que du Vanilla JS.
- **Alternatives** : Dash (Plotly), Gradio.

## 5. n8n
- **Présentation** : Outil d'automatisation de workflows (no-code/low-code) open-source.
- **Rôle dans le projet** : Automatisation des alertes et des flux de travail entre les outils.
- **Avantages** : Interface visuelle, auto-hébergeable, grand nombre d'intégrations.
- **Limites** : Configuration initiale plus complexe que Zapier.
- **Alternatives** : Zapier, Make (Integromat).

## 6. GitHub
- **Présentation** : Plateforme de gestion de code source basée sur Git.
- **Rôle dans le projet** : Centralisation du code, collaboration en équipe via les branches et versioning.
- **Avantages** : Standard du marché, outils de collaboration (Issues, Projects).
- **Limites** : Courbe d'apprentissage pour Git.
- **Alternatives** : GitLab, Bitbucket.

---
**Sources citées** :
- [Gemini CLI Documentation](https://geminicli.com/docs/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Scikit-Learn Official Site](https://scikit-learn.org/)
- [Streamlit Framework](https://streamlit.io/)
- [n8n Automation](https://n8n.io/)
