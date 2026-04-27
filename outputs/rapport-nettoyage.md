# Rapport de Nettoyage des Données - Sprint 2

Ce rapport documente les opérations de nettoyage effectuées sur les données brutes pour garantir la fiabilité de la table analytique finale.

## 1. Analyse par fichier CSV

### 1.1 Accounts (`ravenstack_accounts.csv`)
| Problème | Volume | Stratégie | Justification | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| Source cible non fiable | 100% des lignes | Suppression de `churn_flag` | La colonne sous-évaluait le churn réel (110 vs 352). | Colonne exclue |
| Chemins absolus | N/A | Abstraction relative | Portabilité du code. | OK |

### 1.2 Subscriptions (`ravenstack_subscriptions.csv`)
| Problème | Volume | Stratégie | Justification | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| Types incorrects | 100% des lignes | Conversion `to_datetime` | Nécessaire pour les calculs d'ancienneté. | Dates valides |
| Valeurs manquantes | 4514 lignes (`end_date`) | Conservation | Normal pour les abonnements actifs. | Inchangé |
| Outliers (MRR) | 46 lignes (> 17114.0) | Winsorisation (Clip au Q99) | Éviter que des comptes extrêmes ne faussent les moyennes. | MRR plafonné |
| Orphelins | 0 identifié | Vérification de l'existence | Garantir l'intégrité référentielle. | 100% conservé |
| Source cible non fiable | 100% des lignes | Suppression de `churn_flag` | Cohérence avec la table Accounts. | Colonne exclue |

### 1.3 Feature Usage (`ravenstack_feature_usage.csv`)
| Problème | Volume | Stratégie | Justification | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| Types incorrects | 100% des lignes | Conversion `to_datetime` | Permet le calcul de récence et de tendances. | Dates valides |
| Qualité globale | Élevée | Aucune suppression | Données complètes et structurées. | 25000 lignes |

### 1.4 Support Tickets (`ravenstack_support_tickets.csv`)
| Problème | Volume | Stratégie | Justification | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| Valeurs manquantes | 825 lignes (Score) | Imputation par la médiane | 41% de manquants ; la médiane est moins sensible aux extrêmes. | Score complété |
| Types incorrects | 100% des lignes | Conversion `to_datetime` | Calcul du délai de résolution. | Dates valides |

### 1.5 Churn Events (`ravenstack_churn_events.csv`)
| Problème | Volume | Stratégie | Justification | Résultat |
| :--- | :--- | :--- | :--- | :--- |
| Valeurs manquantes | 148 lignes (Feedback) | Remplacement par "No feedback" | Donnée textuelle ; évite les erreurs de traitement NLP. | Texte normalisé |
| Incohérence cible | 352 comptes uniques | Promotion en "Source de Vérité" | Plus fiable que le flag statique d'origine. | Cible recalculée |

---

## 2. Bilan Global

| Métrique | Valeur |
| :--- | :--- |
| **Nombre total de lignes traitées** | 33 100 |
| **Lignes supprimées** | 0 (priorité à l'imputation et au clipping) |
| **Taux de conservation** | 100% |
| **Taux de perte** | 0% |

**Note sur la Cible** : Bien que 100% des lignes aient été conservées, la définition du "Churn" a radicalement changé, passant d'un flag binaire statique à une détection basée sur les événements réels.

---
*Rapport généré automatiquement le 27/04/2026 dans le cadre du Sprint 2.*
