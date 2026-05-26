# Plan de Soutenance - Projet smartEngine

**Durée totale de la présentation :** 20 minutes
**Public cible :** Jury de soutenance (profils stratégiques et techniques)

---

### 1. Introduction et contexte (2 min) — Sophie
- Présentation générale de l'enjeu stratégique pour RavenStack : la fidélisation client et la sécurisation du MRR face à un churn mal anticipé.
- Objectifs du projet smartEngine : passer d'une gestion réactive à une prédiction proactive de l'attrition.
- Cadrage et contraintes clés : respect du RGPD (Article 22), transparence des algorithmes (explicabilité) et maintien de l'expertise humaine dans la boucle de décision finale.

### 2. Données et feature engineering (4 min) — Quentin
- Bilan sur l'état des données brutes, les défis rencontrés (incohérences sur le flag de churn d'origine, valeurs aberrantes sur le MRR) et les choix de nettoyage (Winsorisation, Imputation de la médiane).
- La stratégie de Feature Engineering : focus sur la création de signaux métiers forts capables de traduire le désengagement.
- Exemples concrets des features générées (ex: `usage_trend_30d` pour la baisse d'utilisation, `critical_ratio` pour les tensions sur le support technique).

### 3. Modélisation et évaluation (4 min) — Maé
- Justification du choix de l'algorithme : l'utilisation du Random Forest pour sa robustesse face aux données et sa capacité à capter des effets de seuil (vs. Régression Logistique).
- Gestion du déséquilibre des classes (comptes en attrition minoritaires) et arbitrage des métriques d'évaluation.
- Explication du choix stratégique assumé d'optimiser en priorité le **Recall** : le coût business d'un churn non détecté est largement supérieur au coût d'un faux positif (appel CS inutile).

### 4. Dashboard et démo live (5 min) — Léo
- Présentation de la solution applicative conçue spécifiquement pour l'équipe Customer Success.
- Démonstration de l'interface Streamlit avec un "entonnoir de décision" : 
  1. Vue d'ensemble des KPIs (Portefeuille).
  2. Matrice de segmentation et visualisation rapide des comptes urgents (Priorisation).
- Explicabilité des résultats (Fiche Compte) : démo d'un graphique SHAP (waterfall) traduisant l'algorithme de façon compréhensible pour expliquer "pourquoi" ce compte spécifique est en danger.

### 5. ROI et feuille de route (3 min) — Sophie
- Évaluation de l'impact financier estimé : ~577 k€ de MRR menacé dans le quadrant Urgence Absolue, et ~230 k€ / mois potentiellement sauvés avec un taux de rétention de 40 %.
- Feuille de route pour le lancement : la phase pilote sur 4 semaines visant à adapter l'outil à la bande passante réelle des CSM et à accompagner la conduite du changement.
- Le protocole de mesure strict : test A/B prévu pour évaluer l'*uplift* de rétention et isoler scientifiquement la performance générée par le modèle (groupe de traitement vs témoin).

### 6. Bilan agents IA (2 min) — Maé
- Retour d'expérience sur notre méthodologie de développement novatrice utilisant l'orchestration de 4 agents (Gemini CLI) sur 4 sprints.
- Points de friction identifiés (ex: recadrage systématique sur l'optimisation du Recall) face aux gains de temps considérables en écriture de scripts.
- Conclusion finale : l'IA en tant qu'accélérateur technique incontournable, et l'indispensabilité de l'intelligence métier humaine pour le guidage éthique, réglementaire et la création de valeur de bout en bout.
