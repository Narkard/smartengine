# 🚀 Guide Antigravity CLI — Sprint 4 smartEngine

> **Principe :** Ce guide est un workflow collaboratif chronologique. À chaque étape, on donne à Antigravity un **prompt d'amorce court**. Antigravity va alors **poser des questions** pour comprendre le contexte avant d'agir. Il faut répondre à ces questions pour qu'il génère un résultat adapté.

**Légende :**
- 🔄 **Action manuelle** — commande à taper soi-même dans le terminal
- 💬 **Prompt d'amorce** — texte court à donner à Antigravity pour démarrer la conversation
- 🔴 **Bloquant** — les membres indiqués doivent attendre cette étape avant de continuer
- ✅ **Point de sync** — push sur GitHub, toute l'équipe fait `git pull`

---

## ÉTAPE 1 — Tous : cloner le dépôt (à faire une seule fois)

> ⚠️ Si tu n'as pas encore le projet sur ta machine, commence ici.

**🔄 Action manuelle :**
```
git clone https://github.com/Narkard/smartengine.git
cd smartengine
```

Puis **chaque jour**, avant de travailler :
```
git pull origin main
antigravity
```

---

## ÉTAPE 2 — Joanne : setup du backlog Sprint 4

**💬 Prompt d'amorce (Joanne → Antigravity) :**
```
Je suis Scrum Master sur le projet smartEngine Sprint 4.
Je dois mettre à jour le backlog dans docs/backlog.md.
Pose-moi les questions nécessaires avant de commencer.
```

> Antigravity va demander : quelles stories du Sprint 3 passer en Done ? Quels membres pour les nouvelles stories ? etc.
> Réponds à ses questions, il génère le backlog mis à jour.

**🔄 Action manuelle (Joanne) :**
```
git add docs/backlog.md
git commit -m "docs: backlog Sprint 4 mis à jour"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 3 — Joanne & Maé : infrastructure (en parallèle)

### Joanne : mise à jour du GEMINI.md

**💬 Prompt d'amorce (Joanne → Antigravity) :**
```
Je dois mettre à jour le fichier GEMINI.md à la racine du projet.
On vient de terminer le Sprint 3 et on commence le Sprint 4.
Pose-moi les questions nécessaires pour le mettre à jour correctement.
```

> Antigravity va demander : qui sont les membres du Sprint 4 ? Quels sont les nouveaux livrables ? Quelles conventions changer ?
> Réponds à ses questions, il met à jour le fichier.

**🔄 Action manuelle (Joanne) :**
```
git add GEMINI.md
git commit -m "docs: GEMINI.md mis à jour Sprint 4"
git push origin main
```

---

### Maé : création de l'agent de déploiement

**💬 Prompt d'amorce (Maé → Antigravity) :**
```
Je dois créer un nouvel agent IA pour le Sprint 4 du projet smartEngine.
Cet agent sera dédié aux tâches de déploiement.
Regarde les agents existants dans .gemini/agents/ pour comprendre le format,
puis pose-moi les questions nécessaires avant de le créer.
```

> Antigravity va demander : enrichir un agent existant ou en créer un nouveau ? Quelles tâches spécifiques doit-il couvrir ? Quelles contraintes (autonomie, chemins relatifs...) ?
> Réponds à ses questions, il génère l'agent.

**🔄 Action manuelle (Maé) :**
```
git add .gemini/agents/agent-deploiement.md
git commit -m "feat: agent déploiement Sprint 4"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 4 — Quentin : fichier de priorisation

> 🔴 **BLOQUANT pour Léo et Sophie** — ne pas sauter cette étape.

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

### Étape 4b — Exécuter et vérifier

**🔄 Action manuelle (Quentin) :**
```
python src/generate_priorisation.py
```

**🤖 Prompt Antigravity (Quentin) :**
```
Le script vient de générer outputs/priorisation.csv.
Vérifie que le fichier est correct :
- Pas de valeurs manquantes
- Les 4 quadrants sont présents
- Affiche les 5 premières lignes et la répartition par quadrant
```

### Étape 4c — Push

**🔄 Action manuelle (Quentin) :**
```
git add outputs/priorisation.csv src/generate_priorisation.py
git commit -m "feat: fichier priorisation Sprint 4 - 4 quadrants risque/valeur"
git push origin main
```

✅ **Point de sync — Léo et Sophie font `git pull origin main` et peuvent démarrer**

---

## ÉTAPE 5 — Léo & Sophie : livrables principaux (en parallèle)

> 🔴 Démarrer **uniquement après l'ÉTAPE 4**.
> Faire d'abord : `git pull origin main`

### Léo : dashboard Streamlit

#### Étape 5a — Installer les dépendances

**🤖 Prompt Antigravity (Léo) :**
```
Crée ou mets à jour src/requirements.txt avec les dépendances suivantes :
streamlit, pandas, plotly, shap, joblib, scikit-learn, matplotlib

Puis donne-moi la commande pour les installer.
```

**🔄 Action manuelle (Léo) :**
```
pip install -r src/requirements.txt
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
- Graphique SHAP : charger outputs/models/churn_model.joblib, calculer les valeurs SHAP, afficher les 5 facteurs principaux

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
Le dashboard src/dashboard.py produit l'erreur suivante au lancement :
[coller le message d'erreur exact]
Identifie la cause et corrige le fichier.
```

#### Étape 5e — Push

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

Le document doit répondre à 4 questions :
1. Que dit le modèle ? (Taux de churn global, profil type, top 3 facteurs)
2. Quelles actions par quadrant ? (Détailler les 4 quadrants)
3. Quel ROI estimé ? (Calculer le MRR sauvé si on retient 40% des comptes Q1)
4. Quelle feuille de route ? (Phase pilote 4 semaines, protocole de test A/B)
```

#### Étape 5g — Relire et ajuster

**🔄 Action manuelle (Sophie) :**
Relire le document. Si des passages sont trop techniques :

**🤖 Prompt Antigravity (Sophie) :**
```
Ce passage du document de recommandations est trop technique pour la direction :
[coller le passage]
Reformule-le en langage métier, sans jargon data science.
```

#### Étape 5h — Push

**🔄 Action manuelle (Sophie) :**
```
git add outputs/recommandations.md
git commit -m "docs: recommandations stratégiques Sprint 4 + protocole mesure d'impact"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 6 — Tous : dossier de conception Section 4 (en parallèle)

> Chaque membre rédige sa sous-section. Joanne compile ensuite.

### Quentin — sous-section 4.1

**🤖 Prompt Antigravity (Quentin) :**
```
Rédige et ajoute la sous-section "4.1 Segmentation risque / valeur" dans
docs/dossier-conception.md. Couvre :
- Définition du MRR et de la CLV
- Justification du choix de la médiane du MRR comme seuil
- Pourquoi la matrice risque/valeur plutôt que K-Means
- Lien avec l'article 22 du RGPD (pourquoi un humain doit rester dans la boucle)
```

**🔄 Action manuelle (Quentin) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.1 segmentation risque/valeur"
git push origin main
```

---

### Léo — sous-section 4.2

**🤖 Prompt Antigravity (Léo) :**
```
Rédige et ajoute la sous-section "4.2 Dashboard Streamlit" dans
docs/dossier-conception.md. Couvre :
- Choix des visualisations (scatter plot, SHAP, jauge)
- Organisation narrative des 3 vues
- Gestion de l'accessibilité WCAG (palette daltonisme-friendly)
- Comment présenter un score à un public non technique
- Comment l'agent de déploiement a été utilisé
```

**🔄 Action manuelle (Léo) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.2 dashboard Streamlit"
git push origin main
```

---

### Sophie — sous-section 4.3

**🤖 Prompt Antigravity (Sophie) :**
```
Rédige et ajoute la sous-section "4.3 Recommandations et mesure d'impact" dans
docs/dossier-conception.md. Couvre :
- Méthode de calcul du ROI estimé
- Protocole de mesure d'impact (groupe témoin, test A/B, uplift)
- Conduite du changement (freins possibles et solutions)
```

**🔄 Action manuelle (Sophie) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.3 recommandations et mesure d'impact"
git push origin main
```

---

### Maé — sous-sections 4.4 et 4.5

**🤖 Prompt Antigravity (Maé) :**
```
Rédige et ajoute les sous-sections 4.4 et 4.5 dans docs/dossier-conception.md :
- 4.4 : Retour d'expérience sur les agents IA (bilan des 4 agents utilisés sur les 4 sprints : points forts, limites, interventions manuelles)
- 4.5 : Limites et perspectives du modèle (ce que le modèle ne capture pas, améliorations possibles)
```

**🔄 Action manuelle (Maé) :**
```
git add docs/dossier-conception.md
git commit -m "docs: sections 4.4 bilan agents + 4.5 limites perspectives"
git push origin main
```

✅ **Point de sync — Joanne fait `git pull origin main`**

---

## ÉTAPE 7 — Joanne : compilation de la Section 4

**🤖 Prompt Antigravity (Joanne) :**
```
Compile et harmonise la section 4 complète dans docs/dossier-conception.md.
Vérifie la cohérence de la mise en forme.
Ajoute :
- Une introduction à la section 4
- Une conclusion générale du projet
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4 harmonisée - dossier conception final"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 8 — Joanne : plan de soutenance

**🤖 Prompt Antigravity (Joanne) :**
```
Génère un plan détaillé pour la soutenance (20 minutes) dans docs/soutenance_plan.md.
Répartition :
- Introduction et contexte (2 min) — Sophie
- Données et feature engineering (4 min) — Quentin
- Modélisation et évaluation (4 min) — Maé
- Dashboard et démo live (5 min) — Léo
- ROI et feuille de route (3 min) — Sophie
- Bilan agents IA (2 min) — Maé
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/soutenance_plan.md
git commit -m "docs: plan soutenance Sprint 4"
git push origin main
```

---

## ÉTAPE 9 — Maé : vérification finale de l'autonomie

**🤖 Prompt Antigravity (Maé) :**
```
Vérifie que tous les scripts de production (src/generate_priorisation.py, src/dashboard.py)
fonctionnent de manière totalement autonome sans Gemini CLI.
Vérifie que src/requirements.txt est complet.
Liste ce qui doit être corrigé si besoin.
```

**🔄 Action manuelle (Maé) :**
Si des corrections sont nécessaires :
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
Structure : Hier / Aujourd'hui / Blocages pour chaque membre (Léo, Quentin, Maé, Sophie, Joanne).
```

**🔄 Action manuelle (Joanne) :**
```
git add docs/standups/
git commit -m "docs: standup [date]"
git push origin main
```

---

## 📊 Vue d'ensemble du workflow

```
ÉTAPE 1  → Tous        : git clone + setup Antigravity
ÉTAPE 2  → Joanne      : Backlog Sprint 4
ÉTAPE 3  → Joanne + Maé: GEMINI.md + Agent déploiement (en parallèle)
ÉTAPE 4  → Quentin     : priorisation.csv  ← 🔴 BLOQUANT pour Léo et Sophie
ÉTAPE 5  → Léo + Sophie: dashboard + recommandations (en parallèle, après git pull)
ÉTAPE 6  → Tous        : dossier de conception Section 4 (en parallèle)
ÉTAPE 7  → Joanne      : compilation Section 4
ÉTAPE 8  → Joanne      : plan soutenance
ÉTAPE 9  → Maé         : vérification autonomie scripts
ÉTAPE 10 → Joanne      : standups quotidiens (tout au long du sprint)
```

---

## ✅ Checklist finale avant soutenance

```
[ ] outputs/priorisation.csv            → Quentin (ÉTAPE 4)
[ ] src/dashboard.py                    → Léo     (ÉTAPE 5)
[ ] src/requirements.txt                → Léo     (ÉTAPE 5)
[ ] outputs/recommandations.md          → Sophie  (ÉTAPE 5)
[ ] .gemini/agents/deployment-manager.md → Maé     (ÉTAPE 3)
[ ] GEMINI.md mis à jour                → Joanne  (ÉTAPE 3)
[ ] docs/backlog.md Sprint 4 complet    → Joanne  (ÉTAPE 2)
[ ] docs/dossier-conception.md S4       → Tous    (ÉTAPES 6 + 7)
[ ] docs/soutenance_plan.md             → Joanne  (ÉTAPE 8)
[ ] Scripts autonomes vérifiés          → Maé     (ÉTAPE 9)
[ ] Tout est pushé sur GitHub           → Tous
```
