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
## 2. Traitement des données (Sprint 2)

### 2.1 État des données brutes et nettoyage
Avant traitement, les données présentaient plusieurs anomalies :
- **churn_flag** : Incohérent entre les sources (110 vs 352 événements réels).
- **support_tickets** : 41% de valeurs manquantes pour le `satisfaction_score`.
- **subscriptions** : Présence d'outliers extrêmes sur le MRR (comptes tests ou erreurs de saisie).

**Stratégies choisies :**
- **Imputation** : Médiane pour les scores de satisfaction (robuste aux extrêmes).
- **Winsorisation** : Clipping du MRR au 99ème percentile.
- **Exclusion** : Suppression radicale de la colonne `churn_flag` d'origine pour éviter toute pollution du modèle.

### 2.2 Construction de la table analytique
La table `analytics.csv` est construite par jointures successives à partir du référentiel `accounts_cleaned.csv` :
- **Granularité** : Une ligne par `account_id`.
- **Méthode de jointure** : `left join` systématique pour conserver tous les comptes, même ceux n'ayant pas encore utilisé le produit ou ouvert de tickets.
- **Cible (Target)** : Recalculée via la présence ou non dans `churn_cleaned.csv`.

### 2.3 Feature Engineering (Détails et Justification)
| Feature | Source | Justification Métier |
| :--- | :--- | :--- |
| `usage_trend_30d` | Usage | Capture le désengagement progressif avant le churn effectif. |
| `days_since_last_usage` | Usage | Mesure l'inactivité immédiate (signal d'alerte critique). |
| `critical_ratio` | Support | Identifie les comptes en situation de tension technique majeure. |
| `nb_unique_features` | Usage | Mesure l'adoption du produit (stickiness). |
| `seniority_months` | Sub | Distingue le churn précoce (onboarding raté) du churn mature. |
| `nb_upgrades` | Sub | Indique la satisfaction et la croissance du compte (anti-churn). |

### 2.4 Retour d'expérience sur l'Agent de Traitement
L'agent `data-engineer` a été configuré pour automatiser ces tâches. 
- **Points forts** : Excellente gestion des types temporels et des chemins relatifs. 
- **Ajustements nécessaires** : L'agent a dû être explicitement instruit d'ignorer le `churn_flag` d'origine, qu'il avait tendance à conserver par défaut. La séparation en trois scripts (`clean`, `build`, `analytics`) a permis une meilleure traçabilité.

---
### 2.3 Tâche de recherche : Théorie du Feature Engineering

**Importance vs Algorithme** : Le feature engineering est souvent plus crucial que le choix du modèle car il fournit la "matière première". Un algorithme sophistiqué sur des données pauvres (brutes) performera moins bien qu'un modèle simple sur des features riches et intelligentes qui isolent les signaux métiers.

**Variables de Tendance** : Elles se calculent en comparant une fenêtre temporelle récente à une fenêtre de référence passée. Exemple : `(Moyenne_Mois_N / Moyenne_Mois_N-1) - 1`.

**Encodage des variables** :
- **One-Hot Encoding** : Création d'une colonne binaire par catégorie. À utiliser pour les variables nominales sans ordre (ex: Secteur d'activité).
- **Label Encoding** : Conversion en entiers (1, 2, 3). À utiliser pour les variables ordinales (ex: Plan Starter < Pro < Enterprise).

**Normalisation vs Standardisation** :
- **Normalisation** : Ramène les valeurs entre [0, 1]. Utile pour les algorithmes basés sur la distance (K-Means, KNN).
- **Standardisation** : Centre les données (moyenne 0, écart-type 1). Préférable pour les modèles linéaires et les réseaux de neurones.
- *Note : Les arbres de décision (Random Forest) n'en ont généralement pas besoin.*

## 3. Modélisation et Évaluation (Sprint 3)

### 3.1 Choix de l'Algorithme : Random Forest
Nous avons sélectionné le **Random Forest** pour sa capacité à gérer des relations non-linéaires complexes entre les features d'usage et de support. Contrairement à une régression logistique, il capture mieux les seuils critiques (ex: une baisse d'usage brutale est plus prédictive qu'une baisse linéaire).
- **Justification Métier** : Le modèle est "robuste" et moins sensible aux valeurs extrêmes qui persistent malgré le nettoyage, garantissant une stabilité des scores pour les équipes CS.

### 3.2 Gestion du déséquilibre des classes
Le dataset présente une majorité de comptes sains (Non-Churn). Nous avons utilisé le paramètre `class_weight='balanced'` pour forcer l'algorithme à accorder autant d'importance à la détection d'un churn (classe minoritaire) qu'à celle d'un compte stable.

### 3.3 Métriques retenues : Le Rappel (Recall) avant tout
Pour RavenStack, le **Recall est la priorité absolue** :
- **Justification** : Le coût d'un "Churn non détecté" (perte de MRR sèche) est bien plus élevé que le coût d'une "Fausse Alerte" (un appel de courtoisie du Customer Success vers un client qui n'allait pas partir). Il vaut mieux contacter 10 clients stables par erreur que de rater 1 client sur le départ.

### 3.4 Interprétation des Features Importantes
Les variables d'usage (`usage_trend_30d`) et de support (`critical_ratio`) dominent le modèle. Cela confirme l'hypothèse métier : un client qui réduit son activité tout en multipliant les tickets critiques est en phase de rupture imminente.

### 3.5 Analyse des Biais et Limites
- **Biais** : Une analyse par industrie montre que le modèle est légèrement plus "sévère" avec le secteur EdTech. Cela nécessite une vigilance humaine lors de l'interprétation.
- **Limites** : Le modèle ne prend pas encore en compte les données de sentiment (analyse de texte des tickets), ce qui pourrait affiner la prédiction.

### 3.6 Justification des Seuils de Risque (PO Vision)
Nous avons défini trois segments d'action pour l'équipe Customer Success :
- **High (>= 0.65)** : **Priorité Absolue.** Probabilité de départ imminente. Action : Appel direct du CSM sous 24h avec proposition commerciale (remise ou formation offerte).
- **Medium (0.35 - 0.65)** : **Vigilance.** Engagement en baisse. Action : Envoi d'un mail personnalisé automatisé proposant un point de situation.
- **Low (< 0.35)** : **Sain.** Suivi standard.

**Logique de Rentabilité** : Les seuils ont été calibrés pour maximiser le Recall sur le segment High. Le coût opérationnel d'intervention est concentré là où la probabilité de sauvetage est la plus forte, optimisant ainsi le ROI du service CS.

## 4. Déploiement (Sprint 4)
### 4.1 Dashboard
Développement d'une interface **Streamlit** permettant :
- Visualisation des KPIs (MRR, Taux de Churn).
- Analyse de la corrélation Usage/Revenu.
- Tableau d'alertes dynamique pour les équipes Customer Success.

*Dernière mise à jour : 29 mars 2026*

