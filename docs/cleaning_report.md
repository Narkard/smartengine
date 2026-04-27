# Rapport de Nettoyage et Recalcul de la Cible - Projet smartEngine

## 1. Synthèse du Recalcul de la Cible
L'objectif principal était de fiabiliser la variable cible (churn) en délaissant la colonne `churnflag` d'origine, jugée incohérente avec les événements réels de résiliation.

### Comparaison des sources :
- **Source d'origine (`churn_flag`)** : 110 cas de churn identifiés.
- **Source alternative (`churn_events`)** : 352 cas de churn identifiés.

**Décision** : La cible a été recalculée en croisant la table des comptes avec la table des événements de churn. Tout compte présent dans `ravenstack_churn_events.csv` est désormais marqué comme `churn_flag = 1`.

---

## 2. Sources Utilisées et Justification

| Source | Rôle | Justification (Fiabilité, Complétude, Cohérence) |
| :--- | :--- | :--- |
| `ravenstack_accounts.csv` | Référentiel clients | Source primaire pour l'identité des comptes. La colonne `churn_flag` a été **exclue** car elle sous-évaluait massivement le churn réel. |
| `ravenstack_churn_events.csv` | Source de vérité (Cible) | **Source privilégiée.** Elle contient des logs transactionnels de résiliation (dates, motifs, montants remboursés), ce qui lui confère une fiabilité opérationnelle supérieure aux flags statiques. |
| `ravenstack_subscriptions.csv` | Données contractuelles | Utilisée pour l'ancienneté et le MRR. La colonne `churn_flag` y a également été **exclue** par souci de cohérence globale. |
| `ravenstack_feature_usage.csv` | Comportement utilisateur | Utilisée pour calculer les tendances d'engagement. Source exhaustive sur les interactions techniques. |
| `ravenstack_support_tickets.csv` | Satisfaction client | Utilisée pour mesurer la tension relationnelle (tickets critiques, temps de résolution). |

---

## 3. Détail des Transformations et Arbitrages

### Éviction de `churnflag`
Toute référence à `churnflag` dans les fichiers `accounts` et `subscriptions` a été supprimée dès l'étape de nettoyage (`clean_data.py`). Cela garantit qu'aucune logique prédictive ou analytique ne s'appuie par erreur sur cette source corrompue.

### Arbitrage des conflits
En cas de conflit entre le flag statique (ex: `churn_flag=False`) et l'existence d'un événement (ex: présence dans `churn_events`), l'événement prévaut systématiquement. Un événement de résiliation est une action concrète et datée, tandis qu'un flag peut ne pas avoir été mis à jour suite à un bug de synchronisation ou une erreur humaine.

### Abstraction des Chemins
Tous les scripts ont été mis à jour pour utiliser des chemins relatifs via `os.path.abspath(__file__)`. Le projet peut désormais être déplacé ou cloné sur n'importe quel environnement sans modification du code source.

---

## 4. Statistiques Finales (Table Analytique)
- **Nombre total de comptes** : 500
- **Taux de Churn (Recalculé)** : 70.4% (352 / 500)
- **Nombre de variables** : 28 (incluant features d'usage, support et financier)
