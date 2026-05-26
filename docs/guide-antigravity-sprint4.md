# 🚀 Guide Antigravity CLI — Sprint 4 smartEngine

> **Principe :** Chaque membre ouvre Antigravity CLI dans le dossier `Projet smartEngine` et donne des prompts précis à l'IA pour générer ses livrables. L'IA génère, tu valides et tu pushes.

---

## 🔽 Étape 0 — Cloner le dépôt (à faire une seule fois)

> ⚠️ **Si tu n'as pas encore le projet sur ta machine**, commence par cloner le dépôt GitHub avant tout.

1. Ouvre un terminal et place-toi dans le dossier où tu veux mettre le projet :
   ```
   cd C:\Users\<ton-nom>\Desktop
   ```
2. Clone le dépôt :
   ```
   git clone https://github.com/Narkard/smartengine.git
   ```
3. Entre dans le dossier cloné :
   ```
   cd smartengine
   ```
4. Vérifie que tout est bien récupéré :
   ```
   git log --oneline -5
   ```

> ✅ Tu n'as à faire cette étape **qu'une seule fois**. Pour les jours suivants, tu fais juste un `git pull`.

---

## 📂 Avant tout — Setup commun (chaque jour)

**Chaque membre de l'équipe doit :**

1. Ouvrir un terminal dans le dossier du projet :
   ```
   cd "C:\Users\<ton-nom>\Desktop\smartengine"
   ```
2. Récupérer les dernières modifications de l'équipe :
   ```
   git pull origin main
   ```
3. Lancer Antigravity CLI :
   ```
   antigravity
   ```
4. Vérifier qu'on est bien sur `main` et à jour :
   ```
   git pull origin main
   ```

---

## 💻 Léo (Moi) — Dashboard Streamlit

**Livrable :** `src/dashboard.py` + `requirements.txt`

---

### Étape 1 — 🔄 Action manuelle : récupérer le travail de Quentin

Attendre que Quentin ait pushé `outputs/priorisation.csv` (le dashboard dépend de ce fichier).
Une fois qu'il a pushé, récupère son travail :

```
git pull origin main
```

Vérifie que le fichier est bien là :
```
ls outputs/priorisation.csv
```

---

### Étape 2 — 🤖 Prompt Antigravity : installer les dépendances

```
Vérifie que les librairies suivantes sont listées dans src/requirements.txt
(crée le fichier s'il n'existe pas) :
streamlit, pandas, plotly, shap, joblib, scikit-learn, matplotlib

Ensuite installe-les avec : pip install -r src/requirements.txt
```

---

### Étape 3 — 🤖 Prompt Antigravity : générer le dashboard

```
En te basant sur les fichiers outputs/scores.csv et outputs/priorisation.csv,
génère src/dashboard.py : une application Streamlit avec 3 vues.

Vue 1 — Portefeuille :
- KPIs en haut : nombre de comptes, taux de churn prédit (%), MRR total à risque
- Histogramme de distribution des churn_score
- Graphique camembert de répartition par quadrant

Vue 2 — Priorisation :
- Scatter plot interactif (axe X = churn_score, axe Y = MRR, couleur = quadrant)
- Tableau filtrable par quadrant, plan, fourchette de score et de MRR
- Colonnes affichées : account_id, churn_score, risk_level, MRR, quadrant, action_recommandee

Vue 3 — Fiche compte :
- Sélecteur de compte (dropdown sur account_id)
- Affiche le profil complet du compte (plan, ancienneté, usage, tickets)
- Jauge visuelle du score de churn (présentée de façon non technique)
- Quadrant et action recommandée mis en évidence avec une icône
- Graphique SHAP en barres horizontales :
  charger outputs/models/churn_model.joblib,
  calculer les valeurs SHAP pour ce compte,
  afficher les 5 facteurs qui augmentent ou diminuent son score

Contraintes :
- Palette de couleurs accessible aux daltoniens (orange/bleu, pas rouge/vert pur)
- Libellés texte sur tous les graphiques en plus de la couleur
- Exécutable avec : streamlit run src/dashboard.py
- Aucune dépendance à Gemini CLI
```

---

### Étape 4 — 🔄 Action manuelle : tester le dashboard localement

Lance le dashboard dans le terminal :
```
streamlit run src/dashboard.py
```

Vérifier que :
- [ ] La Vue 1 (Portefeuille) s'affiche avec les KPIs et les graphiques
- [ ] La Vue 2 (Priorisation) : les filtres fonctionnent, le scatter plot est interactif
- [ ] La Vue 3 (Fiche compte) : le dropdown permet de choisir un compte, le graphique SHAP s'affiche

---

### Étape 5 — 🤖 Prompt Antigravity (si bug) : corriger les erreurs

Si une erreur apparaît au lancement, copie-colle le message d'erreur dans Antigravity :
```
Le dashboard src/dashboard.py produit l'erreur suivante au lancement :
[coller ici le message d'erreur exact]
Identifie la cause et corrige le fichier.
```

---

### Étape 6 — 🔄 Action manuelle : push du dashboard

```
git add src/dashboard.py src/requirements.txt
git commit -m "feat: dashboard Streamlit Sprint 4 (3 vues + SHAP)"
git push origin main
```

---

### Étape 7 — 🤖 Prompt Antigravity : tâche de recherche

```
Dans le cadre du Sprint 4 du projet smartEngine, rédige une synthèse de recherche
à ajouter dans docs/dossier-conception.md (section 4.2 Dashboard). Documente :

1. Qu'est-ce que le data storytelling ? Comment structurer un dashboard pour
   raconter une histoire avec les données ? Quels sont les principes clés ?

2. Quels sont les principes d'accessibilité visuelle WCAG à respecter dans
   un dashboard ? Comment gérer le daltonisme dans les choix de couleurs ?
   Donne des exemples concrets (palettes, alternatives textuelles).

3. Comment présenter un score de probabilité (ex: 0.82 de churn) à un public
   non technique sans créer de fausses certitudes ? Quelles formulations utiliser ?
```

---

### Étape 8 — 🤖 Prompt Antigravity : rédiger la sous-section du dossier de conception

```
Rédige et ajoute la sous-section "4.2 Dashboard Streamlit" dans
docs/dossier-conception.md. Couvre :
- Choix des visualisations et justification (pourquoi scatter plot, pourquoi SHAP)
- Organisation narrative des 3 vues (portefeuille → priorisation → fiche compte)
- Gestion de l'accessibilité WCAG et du daltonisme (choix de palette, libellés)
- Retour d'expérience Streamlit (avantages, limites rencontrées)
- Comment l'agent de déploiement a été utilisé pour générer le code
```

---

### Étape 9 — 🔄 Action manuelle : push du dossier de conception

```
git add docs/dossier-conception.md
git commit -m "docs: section 4.2 dashboard - dossier de conception Sprint 4"
git push origin main
```

---

## 💻 Quentin — Fichier de priorisation

**Livrable :** `outputs/priorisation.csv`

> ⚠️ **À faire EN PREMIER** — Léo attend ce fichier pour le dashboard.

### Ordre des étapes

**Étape 1 — Générer le script de priorisation**

Prompt Antigravity :
```
Génère un script Python src/generate_priorisation.py qui :
1. Charge outputs/scores.csv (colonnes : account_id, churn_score, risk_level)
2. Charge data/processed/analytics.csv et en extrait le MRR par account_id
3. Fusionne les deux tables sur account_id
4. Calcule la médiane du MRR et crée une colonne value_level :
   - 'high' si MRR >= médiane
   - 'low' si MRR < médiane
5. Affecte un quadrant selon ces règles :
   - risk_level='High' ET value_level='high' → quadrant='Q1 - Priorité maximale'
   - risk_level='High' ET value_level='low'  → quadrant='Q2 - Action automatisée'
   - risk_level!='High' ET value_level='high' → quadrant='Q3 - Surveillance'
   - risk_level!='High' ET value_level='low'  → quadrant='Q4 - Aucune action'
6. Ajoute une colonne action_recommandee selon le quadrant
7. Exporte outputs/priorisation.csv avec les colonnes :
   account_id, churn_score, risk_level, MRR, value_level, quadrant, action_recommandee
8. Affiche un résumé : nombre de comptes par quadrant et médiane MRR utilisée
```

**Étape 2 — Exécuter le script**
```
python src/generate_priorisation.py
```

**Étape 3 — Vérifier le fichier produit**

Prompt Antigravity :
```
Vérifie que outputs/priorisation.csv est correct :
- Pas de valeurs manquantes
- Les 4 quadrants sont présents
- Les colonnes correspondent exactement à ce format :
  account_id, churn_score, risk_level, MRR, value_level, quadrant, action_recommandee
Affiche un aperçu des 5 premières lignes et le nombre de comptes par quadrant.
```

**Étape 4 — Push**
```
git add outputs/priorisation.csv src/generate_priorisation.py
git commit -m "feat: génération fichier priorisation Sprint 4 (4 quadrants)"
git push origin main
```

**Étape 5 — Rédiger ta partie du dossier de conception**

Prompt Antigravity :
```
Rédige la sous-section "Segmentation risque / valeur" de la section 4 du dossier
docs/dossier-conception.md. Couvre : définition MRR et CLV, justification de la
médiane comme seuil, pourquoi la matrice plutôt que le clustering K-Means,
Next Best Action par quadrant, lien avec l'article 22 du RGPD (humain dans la boucle).
```

---

## 💻 Maé — Agent de déploiement

**Livrable :** `.gemini/agents/agent-deploiement.md`

### Ordre des étapes

> Maé peut travailler **en parallèle** de Léo et Quentin.

**Étape 1 — Créer l'agent de déploiement**

Prompt Antigravity :
```
Crée le fichier .gemini/agents/agent-deploiement.md : un agent spécialisé
dans les tâches de déploiement du Sprint 4 de smartEngine.

L'agent doit être capable de :
- Générer src/dashboard.py à partir de outputs/scores.csv et outputs/priorisation.csv
- Vérifier la cohérence des fichiers de sortie (colonnes, types, valeurs manquantes)
- Générer et maintenir requirements.txt à jour
- Vérifier que tous les scripts sont autonomes (exécutables sans Gemini CLI)

Format du fichier : même structure que les agents existants dans .gemini/agents/
(frontmatter YAML avec name et description, puis sections Rôle, Étapes, Règles d'Or)

Règles d'Or à inclure :
- Autonomie : tous les scripts produits doivent fonctionner sans Gemini CLI
- Les scripts doivent utiliser des chemins relatifs
- Toujours vérifier les colonnes attendues avant de générer du code
```

**Étape 2 — Vérifier l'autonomie des scripts existants**

Prompt Antigravity :
```
Vérifie que src/dashboard.py (quand il existera) peut s'exécuter avec
"streamlit run src/dashboard.py" sans aucune dépendance à Gemini CLI.
Vérifie aussi que src/generate_priorisation.py s'exécute avec "python src/generate_priorisation.py".
Liste toutes les dépendances manquantes dans requirements.txt.
```

**Étape 3 — Rédiger le bilan des agents (dossier de conception)**

Prompt Antigravity :
```
Rédige la sous-section "Retour d'expérience sur les agents IA" de la section 4
du dossier docs/dossier-conception.md. Dresse le bilan sur les 4 sprints :
- Sprint 1 : data-explorer.md
- Sprint 2 : data-engineer.md
- Sprint 3 : model-trainer.md
- Sprint 4 : agent-deploiement.md

Pour chaque agent : rôle, points forts, limites, ce qui a nécessité une
intervention manuelle.
```

**Étape 4 — Rédiger les limites et perspectives (dossier de conception)**

Prompt Antigravity :
```
Rédige la sous-section "Limites et perspectives" de la section 4 du dossier
docs/dossier-conception.md. Couvre :
- Ce que le modèle Random Forest ne capture pas (sentiment des tickets, données externes)
- Biais identifié sur le secteur EdTech
- Améliorations possibles : NLP sur les tickets, données comportementales granulaires,
  réentraînement périodique (drift), survival analysis
```

**Étape 5 — Push**
```
git add .gemini/agents/agent-deploiement.md
git commit -m "feat: agent déploiement Sprint 4"
git push origin main
```

---

## 🎯 Sophie — Document de recommandations

**Livrable :** `outputs/recommandations.md`

> Sophie peut commencer dès que `outputs/priorisation.csv` est disponible
> (pour avoir les vrais chiffres par quadrant).

### Ordre des étapes

**Étape 1 — Générer le document de recommandations**

Prompt Antigravity :
```
Génère le fichier outputs/recommandations.md : un document de recommandations
stratégiques rédigé pour la direction de RavenStack (public non technique).

Utilise les données de outputs/scores.csv et outputs/priorisation.csv pour
illustrer avec de vrais chiffres.

Le document doit répondre à 4 questions :

1. Que dit le modèle ?
   - Taux de churn global prédit (% de comptes en High risk)
   - Profil type des comptes à risque (plan, ancienneté, usage)
   - Top 3 des facteurs de churn identifiés (usage_trend_30d, critical_ratio, etc.)
   - Rédigé en langage non technique, sans jargon ML

2. Quelles actions par quadrant ?
   - Q1 (risque élevé / valeur élevée) : appel CSM direct sous 24h
   - Q2 (risque élevé / valeur faible) : email automatisé de relance
   - Q3 (risque faible / valeur élevée) : fidélisation douce, ne pas sur-solliciter
   - Q4 (risque faible / valeur faible) : aucune action prioritaire

3. Quel ROI estimé ?
   - MRR actuellement à risque (somme du MRR des comptes High risk)
   - Estimation du MRR sauvé si on retient 40% des comptes Q1
   - Coût estimé des actions (temps CSM, coût des remises)
   - Calcul du ROI = (MRR sauvé − coût actions) / coût actions

4. Quelle feuille de route ?
   - Phase pilote 4 semaines : uniquement Q1
   - Mesure des résultats (groupe témoin, test A/B, uplift)
   - Élargissement progressif si résultats positifs

5. Protocole de mesure d'impact :
   - Définition du groupe témoin et du groupe traité
   - Méthode de calcul de l'uplift
   - KPI de suivi : taux de rétention, MRR sauvé, coût par compte retenu
```

**Étape 2 — Relire et ajuster**
> Vérifier que le document est compréhensible par quelqu'un sans connaissance en data science.

**Étape 3 — Rédiger sa partie du dossier de conception**

Prompt Antigravity :
```
Rédige la sous-section "Recommandations et mesure d'impact" de la section 4 du
dossier docs/dossier-conception.md. Couvre : méthode de calcul du ROI, protocole
de mesure d'impact (groupe témoin, test A/B, uplift), conduite du changement
(freins possibles des équipes métier, comment les accompagner).
```

**Étape 4 — Push**
```
git add outputs/recommandations.md
git commit -m "docs: recommandations stratégiques et protocole mesure d'impact"
git push origin main
```

---

## 🔁 Joanne — Scrum Master (Infrastructure & Coordination)

**Livrables :** Backlog + `GEMINI.md` + Standups + Section 4 (coordination)

### Ordre des étapes

**Étape 1 — Mettre à jour le backlog**

Prompt Antigravity :
```
Mets à jour docs/backlog.md pour le Sprint 4 :
1. Passe toutes les stories des Sprints 1, 2 et 3 en statut "✅ Done"
2. Ajoute les nouvelles user stories du Sprint 4 avec le tableau :
   | ID | En tant que... | Je veux... | Afin de... | État | Responsable |
   - US-S4-01 : Responsable CS / dashboard interactif / consulter sans coder → Léo
   - US-S4-02 : Directeur commercial / alerte compte VIP High risk / appel 24h → Léo
   - US-S4-03 : Direction RavenStack / recommandations + ROI / décider du budget → Sophie
   - US-S4-04 : Product Owner / support de soutenance / présenter au jury → Toute l'équipe
   - US-S4-05 : Développeur IA / fichier priorisation.csv / alimenter le dashboard → Quentin
   - US-S4-06 : Scrum Master / GEMINI.md complet / référence unique du projet → Joanne
```

**Étape 2 — Mettre à jour `GEMINI.md`**

Prompt Antigravity :
```
Mets à jour le fichier GEMINI.md à la racine du projet pour refléter l'état
complet après les 4 sprints :
- Section "Sprint en cours" : Sprint 4 - Déploiement
- Rôles du Sprint 4 : PO=Sophie, SM=Joanne, Devs IA=Léo/Quentin/Maé
- Ajouter la section Sprint 4 dans l'historique avec ses livrables
- Mettre à jour les conventions : ajouter les nouveaux fichiers
  (priorisation.csv, recommandations.md, dashboard.py, agent-deploiement.md)
- Ajouter les chemins vers les fichiers clés du projet complet
```

**Étape 3 — Documenter les standups quotidiens**

Chaque matin, prompt Antigravity :
```
Crée le fichier docs/standups/2026-MM-JJ.md pour le standup du jour.
Structure :
## Daily Standup — 2026-MM-JJ
### Léo : Hier / Aujourd'hui / Blocages
### Quentin : Hier / Aujourd'hui / Blocages
### Maé : Hier / Aujourd'hui / Blocages
### Sophie : Hier / Aujourd'hui / Blocages
```

**Étape 4 — Coordonner la Section 4 du dossier de conception**

Une fois que Léo, Quentin, Maé et Sophie ont chacun rédigé leur sous-section :

Prompt Antigravity :
```
Compile et harmonise la section 4 du dossier docs/dossier-conception.md
en intégrant les sous-sections rédigées par l'équipe :
- 4.1 Segmentation risque/valeur (Quentin)
- 4.2 Dashboard Streamlit (Léo)
- 4.3 Recommandations et mesure d'impact (Sophie)
- 4.4 Retour d'expérience sur les agents IA (Maé)
- 4.5 Limites et perspectives (Maé)

Assure la cohérence du style, ajoute une introduction à la section 4
et une conclusion générale du projet.
```

**Étape 5 — Structurer le support de soutenance**

Prompt Antigravity :
```
Génère un plan détaillé pour le support de soutenance docs/soutenance_plan.md.
Le plan doit couvrir les 4 sprints en environ 20 minutes :
- Introduction et contexte RavenStack (2 min) — Sophie
- Sprint 1-2 : Données et feature engineering (4 min) — Quentin
- Sprint 3 : Modélisation et évaluation (4 min) — Maé
- Sprint 4 : Dashboard et recommandations (5 min) — Léo
- ROI et feuille de route (3 min) — Sophie
- Bilan agents IA et retour d'expérience (2 min) — Maé
```

**Étape 6 — Push final de cohésion**
```
git add docs/backlog.md GEMINI.md docs/standups/ docs/dossier-conception.md
git commit -m "docs: mise à jour backlog, GEMINI.md et section 4 dossier conception Sprint 4"
git push origin main
```

---

## 📋 Ordre de travail recommandé (timeline)

```
JOUR 1
├── Joanne    → Backlog + GEMINI.md  (setup immédiat)
├── Quentin   → generate_priorisation.py + priorisation.csv  (PRIORITAIRE)
└── Maé       → agent-deploiement.md  (en parallèle)

JOUR 2
├── Léo       → dashboard.py  (dès que priorisation.csv est pushé)
└── Sophie    → recommandations.md  (dès que priorisation.csv est pushé)

JOUR 3
├── Tous      → Rédaction de sa sous-section du dossier de conception
└── Joanne    → Compilation et harmonisation Section 4

JOUR 4
└── Tous      → Support soutenance + répétitions
```

---

## ✅ Checklist finale avant soutenance

```
[ ] outputs/priorisation.csv  présent et valide
[ ] src/dashboard.py  fonctionne avec : streamlit run src/dashboard.py
[ ] outputs/recommandations.md  rédigé pour public non technique
[ ] docs/dossier-conception.md  contient les sections 1 à 4
[ ] .gemini/agents/agent-deploiement.md  créé
[ ] GEMINI.md  mis à jour (4 sprints)
[ ] docs/backlog.md  Sprint 4 complet
[ ] docs/soutenance.pptx  finalisé
[ ] git push origin main  (tout est sur GitHub)
```
