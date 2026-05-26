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

**💬 Prompt d'amorce (Quentin → Antigravity) :**
```
Je dois créer un script Python qui génère un fichier de priorisation des clients
à risque de churn pour le projet smartEngine.
Les données sources sont outputs/scores.csv et data/processed/analytics.csv.
Pose-moi les questions nécessaires avant de commencer.
```

> Antigravity va demander : quelles colonnes sont disponibles ? Comment définir la valeur d'un compte ? Quel seuil utiliser pour séparer valeur haute et basse ? Quelle structure pour le CSV final ?
> Réponds à ses questions en donnant les détails du projet.

### Étape 4b — Exécuter et vérifier

**🔄 Action manuelle (Quentin) :**
```
python src/generate_priorisation.py
```

**💬 Prompt d'amorce (Quentin → Antigravity) :**
```
Le script vient de générer outputs/priorisation.csv.
Peux-tu vérifier que le fichier est correct et me donner un résumé ?
```

> Antigravity va analyser le fichier et signaler s'il y a des problèmes (valeurs manquantes, quadrants absents, mauvaises colonnes).

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

**💬 Prompt d'amorce (Léo → Antigravity) :**
```
Je dois créer un dashboard Streamlit pour le projet smartEngine Sprint 4.
Avant de commencer à coder, quelles dépendances Python vais-je avoir besoin ?
Aide-moi à créer ou mettre à jour src/requirements.txt.
```

> Antigravity va demander : quelles fonctionnalités sont prévues (SHAP, graphiques interactifs...) ? Quelle version de Python ? etc.

**🔄 Action manuelle (Léo) :**
```
pip install -r src/requirements.txt
```

#### Étape 5b — Générer le dashboard

**💬 Prompt d'amorce (Léo → Antigravity) :**
```
Je dois créer src/dashboard.py : une application Streamlit pour les équipes
Customer Success de RavenStack. Elle doit exploiter outputs/priorisation.csv
et outputs/scores.csv.
Pose-moi les questions nécessaires pour comprendre ce que le dashboard doit faire
avant de commencer à coder.
```

> Antigravity va demander : combien de vues ? Qui sont les utilisateurs (non techniques ?) ? Faut-il des explications SHAP ? Quelles contraintes d'accessibilité ?
> Réponds précisément : 3 vues (portefeuille, priorisation, fiche compte), utilisateurs non techniques, SHAP pour la fiche compte, accessibilité WCAG / daltonisme.

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

**💬 Prompt d'amorce (Léo → Antigravity) — si bug :**
```
J'ai une erreur au lancement du dashboard. Voici le message :
[coller le message d'erreur exact]
Qu'est-ce qui ne va pas ?
```

> Antigravity va analyser l'erreur, poser des questions de contexte si nécessaire, puis proposer une correction.

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

**💬 Prompt d'amorce (Sophie → Antigravity) :**
```
Je suis Product Owner sur le projet smartEngine Sprint 4.
Je dois rédiger un document de recommandations stratégiques pour la direction
de RavenStack, basé sur les résultats du modèle de churn.
Pose-moi les questions nécessaires avant de commencer à rédiger.
```

> Antigravity va demander : qui est le public cible ? Quels chiffres utiliser ? Faut-il calculer un ROI ? Doit-on inclure un protocole de mesure ?
> Réponds : public non technique (direction), utiliser les vrais chiffres de priorisation.csv, inclure ROI estimé et protocole groupe témoin/A/B test.

#### Étape 5g — Relire et ajuster

**🔄 Action manuelle (Sophie) :**
Relire le document. Si des passages sont trop techniques :

**💬 Prompt d'amorce (Sophie → Antigravity) :**
```
Ce passage du document de recommandations est trop technique pour la direction :
[coller le passage]
Reformule-le en langage non technique, sans jargon data science.
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

**💬 Prompt d'amorce (Quentin → Antigravity) :**
```
Je dois rédiger la sous-section 4.1 "Segmentation risque / valeur" dans
docs/dossier-conception.md, pour documenter les choix faits dans ce sprint.
Pose-moi les questions nécessaires pour rédiger cette section.
```

> Antigravity va demander : pourquoi la médiane ? Pourquoi pas un clustering ? Quel lien avec le RGPD ?
> Réponds avec tes justifications, il rédige la section.

**🔄 Action manuelle (Quentin) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.1 segmentation risque/valeur"
git push origin main
```

---

### Léo — sous-section 4.2

**💬 Prompt d'amorce (Léo → Antigravity) :**
```
Je dois rédiger la sous-section 4.2 "Dashboard Streamlit" dans
docs/dossier-conception.md pour documenter les choix de conception.
Pose-moi les questions nécessaires avant de rédiger.
```

> Antigravity va demander : pourquoi ces visualisations ? Comment as-tu géré l'accessibilité ? Quel retour d'expérience sur Streamlit ?

**🔄 Action manuelle (Léo) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.2 dashboard Streamlit"
git push origin main
```

---

### Sophie — sous-section 4.3

**💬 Prompt d'amorce (Sophie → Antigravity) :**
```
Je dois rédiger la sous-section 4.3 "Recommandations et mesure d'impact" dans
docs/dossier-conception.md.
Pose-moi les questions nécessaires pour rédiger cette section.
```

> Antigravity va demander : comment as-tu calculé le ROI ? Quel protocole de mesure as-tu défini ? Quels freins au changement as-tu anticipés ?

**🔄 Action manuelle (Sophie) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4.3 recommandations et mesure d'impact"
git push origin main
```

---

### Maé — sous-sections 4.4 et 4.5

**💬 Prompt d'amorce (Maé → Antigravity) :**
```
Je dois rédiger deux sous-sections dans docs/dossier-conception.md :
- 4.4 : Retour d'expérience sur les agents IA (bilan des 4 sprints)
- 4.5 : Limites et perspectives du modèle
Pose-moi les questions nécessaires avant de commencer.
```

> Antigravity va demander : quels agents ont été créés à chaque sprint ? Qu'est-ce qui a bien marché ? Quelles limites as-tu observées sur le modèle ?

**🔄 Action manuelle (Maé) :**
```
git add docs/dossier-conception.md
git commit -m "docs: sections 4.4 bilan agents + 4.5 limites perspectives"
git push origin main
```

✅ **Point de sync — Joanne fait `git pull origin main`**

---

## ÉTAPE 7 — Joanne : compilation de la Section 4

**💬 Prompt d'amorce (Joanne → Antigravity) :**
```
Toute l'équipe a rédigé sa sous-section dans docs/dossier-conception.md.
Je dois maintenant compiler et harmoniser la section 4 pour qu'elle soit cohérente.
Pose-moi les questions nécessaires avant de commencer.
```

> Antigravity va demander : y a-t-il des incohérences de style à corriger ? Faut-il une introduction et une conclusion à la section 4 ? Le dossier complet couvre-t-il bien les sections 1 à 4 ?

**🔄 Action manuelle (Joanne) :**
```
git add docs/dossier-conception.md
git commit -m "docs: section 4 harmonisée - dossier conception final"
git push origin main
```

✅ **Point de sync — toute l'équipe fait `git pull origin main`**

---

## ÉTAPE 8 — Joanne : plan de soutenance

**💬 Prompt d'amorce (Joanne → Antigravity) :**
```
Je dois créer un plan de soutenance pour présenter le projet smartEngine au jury.
La soutenance dure environ 20 minutes pour 5 personnes.
Pose-moi les questions nécessaires avant de générer le plan.
```

> Antigravity va demander : combien de temps par personne ? Dans quel ordre présenter les sprints ? Y a-t-il une démo live du dashboard ?

**🔄 Action manuelle (Joanne) :**
```
git add docs/soutenance_plan.md
git commit -m "docs: plan soutenance Sprint 4"
git push origin main
```

---

## ÉTAPE 9 — Maé : vérification finale de l'autonomie

**💬 Prompt d'amorce (Maé → Antigravity) :**
```
Avant la livraison finale du projet smartEngine, je dois vérifier que tous
les scripts fonctionnent sans Gemini CLI.
Aide-moi à faire cette vérification. Par quoi commencer ?
```

> Antigravity va demander : quels scripts sont concernés ? Veux-tu tester l'exécution ou seulement analyser les dépendances ? etc.

**🔄 Action manuelle (Maé) :**
Si des corrections sont nécessaires :
```
git add src/
git commit -m "fix: autonomie scripts vérifiée - aucune dépendance Gemini CLI"
git push origin main
```

---

## ÉTAPE 10 — Joanne : standup quotidien (chaque matin)

**💬 Prompt d'amorce (Joanne → Antigravity) — chaque matin :**
```
Je dois créer le compte-rendu du standup d'aujourd'hui pour le projet smartEngine.
Aide-moi à le structurer dans docs/standups/.
```

> Antigravity va demander la date, les informations de chaque membre, les blocages éventuels.

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
[ ] .gemini/agents/agent-deploiement.md → Maé     (ÉTAPE 3)
[ ] GEMINI.md mis à jour                → Joanne  (ÉTAPE 3)
[ ] docs/backlog.md Sprint 4 complet    → Joanne  (ÉTAPE 2)
[ ] docs/dossier-conception.md S4       → Tous    (ÉTAPES 6 + 7)
[ ] docs/soutenance_plan.md             → Joanne  (ÉTAPE 8)
[ ] Scripts autonomes vérifiés          → Maé     (ÉTAPE 9)
[ ] Tout est pushé sur GitHub           → Tous
```
