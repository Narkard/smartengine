# Dossier de Conception - smartEngine

## 1. Cadrage du Projet (Sprint 1)
*Contenu du Sprint 1 (Cadrage métier, RGPD, Outils)*

## 2. Traitement des Données (Sprint 2)

### 2.1 État des données brutes
Avant nettoyage, les données présentaient :
- Des types de dates incohérents (stockés en chaînes).
- **825 valeurs manquantes** dans le score de satisfaction client (`support_tickets.csv`).
- Des disparités de granularité (comptes vs tickets vs usage).

### 2.2 Stratégies de Nettoyage
- **Imputation** : Nous avons choisi l'imputation par la **médiane** pour le `satisfaction_score`. Cette stratégie permet de ne pas supprimer 40% des tickets tout en restant robuste aux valeurs extrêmes.
- **Conversion** : Toutes les colonnes temporelles ont été normalisées au format `datetime`.
- **Dédoublonnage** : Aucune suppression n'a été nécessaire après vérification.

### 2.3 Table Analytique & Features
- **Granularité** : Une ligne par `account_id` (Compte client).
- **Features créées** :
    - *Usage* : Sommes, moyennes et écart-types de `usage_count` et `usage_duration`.
    - *Support* : Nombre de tickets, taux d'escalade (`high_escalation_ratio`) et délai de résolution moyen.
    - *Engagement* : Recréation du profil du dernier abonnement actif (MRR, Plan, Fréquence).
- **Target** : Variable binaire `target_churn` (1 si résilié, 0 sinon).

### 2.4 Retour d'expérience Agent
L'utilisation de l'agent **Data Engineer** (`data-processor.md`) a permis d'automatiser la génération des scripts de nettoyage et de jointure. Quelques corrections manuelles ont été apportées sur les types de jointures (`left join`) pour garantir qu'aucun client ne soit perdu lors de la fusion.

*Dernière mise à jour : 30 mars 2026*
