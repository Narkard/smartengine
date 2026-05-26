# 🚀 Guide Antigravity CLI — Sprint 4 smartEngine

> **Principe :** Ce guide est un workflow collaboratif chronologique. Chaque étape indique **qui** fait **quoi** et dans **quel ordre**. Les étapes sont interdépendantes : certains membres doivent attendre qu'une étape précédente soit terminée avant de commencer.

**Légende :**
- 🔄 **Action manuelle** — commande à taper soi-même dans le terminal
- 🤖 **Prompt Antigravity** — texte à donner à l'IA dans Antigravity CLI
- 🔴 **Bloquant** — les membres indiqués doivent attendre cette étape avant de continuer
- ✅ **Point de sync** — push sur GitHub, toute l'équipe peut `git pull`

---

## ÉTAPE 1 — Tous : cloner le dépôt (à faire une seule fois)

> ⚠️ **Chaque membre qui n'a pas encore le projet sur sa machine commence ici.**

**🔄 Action manuelle :**
```
git clone https://github.com/Narkard/smartengine.git
cd smartengine
```

Puis chaque jour, avant de travailler :
```
git pull origin main
```

Lancer Antigravity CLI depuis le dossier du projet :
```
antigravity
```

---

## ÉTAPE 2 — Joanne : setup du backlog Sprint 4

> Joanne démarre en tout premier pour que l'équipe ait un backlog clair dès le départ.

**🤖 Prompt Antigravity (Joanne) :**
```
Mets à jour docs/backlog.md pour le Sprint 4 :
1. Passe toutes les stories des Sprints 1, 2 et 3 en statut "✅ Done"
2. Ajoute les nouvelles user stories du Sprint 4 :
   | ID       | En tant que...          | Je veux...                        | Afin de...                            | État       | Responsable |
   | US-S4-01 | Responsable CS          | Un dashboard interactif           | Consulter les comptes à risque        | 🔲 To Do  | Léo         |
   | US-S4-02 | Directeur commercial    | Une alerte compte VIP High risk   | Déclencher un appel sous 24h          | 🔲 To Do  | Léo         |
   | US-S4-03 | Direction RavenStack    | Recommandations + ROI estimé      | Décider du budget rétention           | 🔲 To Do  | Sophie      |
   | US-S4-04 | Product Owner           | Un support de soutenance          | Présenter au jury                     | 🔲 To Do  | Tous        |
   | US-S4-05 | Développeur IA          | Le fichier priorisation.csv       | Alimenter le dashboard                | 🔲 To Do  | Quentin     |
   | US-S4-06 | Scrum Master            | Un GEMINI.md complet              | Avoir une référence unique du projet  | 🔲 To Do  | Joanne      |
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/backlog.md
git commit -m "docs: backlog Sprint 4 mis à jour"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 3 — Joanne & Maé : setup de l'infrastructure (en parallèle)

> Ces deux tâches peuvent être faites en même temps, elles ne dépendent pas l'une de l'autre.

### Joanne : mise à jour du GEMINI.md

**🤖 Prompt Antigravity (Joanne) :**
```
Mets à jour le fichier GEMINI.md à la racine du projet pour refléter
l'état complet après les 4 sprints :
- Section "Sprint en cours" → Sprint 4 - Déploiement
- Rôles du Sprint 4 : PO=Sophie, SM=Joanne, Devs IA=Léo/Quentin/Maé
- Ajouter la section Sprint 4 dans l'historique avec ses livrables attendus :
  priorisation.csv, dashboard.py, recommandations.md, agent-deploiement.md
- Mettre à jour les conventions de nommage avec les nouveaux fichiers du Sprint 4
- Ajouter les chemins vers tous les fichiers clés du projet complet
```

**🔄 Action manuelle (Joanne) :**
```
git add GEMINI.md
git commit -m "docs: GEMINI.md mis à jour Sprint 4"
git push origin main
```

---

### Maé : création de l'agent de déploiement

**🤖 Prompt Antigravity (Maé) :**
```
Crée le fichier .gemini/agents/agent-deploiement.md : un agent spécialisé
dans les tâches de déploiement du Sprint 4 de smartEngine.

L'agent doit être capable de :
- Générer src/dashboard.py à partir de outputs/scores.csv et outputs/priorisation.csv
- Vérifier la cohérence des fichiers de sortie (colonnes, types, valeurs manquantes)
- Générer et maintenir src/requirements.txt à jour
- Vérifier que tous les scripts sont autonomes (exécutables sans Gemini CLI)

Format : même structure que les agents existants dans .gemini/agents/
(frontmatter YAML : name + description, puis Rôle, Étapes de traitement, Règles d'Or)

Règles d'Or :
- Autonomie : tous les scripts produits doivent fonctionner sans Gemini CLI
- Utiliser des chemins relatifs dans tous les scripts
- Toujours vérifier les colonnes attendues avant de générer du code
```

**🔄 Action manuelle (Maé) :**
```
git add .gemini/agents/agent-deploiement.md
git commit -m "feat: agent déploiement Sprint 4"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 4 — Quentin : génération du fichier de priorisation

> 🔴 **BLOQUANT pour Léo et Sophie** — ils ne peuvent pas commencer leurs livrables sans ce fichier.

### Étape 4a — Générer le script

**🤖 Prompt Antigravity (Quentin) :**
```
Génère un script Python src/generate_priorisation.py qui :
1. Charge outputs/scores.csv (colonnes : account_id, churn_score, risk_level)
2. Charge data/processed/analytics.csv et en extrait le MRR par account_id
3. Fusionne les deux tables sur account_id
4. Calcule la médiane du MRR et crée une colonne value_level :
   - 'high' si MRR >= médiane
   - 'low'  si MRR < médiane
5. Affecte un quadrant selon ces règles :
   - risk_level='High' ET value_level='high' → 'Q1 - Priorité maximale'
   - risk_level='High' ET value_level='low'  → 'Q2 - Action automatisée'
   - risk_level!='High' ET value_level='high' → 'Q3 - Surveillance'
   - risk_level!='High' ET value_level='low'  → 'Q4 - Aucune action'
6. Ajoute une colonne action_recommandee selon le quadrant :
   - Q1 → 'Appel CSM direct sous 24h'
   - Q2 → 'Email automatisé de relance'
   - Q3 → 'Fidélisation douce, surveillance'
   - Q4 → 'Aucune action prioritaire'
7. Exporte outputs/priorisation.csv avec les colonnes :
   account_id, churn_score, risk_level, MRR, value_level, quadrant, action_recommandee
8. Affiche un résumé : médiane MRR utilisée + nombre de comptes par quadrant
```

### Étape 4b — Exécuter le script

**🔄 Action manuelle (Quentin) :**
```
python src/generate_priorisation.py
```

### Étape 4c — Vérifier le fichier produit

**🤖 Prompt Antigravity (Quentin) :**
```
Vérifie que outputs/priorisation.csv est correct :
- Pas de valeurs manquantes
- Les 4 quadrants sont présents (Q1, Q2, Q3, Q4)
- Les colonnes sont exactement : account_id, churn_score, risk_level, MRR, value_level, quadrant, action_recommandee
Affiche les 5 premières lignes et le nombre de comptes par quadrant.
```

### Étape 4d — Push

**🔄 Action manuelle (Quentin) :**
```
git add outputs/priorisation.csv src/generate_priorisation.py
git commit -m "feat: fichier priorisation Sprint 4 - 4 quadrants risque/valeur"
git push origin main
```

✅ **Point de sync — Léo et Sophie font `git pull origin main` et peuvent démarrer**

---

## ÉTAPE 5 — Léo & Sophie : démarrage en parallèle (après `git pull`)

> 🔴 Ces deux tâches démarrent **uniquement après l'ÉTAPE 4**.
> Léo et Sophie font d'abord `git pull origin main` pour récupérer `priorisation.csv`.

### Léo : génération du dashboard Streamlit

#### Étape 5a — Installer les dépendances

**🤖 Prompt Antigravity (Léo) :**
```
Crée ou mets à jour src/requirements.txt avec les dépendances suivantes :
streamlit, pandas, plotly, shap, joblib, scikit-learn, matplotlib

Puis installe-les avec : pip install -r src/requirements.txt
```

#### Étape 5b — Générer le dashboard

**🤖 Prompt Antigravity (Léo) :**
```
En te basant sur outputs/scores.csv et outputs/priorisation.csv,
génère src/dashboard.py : une application Streamlit avec 3 vues.

Vue 1 — Portefeuille :
- KPIs : nombre de comptes, taux de churn prédit (%), MRR total à risque
- Histogramme de distribution des churn_score
- Camembert de répartition par quadrant

Vue 2 — Priorisation :
- Scatter plot interactif (X = churn_score, Y = MRR, couleur = quadrant)
- Tableau filtrable par quadrant, plan, fourchette de score et de MRR
- Colonnes : account_id, churn_score, risk_level, MRR, quadrant, action_recommandee

Vue 3 — Fiche compte :
- Dropdown de sélection d'un compte (account_id)
- Profil complet : plan, ancienneté, usage, tickets
- Jauge visuelle du score (formulée de façon non technique)
- Quadrant et action recommandée mis en évidence avec une icône
- Graphique SHAP : charger outputs/models/churn_model.joblib,
  calculer les valeurs SHAP, afficher les 5 facteurs principaux en barres horizontales

Contraintes :
- Palette daltonisme-friendly (orange/bleu, pas rouge/vert pur)
- Libellés texte sur tous les graphiques, pas uniquement la couleur
- Exécutable avec : streamlit run src/dashboard.py
- Aucune dépendance à Gemini CLI
```

#### Étape 5c — Tester le dashboard

**🔄 Action manuelle (Léo) :**
```
streamlit run src/dashboard.py
```

Vérifier :
- [ ] Vue 1 : KPIs + graphiques affichés
- [ ] Vue 2 : filtres fonctionnels, scatter plot interactif
- [ ] Vue 3 : dropdown de compte, graphique SHAP affiché

#### Étape 5d — Corriger si erreur

**🤖 Prompt Antigravity (Léo) — si bug :**
```
Le dashboard src/dashboard.py produit l'erreur suivante :
[coller le message d'erreur exact]
Identifie la cause et corrige le fichier.
```

#### Étape 5e — Push du dashboard

**🔄 Action manuelle (Léo) :**
```
git add src/dashboard.py src/requirements.txt
git commit -m "feat: dashboard Streamlit Sprint 4 (3 vues + SHAP)"
git push origin main
```

---

### Sophie : document de recommandations

#### Étape 5f — Générer les recommandations

**🤖 Prompt Antigravity (Sophie) :**
```
Génère outputs/recommandations.md : un document stratégique rédigé pour
la direction de RavenStack (public non technique, sans jargon ML).

Utilise les vrais chiffres de outputs/scores.csv et outputs/priorisation.csv.

Le document répond à 4 questions :

1. Que dit le modèle ?
   - Taux de churn global prédit (% de comptes en High risk)
   - Profil type des comptes à risque (plan, ancienneté, usage)
   - Top 3 des facteurs de churn (usage_trend_30d, critical_ratio, etc.)

2. Quelles actions par quadrant ?
   - Q1 (risque élevé / valeur élevée) : appel CSM direct sous 24h + proposition commerciale
   - Q2 (risque élevé / valeur faible) : email automatisé de relance
   - Q3 (risque faible / valeur élevée) : fidélisation douce, ne pas sur-solliciter
   - Q4 (risque faible / valeur faible) : aucune action prioritaire

3. Quel ROI estimé ?
   - MRR actuellement à risque = somme du MRR des comptes Q1 + Q2
   - MRR sauvé estimé si on retient 40% des comptes Q1
   - Coût estimé des actions (temps CSM, remises éventuelles)
   - ROI = (MRR sauvé − coût actions) / coût actions

4. Quelle feuille de route ?
   - Phase pilote 4 semaines : Q1 uniquement
   - Protocole de mesure : groupe témoin + groupe traité
   - Test A/B : comparer les taux de rétention après 4 semaines
   - Uplift = différence de rétention entre groupe traité et groupe témoin
   - KPI : taux de rétention, MRR sauvé, coût par compte retenu
   - Élargissement aux autres quadrants si résultats positifs
```

#### Étape 5g — Relire et ajuster

**🔄 Action manuelle (Sophie) :**
Relire le document et vérifier qu'il est compréhensible par quelqu'un sans connaissance en data science. Corriger le jargon technique si besoin.

#### Étape 5h — Push des recommandations

**🔄 Action manuelle (Sophie) :**
```
git add outputs/recommandations.md
git commit -m "docs: recommandations stratégiques Sprint 4 + protocole mesure d'impact"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 6 — Tous : rédaction du dossier de conception (Section 4)

> Chaque membre rédige **sa propre sous-section** dans `docs/dossier-conception.md`.
> Joanne compile ensuite toutes les contributions.

### Quentin — sous-section 4.1 Segmentation risque/valeur

**🤖 Prompt Antigravity (Quentin) :**
```
Rédige et ajoute la sous-section "4.1 Segmentation risque / valeur" dans
docs/dossier-conception.md. Couvre :
- Définition du MRR et de la CLV (Customer Lifetime Value)
- Justification du choix de la médiane du MRR comme seuil de découpage
- Pourquoi la matrice risque/valeur plutôt que le clustering K-Means
- Next Best Action définie pour chaque quadrant
- Lien avec l'article 22 du RGPD : pourquoi un score seul ne doit jamais
  déclencher une action automatique (humain dans la boucle)
```

**🔄 Action manuelle (Quentin) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.1 segmentation risque/valeur - dossier conception"
git push origin main
```

---

### Léo — sous-section 4.2 Dashboard Streamlit

**🤖 Prompt Antigravity (Léo) :**
```
Rédige et ajoute la sous-section "4.2 Dashboard Streamlit" dans
docs/dossier-conception.md. Couvre :
- Choix des visualisations et justification (scatter plot, SHAP, jauge)
- Organisation narrative des 3 vues (portefeuille → priorisation → fiche compte)
- Gestion de l'accessibilité WCAG : palette daltonisme-friendly, libellés texte
- Comment présenter un score de probabilité à un public non technique
- Retour d'expérience Streamlit (avantages, limites rencontrées)
- Comment l'agent de déploiement a été utilisé pour générer le code
```

**🔄 Action manuelle (Léo) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.2 dashboard - dossier conception"
git push origin main
```

---

### Sophie — sous-section 4.3 Recommandations et mesure d'impact

**🤖 Prompt Antigravity (Sophie) :**
```
Rédige et ajoute la sous-section "4.3 Recommandations et mesure d'impact" dans
docs/dossier-conception.md. Couvre :
- Méthode de calcul du ROI (formule, hypothèses, chiffres utilisés)
- Protocole de mesure d'impact : groupe témoin, test A/B, calcul de l'uplift
- Pourquoi le groupe témoin est indispensable (on ne sait pas si les comptes
  seraient restés sans intervention)
- Conduite du changement : freins possibles des équipes métier et comment
  les accompagner dans l'adoption de l'outil
- KPI de suivi post-déploiement
```

**🔄 Action manuelle (Sophie) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.3 recommandations et mesure d'impact - dossier conception"
git push origin main
```

---

### Maé — sous-sections 4.4 et 4.5

**🤖 Prompt Antigravity (Maé) — Bilan des agents :**
```
Rédige et ajoute la sous-section "4.4 Retour d'expérience sur les agents IA"
dans docs/dossier-conception.md. Dresse le bilan sur les 4 sprints :
- Sprint 1 : data-explorer.md — rôle, points forts, limites, interventions manuelles
- Sprint 2 : data-engineer.md — rôle, points forts, limites, interventions manuelles
- Sprint 3 : model-trainer.md — rôle, points forts, limites, interventions manuelles
- Sprint 4 : agent-deploiement.md — rôle, points forts, limites, interventions manuelles
Conclure : qu'est-ce qui a bien fonctionné ? Qu'est-ce qui aurait nécessité plus de contrôle ?
```

**🤖 Prompt Antigravity (Maé) — Limites et perspectives :**
```
Rédige et ajoute la sous-section "4.5 Limites et perspectives" dans
docs/dossier-conception.md. Couvre :
- Ce que le modèle Random Forest ne capture pas (sentiment des tickets, données externes)
- Biais identifié sur le secteur EdTech (modèle plus sévère sur ce secteur)
- Améliorations possibles avec plus de temps ou de données :
  → Analyse NLP des textes de tickets support
  → Données comportementales plus granulaires (sessions, features utilisées)
  → Réentraînement périodique pour éviter le drift du modèle
  → Survival analysis pour modéliser le temps avant le churn
```

**🔄 Action manuelle (Maé) :**
```
git add docs/dossier-conception.md
git commit -m "docs: sections 4.4 bilan agents + 4.5 limites perspectives - dossier conception"
git push origin main
```

✅ **Point de sync — Joanne fait `git pull origin main` et compile la Section 4**

---

## ÉTAPE 7 — Joanne : compilation et harmonisation de la Section 4

**🤖 Prompt Antigravity (Joanne) :**
```
Compile et harmonise la section 4 du dossier docs/dossier-conception.md.
Les sous-sections ont été rédigées individuellement par les membres de l'équipe.
Vérifie la cohérence du style et de la mise en forme sur l'ensemble du document.
Ajoute :
- Une introduction à la section 4 (présentation des 3 axes du Sprint 4)
- Une conclusion générale du projet (bilan des 4 sprints, apports du système)
Assure-toi que le dossier complet couvre bien les sections 1, 2, 3 et 4.
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/dossier-conception.md
git commit -m "docs: compilation et harmonisation section 4 - dossier conception final"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 8 — Joanne : plan de soutenance

**🤖 Prompt Antigravity (Joanne) :**
```
Génère un plan détaillé pour le support de soutenance dans docs/soutenance_plan.md.
Le plan doit couvrir les 4 sprints en environ 20 minutes :
- Introduction et contexte RavenStack (2 min) — Sophie
- Sprint 1-2 : Données et feature engineering (4 min) — Quentin
- Sprint 3 : Modélisation et évaluation (4 min) — Maé
- Sprint 4 : Dashboard et recommandations en live (5 min) — Léo
- ROI et feuille de route (3 min) — Sophie
- Bilan agents IA et retour d'expérience (2 min) — Maé
Inclure pour chaque partie : slides suggérées, points clés à mentionner,
éléments visuels à montrer (graphiques, extraits de code, captures du dashboard).
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/soutenance_plan.md
git commit -m "docs: plan soutenance Sprint 4"
git push origin main
```

---

## ÉTAPE 9 — Maé : vérification finale de l'autonomie des scripts

> Avant la livraison, Maé vérifie que tout fonctionne sans Gemini CLI.

**🤖 Prompt Antigravity (Maé) :**
```
Vérifie que les scripts suivants sont totalement autonomes (sans Gemini CLI) :
- src/generate_priorisation.py → doit s'exécuter avec : python src/generate_priorisation.py
- src/dashboard.py → doit s'exécuter avec : streamlit run src/dashboard.py
Vérifie que src/requirements.txt liste toutes les dépendances nécessaires.
Liste tout ce qui est manquant ou cassé.
```

**🔄 Action manuelle (Maé) :**
Si des corrections sont nécessaires, les faire puis :
```
git add src/
git commit -m "fix: autonomie scripts vérifiée - aucune dépendance Gemini CLI"
git push origin main
```

---

## ÉTAPE 10 — Joanne : standup quotidien (chaque matin)

**🤖 Prompt Antigravity (Joanne) — chaque matin :**
```
Crée le fichier docs/standups/2026-MM-JJ.md pour le standup du jour.
Structure :
## Daily Standup — 2026-MM-JJ
### Léo : Hier / Aujourd'hui / Blocages
### Quentin : Hier / Aujourd'hui / Blocages
### Maé : Hier / Aujourd'hui / Blocages
### Sophie : Hier / Aujourd'hui / Blocages
### Joanne : Hier / Aujourd'hui / Blocages
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/standups/
git commit -m "docs: standup 2026-MM-JJ"
git push origin main
```

---

## ✅ Checklist finale avant soutenance

```
[ ] outputs/priorisation.csv        → Quentin (ÉTAPE 4)
[ ] src/dashboard.py                → Léo     (ÉTAPE 5)
[ ] src/requirements.txt            → Léo     (ÉTAPE 5)
[ ] outputs/recommandations.md      → Sophie  (ÉTAPE 5)
[ ] .gemini/agents/agent-deploiement.md → Maé (ÉTAPE 3)
[ ] GEMINI.md mis à jour            → Joanne  (ÉTAPE 3)
[ ] docs/backlog.md Sprint 4        → Joanne  (ÉTAPE 2)
[ ] docs/dossier-conception.md S4   → Tous    (ÉTAPE 6 + 7)
[ ] docs/soutenance_plan.md         → Joanne  (ÉTAPE 8)
[ ] Scripts autonomes vérifiés      → Maé     (ÉTAPE 9)
[ ] Tout est pushé sur GitHub       → Tous
```

---

## 📊 Vue d'ensemble du workflow

```
ÉTAPE 1  → Tous        : git clone + setup Antigravity
ÉTAPE 2  → Joanne      : Backlog Sprint 4
ÉTAPE 3  → Joanne      : GEMINI.md            ┐ en parallèle
           Maé         : Agent déploiement     ┘
ÉTAPE 4  → Quentin     : priorisation.csv  ← 🔴 BLOQUANT pour Léo et Sophie
ÉTAPE 5  → Léo         : dashboard.py          ┐ en parallèle
           Sophie      : recommandations.md    ┘ (après git pull étape 4)
ÉTAPE 6  → Tous        : sections dossier conception (en parallèle)
ÉTAPE 7  → Joanne      : compilation Section 4
ÉTAPE 8  → Joanne      : plan soutenance
ÉTAPE 9  → Maé         : vérification autonomie scripts
ÉTAPE 10 → Joanne      : standups quotidiens (tout au long du sprint)
```
