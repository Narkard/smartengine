# Rapport de Performance du Modèle smartEngine - Sprint 3

## 1. Résumé Exécutif
Le modèle de prédiction de churn pour RavenStack a été finalisé lors du Sprint 3. L'algorithme retenu est le **Gradient Boosting Classifier (GBM)**. 
- **Précision globale (Accuracy) :** 70%
- **Rappel (Recall) sur le Churn :** 5% (Basé sur le seuil par défaut de 0.5)
- **Top Feature :** `usage_duration_secs_mean` (Engagement temporel)

Le modèle actuel privilégie la précision globale mais nécessite un ajustement des seuils pour mieux capturer les churners réels (Recall faible à 0.5). L'utilisation de scores de probabilité permet néanmoins de segmenter les comptes par risque.

---

## 2. Comparaison des Algorithmes
Trois algorithmes ont été évalués (estimations basées sur les tests de phase de recherche) :

| Algorithme | Accuracy | F1-Score (Churn) | Recall (Churn) | État |
| :--- | :---: | :---: | :---: | :--- |
| Régression Logistique | 0.65 | 0.04 | 0.03 | Écarté |
| Random Forest | 0.68 | 0.06 | 0.04 | Écarté |
| **Gradient Boosting (GBM)** | **0.70** | **0.06** | **0.05** | **Retenu** |

---

## 3. Matrice de Confusion (Seuil 0.5)
Basé sur le jeu de test (100 comptes) :

| | Prédiction : Non-Churn | Prédiction : Churn |
| :--- | :---: | :---: |
| **Réel : Non-Churn** | 69 (VN) | 9 (FP) |
| **Réel : Churn** | 21 (FN) | 1 (VP) |

**Analyse :** Au seuil standard de 0.5, le modèle manque beaucoup de churners (21 faux négatifs). C'est pourquoi l'utilisation du **churn_score** avec un seuil abaissé est indispensable pour l'action métier.

---

## 4. Analyse des Features Importantes
Les variables clés influençant le score de churn :

1. **`usage_duration_secs_mean` (13.2%)** : Le temps moyen passé par session est le signal le plus fort. Un désengagement temporel précède souvent la résiliation.
2. **`error_count_mean` (12.7%)** : Un taux d'erreurs élevé génère une frustration technique immédiate.
3. **`first_response_time_minutes` (8.4%)** : La réactivité du support est cruciale pour la rétention.
4. **`mrr_amount` (8.1%)** : La valeur du contrat influence la stabilité du compte.
5. **`resolution_time_hours` (8.0%)** : Le temps total pour clore un ticket.

**Interprétation métier :** Le churn est multi-factoriel : il combine un **désengagement d'usage** et une **friction opérationnelle/support**.

---

## 5. Biais identifiés par sous-groupe
- **Plan Tier** : Les comptes Pro et Enterprise ont des comportements d'usage très différents, le modèle tend à mieux prédire les comptes à faible MRR.
- **Beta Features** : Les utilisateurs de fonctionnalités Beta génèrent plus d'erreurs, ce qui peut artificiellement augmenter leur score de risque alors qu'ils sont très engagés.

---

## 6. Limites connues
- **Déséquilibre des classes** : Le faible nombre d'événements de churn dans le dataset limite l'apprentissage des motifs rares.
- **Données statiques** : Le modèle ne prend pas encore en compte l'évolution temporelle (pente de l'usage sur les 3 derniers mois).
- **Sentiment Support** : L'absence d'analyse textuelle des tickets limite la compréhension de l'insatisfaction "cachée".

---

## 7. Seuils retenus pour `scores.csv`
Pour compenser le faible rappel au seuil 0.5, nous avons défini :
- **High (>= 0.65)** : 18.4% de la base. Risque critique, intervention immédiate.
- **Medium (>= 0.35)** : 2.8% de la base. Risque modéré, surveillance accrue.
- **Low (< 0.35)** : 78.8% de la base. Comptes sains.

*Justification :* Ces seuils permettent de flagger environ 20% des clients comme "à risque" pour action prioritaire par les CS.

---

## 8. Recommandations pour le Sprint 4
1. **SMOTE / Upsampling** : Appliquer des techniques de ré-échantillonnage pour améliorer le rappel.
2. **Feature Engineering Temporel** : Créer des features de "trend" (ex: différence d'usage M vs M-1).
3. **NLP simple** : Extraire des mots-clés "négatifs" des tickets de support.
4. **Dashboard** : Visualiser la distribution géographique des scores "High" pour allouer les ressources CS.
