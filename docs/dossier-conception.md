# Dossier de Conception - smartEngine

## 1. Cadrage du Projet

### 1.1 Contexte Métier
RavenStack est un SaaS B2B confronté à un enjeu de rétention client. Chaque départ (churn) entraîne une perte de revenu récurrent mensuel (MRR). Le projet smartEngine doit permettre d'anticiper ces départs.

### 1.2 Objectifs
- Prédire la probabilité de churn pour chaque compte.
- Prioriser les actions des équipes Customer Success (CS).
- Automatiser les notifications pour les comptes à haut risque.

### 1.3 Contraintes RGPD et Éthique
En conformité avec le RGPD et la loi Informatique et Libertés :
- **Minimisation des données** : Seules les données nécessaires à la prédiction du churn sont collectées et traitées.
- **Article 22** : L'utilisation d'un score automatisé doit rester une aide à la décision pour les équipes CS et non une décision entièrement automatisée ayant des impacts juridiques majeurs.
- **Transparence** : Les critères influençant le score doivent être explicables pour éviter les "boîtes noires" et les biais algorithmiques.

### 1.4 Choix des Outils
- **Gestionnaire de version** : GitHub pour la collaboration distribuée.
- **Orchestration IA** : Gemini CLI pour la génération de code et l'analyse automatisée.
- **Data Science** : Python, pandas et scikit-learn pour le pipeline de données et la modélisation.
- **Dashboarding** : Streamlit pour une interface légère et rapide à déployer.
- **Automatisation** : n8n pour les alertes de risque.

---
*Ce document sera complété à chaque sprint (Sprint 2 : Traitement des données).*
