# 📋 Répartition des Tâches — Sprint 4 (smartEngine)

> **Projet :** smartEngine — Prédiction de churn pour RavenStack (SaaS B2B)
> **Sprint :** 4 / 4 (Dernier sprint — Passage à l'action)
> **Objectif global :** Transformer les scores de churn du Sprint 3 en un outil de décision actionnable pour les équipes métier (Customer Success & Direction).

---

## 👥 Équipe Sprint 4

| Rôle | Membre |
| :--- | :--- |
| 🎯 **Product Owner** | Sophie |
| 🔁 **Scrum Master** | Joanne |
| 💻 **Développeur IA** | Léo (Moi) |
| 💻 **Développeur IA** | Quentin |
| 💻 **Développeur IA** | Maé |

> ⚠️ **Rotation des rôles** : Vérifier avant de commencer que chaque membre a occupé chaque rôle (PO, SM, Développeur IA) au moins une fois sur l'ensemble du projet (obligation sprint 4).

---

## ✅ Prérequis avant de commencer le Sprint 4

Avant tout développement, s'assurer collectivement que :

- [ ] `outputs/models/churn_model.joblib` existe et est fonctionnel
- [ ] `outputs/scores.csv` contient une probabilité de churn + niveau de risque par compte
- [ ] `outputs/rapport-modele.md` est complet
- [ ] `docs/dossier-conception.md` (ou `.docx`) contient les sections 1 à 3
- [ ] Le backlog Sprint 3 est à jour (toutes les stories passées en **Done**)

---

## 🗂️ Les 3 Axes du Sprint 4

```
Sprint 4 = Rendre les scores ACTIONNABLES
   │
   ├─── 1. Segmentation risque/valeur  →  outputs/priorisation.csv
   ├─── 2. Dashboard Streamlit          →  src/dashboard.py
   └─── 3. Recommandations & ROI        →  outputs/recommandations.md
```

> ❗ **On ne réentraîne PAS le modèle dans ce sprint.** On consomme uniquement les scores produits au Sprint 3.

---

## 📌 Tâches Détaillées par Membre

---

### 🎯 Sophie — Product Owner

**Livrable principal :** `outputs/recommandations.md`

#### A. Tâche de recherche (à documenter dans le dossier de conception)
Répondre aux questions suivantes et les intégrer dans la section 4 :

| Question | Où l'intégrer |
| :--- | :--- |
| Comment présenter des résultats de data science à un comité de direction non technique ? Quelles erreurs éviter ? | Section 4 — Recommandations |
| Comment construire un business case pour un projet de rétention client ? Quels chiffres utiliser ? | Section 4 — ROI |
| Qu'est-ce qu'un test A/B et un groupe témoin ? Qu'est-ce que l'uplift ? Pourquoi est-ce indispensable pour prouver la valeur d'une action marketing ? | Section 4 — Mesure d'impact |
| Qu'est-ce que la conduite du changement dans le déploiement d'un outil data ? Quels freins peuvent rencontrer les équipes métier ? | Section 4 — Conduite du changement |

#### B. Document de recommandations (`outputs/recommandations.md`)
Ce document est rédigé **pour la direction de RavenStack (public non technique)**. Il doit répondre à 4 questions précises :

1. **Que dit le modèle ?**
   - Résumé en langage non technique : taux de churn global prédit
   - Profils les plus à risque (secteur, plan, ancienneté)
   - Facteurs principaux identifiés (ex : baisse d'usage + tickets critiques)

2. **Quelles actions par quadrant ?**

   | Quadrant | Profil | Action recommandée |
   | :--- | :--- | :--- |
   | Risque élevé / Valeur élevée | Gros comptes en danger | Appel CSM direct sous 24h + proposition commerciale (remise ou formation) |
   | Risque élevé / Valeur faible | Petits comptes en danger | Email automatisé de relance / offre de fidélisation |
   | Risque faible / Valeur élevée | Gros comptes fidèles | Surveillance proactive, newsletter exclusive, ne pas sur-solliciter |
   | Risque faible / Valeur faible | Petits comptes stables | Aucune action prioritaire |

3. **Quel ROI estimé ?**
   - Calculer : combien coûte le churn actuellement (MRR perdu × nb comptes qui churned)
   - Estimer : combien peut-on sauver en retenant X% des comptes prioritaires (Quadrant 1)
   - Estimer : quel est le coût des actions (temps CSM, coût des remises, emails automatiques)
   - Conclure : ROI = (MRR sauvé − Coût des actions) / Coût des actions

4. **Quelle feuille de route de déploiement ?**
   - Phase pilote : cibler uniquement le Quadrant 1 (risque élevé / valeur élevée) sur 4 semaines
   - Mesurer les résultats (voir protocole ci-dessous)
   - Élargissement progressif aux autres quadrants si les résultats sont concluants

5. **Protocole de mesure d'impact (obligatoire)**
   - **Groupe témoin** : Séparer les comptes à risque en 2 groupes. Un groupe reçoit l'action de rétention, l'autre (témoin) ne reçoit rien.
   - **Test A/B** : Comparer le taux de rétention des deux groupes après quelques semaines.
   - **Uplift** : Mesurer la différence de rétention entre groupe traité et groupe témoin. C'est la seule façon de prouver que l'action crée de la valeur (et non que les comptes seraient restés de toute façon).
   - **KPI de suivi** : taux de rétention, MRR sauvé, coût par compte retenu.

#### C. Contribution au Dossier de conception (Section 4)
- Sous-section **Recommandations et mesure d'impact** : méthode de calcul du ROI, protocole de mesure (groupe témoin, uplift), conduite du changement

#### D. Soutenance
- Préparer la partie **pitch commercial et métier** : présenter les recommandations et le ROI au jury comme si c'était la direction de RavenStack.

---

### 🔁 Joanne — Scrum Master

**Livrables principaux :** Infrastructure projet + coordination

#### A. Mise à jour du Backlog Sprint 4
- Passer **toutes** les stories des Sprints 1 à 3 en **Done** (dans l'outil de gestion utilisé aux sprints précédents)
- Ajouter et assigner les nouvelles user stories du Sprint 4 :

  | ID | En tant que... | Je veux... | Afin de... | Assigné à |
  | :--- | :--- | :--- | :--- | :--- |
  | US-S4-01 | Responsable Customer Success | Un dashboard interactif | Consulter les comptes à risque sans écrire de code | Léo |
  | US-S4-02 | Directeur commercial | Recevoir une alerte quand un compte VIP passe en risque élevé | Déclencher un appel dans les 24 heures | Léo |
  | US-S4-03 | Direction RavenStack | Un document de recommandations avec ROI estimé | Décider du budget à allouer à la rétention | Sophie |
  | US-S4-04 | Product Owner | Un support de soutenance structuré | Présenter le projet de manière convaincante au jury | Toute l'équipe |
  | US-S4-05 | Développeur IA | Un fichier `priorisation.csv` | Alimenter le dashboard avec les quadrants | Quentin |
  | US-S4-06 | Scrum Master | Un `GEMINI.md` complet et à jour | Avoir une référence unique de l'état du projet | Joanne |

#### B. Finalisation du `GEMINI.md` (racine du projet)
Le fichier `GEMINI.md` doit être la **référence ultime** de l'état du projet. Contenu attendu :
- Bilan des 4 sprints (résultats, décisions, livrables)
- Liste de tous les agents créés et leur rôle
- Conventions de nommage (fichiers, répertoires)
- Chemins vers les fichiers clés : modèle, scores, dashboard
- Rôles de chaque sprint (qui a fait quoi)
- État final du projet

#### C. Daily Standups
- Planifier et animer les standups quotidiens
- Documenter chaque standup dans `docs/standups/` (format : `AAAA-MM-JJ.md`)
- Structure minimale de chaque standup :
  ```
  ## Standup AAAA-MM-JJ
  ### Léo : Hier / Aujourd'hui / Blocages
  ### Quentin : Hier / Aujourd'hui / Blocages
  ### Maé : Hier / Aujourd'hui / Blocages
  ### Sophie : Hier / Aujourd'hui / Blocages
  ```

#### D. Coordination du Dossier de conception — Section 4
- Coordonner la rédaction collective de la **Section 4** (chaque membre contribue sa partie)
- Rédiger la sous-section **Retour d'expérience sur les agents IA** (bilan sur les 4 sprints) :
  - Quels agents ont été créés, enrichis, abandonnés ?
  - Qu'est-ce qui a bien fonctionné ?
  - Qu'est-ce qui a nécessité une intervention manuelle ?

#### E. Support de Soutenance (`docs/soutenance.pptx`)
- Structurer le plan global du support (fil conducteur de la présentation)
- S'assurer que le support respecte le temps imparti et couvre tous les sprints
- Coordonner les contributions de chaque membre

#### F. Sprint Review / Soutenance
- La Sprint Review du Sprint 4 **est la soutenance elle-même**

#### G. Rétrospective finale (15 min après la soutenance)
Organiser et documenter la rétrospective sur l'ensemble du projet :
- Qu'est-ce qui a bien fonctionné ?
- Qu'est-ce qui aurait pu être amélioré ?
- Qu'avez-vous appris individuellement ?
- Que feriez-vous différemment si vous recommenciez ?

---

### 💻 Léo (Moi) — Développeur IA

**Livrable principal :** `src/dashboard.py` + `requirements.txt`

#### A. Tâche de recherche (à documenter dans le dossier de conception)

| Question | Concept clé |
| :--- | :--- |
| Qu'est-ce que le **data storytelling** ? Comment structurer un dashboard pour raconter une histoire avec les données ? | Data storytelling |
| Quels sont les principes d'**accessibilité visuelle (WCAG)** à respecter ? Comment gérer le daltonisme dans les choix de couleurs ? | WCAG / Accessibilité |
| Comment présenter un **score de probabilité** à un public non technique sans créer de fausses certitudes ? | Communication des probabilités |

#### B. Dashboard Streamlit (`src/dashboard.py`)

Le dashboard est l'interface entre le modèle et les équipes métier. Il doit être **utilisable par un responsable Customer Success non technique**.

**Source de données :** `outputs/scores.csv` + `outputs/priorisation.csv`
**Commande d'exécution :** `streamlit run src/dashboard.py`

##### Vue 1 — Portefeuille (vue globale)
- KPIs en haut de page :
  - Nombre total de comptes
  - Taux de churn prédit (% de comptes en risque élevé)
  - MRR total à risque (€)
- Graphique de distribution des scores de churn (histogramme ou KDE)
- Graphique de répartition des comptes par quadrant (camembert ou barres)
- Graphique de distribution par plan (Starter / Pro / Enterprise)

##### Vue 2 — Priorisation (liste d'action)
- Visualisation graphique de la matrice risque/valeur (scatter plot : axe X = churn_score, axe Y = MRR, couleur = quadrant)
- Tableau filtrable et triable des comptes avec colonnes :
  - `account_id`, `churn_score`, `risk_level`, `MRR`, `quadrant`, `action recommandée`, `plan`, `seniority_months`
- Filtres : par quadrant, par plan, par seuil de score, par fourchette de MRR

##### Vue 3 — Fiche compte (détail individuel)
Accessible en sélectionnant un compte dans le tableau ou via un champ de recherche :
- **Profil du compte** : plan, ancienneté (mois), usage récent, nombre de tickets, score de satisfaction
- **Score de churn** : jauge visuelle (ex : 0.78 → risque élevé) présentée de manière non technique
- **Quadrant & Action recommandée** : affichée en évidence (ex : « 🚨 Appel CSM sous 24h »)
- **Explication SHAP** : graphique en barres horizontales montrant les 5 facteurs qui augmentent ou diminuent le score pour ce compte spécifique (ex : usage_trend_30d ↓ = +0.15 vers churn)

##### Contraintes techniques
- Exécutable **sans Gemini CLI** (le dashboard est un livrable autonome de production)
- `requirements.txt` doit lister toutes les dépendances : `streamlit`, `pandas`, `shap`, `matplotlib`, `plotly`, etc.
- Respecter les normes **WCAG** : contraste suffisant, ne pas utiliser uniquement la couleur pour distinguer les quadrants (ajouter icônes ou libellés), palette adaptée au daltonisme (éviter rouge/vert pur, préférer orange/bleu)

#### C. Contribution au Dossier de conception — Section 4
Rédiger la sous-section **Dashboard** :
- Choix des visualisations et pourquoi
- Organisation des trois vues (logique narrative)
- Gestion de l'accessibilité (WCAG, daltonisme)
- Retour d'expérience sur Streamlit
- Comment l'agent a été utilisé pour générer le code

#### D. Support de soutenance
- Contribuer la partie technique Dashboard (captures d'écran, démonstration live si possible)

---

### 💻 Quentin — Développeur IA

**Livrable principal :** `outputs/priorisation.csv`

#### A. Tâche de recherche (à documenter dans le dossier de conception)

| Question | Concept clé |
| :--- | :--- |
| Qu'est-ce que le **MRR** (Monthly Recurring Revenue) et la **CLV** (Customer Lifetime Value) ? Comment estimer la valeur d'un compte ? | MRR / CLV |
| Qu'est-ce qu'une **matrice de priorisation** ? En quoi croiser deux dimensions aide-t-il à décider ? | Matrice risque/valeur |
| Qu'est-ce que la **Next Best Action** ? Comment associer une action à un segment de clients ? | Next Best Action |
| Que dit l'**article 22 du RGPD** sur les décisions automatisées ? Que signifie « garder l'humain dans la boucle » et pourquoi un score de churn ne doit-il jamais, à lui seul, déclencher une action ? | RGPD art. 22 / Humain dans la boucle |

#### B. Fichier de priorisation (`outputs/priorisation.csv`)

**Source de données :** `outputs/scores.csv` (Sprint 3) + données MRR depuis `data/processed/analytics.csv`

##### Étape 1 — Chargement et croisement
- Charger `scores.csv` (colonnes : `account_id`, `churn_score`, `risk_level`)
- Extraire le MRR par compte depuis `analytics.csv`
- Joindre les deux sources sur `account_id`

##### Étape 2 — Définition du seuil de valeur
- Calculer la **médiane du MRR** du portefeuille
- Justifier ce choix (ou choisir un seuil alternatif et le justifier)
- Créer la colonne binaire `value_level` : `high` si MRR ≥ médiane, `low` sinon

##### Étape 3 — Affectation des quadrants
Logique d'affectation :

| Condition | Quadrant | Action recommandée |
| :--- | :--- | :--- |
| `risk_level == 'high'` ET `value_level == 'high'` | Q1 - Priorité maximale | Appel CSM direct sous 24h |
| `risk_level == 'high'` ET `value_level == 'low'` | Q2 - Action automatisée | Email de relance automatisé |
| `risk_level != 'high'` ET `value_level == 'high'` | Q3 - Surveillance | Fidélisation douce, ne pas déranger |
| `risk_level != 'high'` ET `value_level == 'low'` | Q4 - Aucune action | Aucune action prioritaire |

##### Étape 4 — Génération du fichier CSV
Structure **stricte** du fichier final :

```
account_id, churn_score, risk_level, MRR, value_level, quadrant, action_recommandee
```

- Trier par `quadrant` puis par `churn_score` décroissant
- Vérifier l'absence de valeurs manquantes
- Vérifier que `priorisation.csv` est bien lisible par `dashboard.py` de Léo (coordonner)

##### Étape 5 — Pourquoi pas un clustering ?
Documenter la justification (pour le dossier de conception) :
- K-Means découvrirait des groupes automatiquement mais difficiles à interpréter
- La matrice risque/valeur est volontairement simple : chaque quadrant = une décision métier claire
- Ça parle directement aux équipes CS sans nécessiter d'expertise statistique

#### C. Contribution au Dossier de conception — Section 4
Rédiger la sous-section **Segmentation risque / valeur** :
- Définition du MRR et de la CLV
- Justification du choix de la médiane comme seuil de découpage
- Pourquoi la matrice plutôt que le clustering
- Définition de la Next Best Action par quadrant
- Articulation avec l'article 22 du RGPD (humain dans la boucle)

#### D. Support de soutenance
- Contribuer la partie segmentation et matrice risque/valeur

---

### 💻 Maé — Développeur IA

**Livrable principal :** `.gemini/agents/agent-deploiement.md` (nouveau agent ou enrichissement d'un agent existant)

#### A. Choix et justification de l'approche agent
Deux options possibles (choisir et justifier dans le dossier de conception) :
1. **Enrichir un agent existant** (ex : `model-trainer.md`) en ajoutant les capacités de déploiement
2. **Créer un nouvel agent dédié** `agent-deploiement.md`

Quel que soit le choix, documenter **pourquoi** dans la section 4 du dossier de conception.

#### B. Agent de déploiement (`.gemini/agents/agent-deploiement.md`)
L'agent doit être capable de :
- Générer ou enrichir `src/dashboard.py` à partir de `scores.csv` et `priorisation.csv`
- Vérifier la cohérence des fichiers de sortie (colonnes présentes, pas de NaN, types corrects)
- Générer / mettre à jour `requirements.txt` avec les bonnes dépendances
- Documenter ses propres interventions (log ou commentaires dans les fichiers produits)

Structure minimale du fichier agent :
```markdown
# Agent : [Nom]

## Rôle
## Contraintes
## Entrées attendues
## Sorties produites
## Workflow
## Rappels importants (autonomie, pas de dépendance à Gemini en production)
```

#### C. Autonomie des scripts de production
> ⚠️ **Rappel critique du PDF** : À la livraison finale, le projet ne contiendra pas Gemini CLI. Tous les scripts produits dans ce sprint (`dashboard.py` notamment) doivent fonctionner de manière **autonome**, sans dépendre d'un agent.

Vérifier que :
- `src/dashboard.py` s'exécute avec `streamlit run src/dashboard.py` sans aucune intervention de Gemini
- `outputs/priorisation.csv` peut être regénéré en lançant un script Python seul
- `requirements.txt` est complet et à jour

#### D. Bilan global des agents IA (Section 4 du dossier de conception)
Rédiger la sous-section **Retour d'expérience sur les agents** en retraçant les 4 sprints :

| Sprint | Agent | Statut | Points forts | Limites / interventions manuelles |
| :--- | :--- | :--- | :--- | :--- |
| Sprint 1 | `data-explorer.md` | Créé | … | … |
| Sprint 2 | `data-engineer.md` | Créé | … | … |
| Sprint 3 | `model-trainer.md` | Créé | … | … |
| Sprint 4 | `agent-deploiement.md` | Créé / Enrichi | … | … |

#### E. Limites et perspectives du modèle (Section 4 du dossier de conception)
Rédiger la sous-section **Limites et perspectives** :
- Qu'est-ce que le modèle ne capture pas (ex : données de sentiment des tickets, données externes)
- Biais identifiés (ex : secteur EdTech légèrement surpénalisé)
- Améliorations possibles avec plus de temps ou de données :
  - Analyse NLP des textes de tickets de support
  - Données comportementales plus granulaires (sessions, features utilisées)
  - Réentraînement périodique (drift du modèle)
  - Modèle de survie (survival analysis) pour modéliser le temps avant churn

#### F. Support de soutenance
- Contribuer la partie bilan des agents et retour d'expérience IA

---

## 🏗️ Structure du Dépôt à la fin du Sprint 4

```
smartengine-groupe-X/
├── .gitignore
├── GEMINI.md                           ← Mis à jour (Joanne)
├── README.md
├── requirements.txt                    ← NOUVEAU Sprint 4 (Léo)
├── .gemini/
│   └── agents/
│       ├── data-explorer.md            # Sprint 1
│       ├── data-engineer.md            # Sprint 2
│       ├── model-trainer.md            # Sprint 3
│       └── agent-deploiement.md        # NOUVEAU Sprint 4 (Maé)
├── data/
│   ├── raw/                            # Les 5 CSV d'origine (JAMAIS modifiés)
│   └── processed/
│       └── analytics.csv              # Table analytique (Sprint 2)
├── outputs/
│   ├── rapport-nettoyage.md           # Sprint 2
│   ├── rapport-modele.md              # Sprint 3
│   ├── scores.csv                     # Sprint 3
│   ├── evaluation_metrics.json        # Sprint 3
│   ├── models/
│   │   └── churn_model.joblib         # Modèle sauvegardé (Sprint 3)
│   ├── priorisation.csv               # NOUVEAU Sprint 4 (Quentin)
│   └── recommandations.md             # NOUVEAU Sprint 4 (Sophie)
├── src/
│   ├── clean_data.py                  # Sprint 2
│   ├── build_features.py              # Sprint 2
│   ├── build_analytics.py             # Sprint 2
│   ├── train_model.py                 # Sprint 3
│   ├── evaluate_model.py              # Sprint 3
│   ├── generate_scores.py             # Sprint 3
│   └── dashboard.py                   # NOUVEAU Sprint 4 (Léo)
└── docs/
    ├── standups/                      # Daily standups (Joanne)
    ├── dossier-conception.md          # Sections 1 à 4 (Sprint 4 = Section 4)
    ├── backlog.md                     # Sprint 4 à jour (Joanne)
    └── soutenance.pptx                # Support de présentation (toute l'équipe)
```

---

## 📅 Synthèse des Livrables

| # | Livrable | Fichier attendu | Responsable | Priorité |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Fichier de priorisation | `outputs/priorisation.csv` | **Quentin** | 🔴 Critique (alimente le dashboard) |
| 2 | Dashboard Streamlit | `src/dashboard.py` + `requirements.txt` | **Léo** | 🔴 Critique |
| 3 | Document de recommandations | `outputs/recommandations.md` | **Sophie** | 🔴 Critique |
| 4 | Section 4 dossier de conception | `docs/dossier-conception.md` | **Toute l'équipe** (Joanne pilote) | 🟠 Important |
| 5 | Agent de déploiement | `.gemini/agents/agent-deploiement.md` | **Maé** | 🟠 Important |
| 6 | GEMINI.md final | `GEMINI.md` (racine) | **Joanne** | 🟠 Important |
| 7 | Backlog Sprint 4 | Outil de gestion / `docs/backlog.md` | **Joanne** | 🟡 À faire en début de sprint |
| 8 | Support de soutenance | `docs/soutenance.pptx` | **Toute l'équipe** | 🟡 À préparer en fin de sprint |

---

## 🔗 Dépendances entre Livrables

```
Quentin (priorisation.csv)
    └──► Léo (dashboard.py) ──► Soutenance
Sophie (recommandations.md) ──► Soutenance
Maé (agent-deploiement.md) ──► vérifie dashboard.py
Joanne (backlog + GEMINI.md) ──► cohésion globale ──► Soutenance
```

> ⚠️ **Point de synchronisation critique** : Léo (dashboard) dépend du format exact du fichier de Quentin (`priorisation.csv`). Se coordonner en début de sprint pour aligner les noms de colonnes.

---

## 📚 Ressources Sprint 4

| Ressource | Lien |
| :--- | :--- |
| Documentation Streamlit | https://docs.streamlit.io |
| Galerie d'exemples Streamlit | https://streamlit.io/gallery |
| WCAG — Accessibilité web | https://www.w3.org/WAI/WCAG21/quickref/ |
| Guide Orchestration d'agents IA | Discord #liens-outils |

---

## 🎙️ Rituels Scrum Sprint 4

| Rituel | Fréquence | Responsable | Où documenter |
| :--- | :--- | :--- | :--- |
| Daily Standup | Quotidien | Joanne | `docs/standups/AAAA-MM-JJ.md` |
| Sprint Review | Fin de sprint | Toute l'équipe | = Soutenance |
| Rétrospective finale | Après la soutenance (15 min) | Joanne | `docs/standups/retrospective-finale.md` |

---

*Document créé le 26/05/2026 — Sprint 4 smartEngine*
