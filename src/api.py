"""
API FastAPI - SmartEngine
Expose les scores de churn et la priorisation pour n8n.
Lancement : uvicorn src.api:app --reload  (depuis la racine du projet)
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# --- Chemins (relatifs à la racine du projet) ---
# On détecte la racine : ce fichier est dans src/, donc on remonte d'un niveau
BASE_DIR = Path(__file__).resolve().parent.parent
SCORES_PATH = BASE_DIR / "outputs" / "scores.csv"
PRIORISATION_PATH = BASE_DIR / "outputs" / "priorisation.csv"

# Chemins des scripts du pipeline (relatifs à la racine)
SCRIPT_SCORES = BASE_DIR / "src" / "generate_scores.py"
SCRIPT_PRIORISATION = BASE_DIR / "src" / "generate_priorisation.py"

# --- Initialisation de l'application ---
app = FastAPI(
    title="SmartEngine API",
    description="API de churn scoring pour les workflows n8n",
    version="1.0.0",
)

# --- Middleware CORS : autorise les appels externes (n8n, navigateur, etc.) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # En prod, restreindre à l'IP du serveur n8n
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def charger_scores() -> pd.DataFrame:
    """Charge scores.csv et lève une erreur propre si absent."""
    if not SCORES_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail=f"Fichier scores.csv introuvable : {SCORES_PATH}"
        )
    df = pd.read_csv(SCORES_PATH)
    return df


def convertir_en_python_natif(obj):
    """Convertit les types numpy en types Python natifs pour la sérialisation JSON."""
    import numpy as np
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def df_vers_json(df: pd.DataFrame) -> list:
    """Convertit un DataFrame en liste de dicts avec types Python natifs."""
    records = df.to_dict(orient="records")
    # Convertit chaque valeur numpy en type Python standard
    propres = []
    for row in records:
        propres.append({k: convertir_en_python_natif(v) for k, v in row.items()})
    return propres


# ---------------------------------------------------------------------------
# Endpoint 1 : GET /health
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Santé"])
def health():
    """Vérifie que l'API tourne."""
    return {"status": "ok"}


# ---------------------------------------------------------------------------
# Endpoint 2 : GET /scores
# ---------------------------------------------------------------------------

@app.get("/scores", tags=["Scores"])
def get_scores():
    """Retourne tous les comptes de scores.csv au format JSON."""
    df = charger_scores()
    return df_vers_json(df)


# ---------------------------------------------------------------------------
# Endpoint 3 : GET /scores/{account_id}
# ---------------------------------------------------------------------------

@app.get("/scores/{account_id}", tags=["Scores"])
def get_score_par_compte(account_id: str):
    """Retourne le score d'un compte précis. Erreur 404 si inconnu."""
    df = charger_scores()
    ligne = df[df["account_id"] == account_id]

    if ligne.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Compte '{account_id}' introuvable dans scores.csv"
        )

    # Retourne le premier résultat (l'account_id est unique)
    return df_vers_json(ligne)[0]


# ---------------------------------------------------------------------------
# Endpoint 4 : GET /portfolio
# ---------------------------------------------------------------------------

@app.get("/portfolio", tags=["Synthèse"])
def get_portfolio():
    """
    Retourne une synthèse globale du portefeuille.
    Les noms de champs sont fixes pour garantir la compatibilité n8n.
    """
    df = charger_scores()

    # Normalise la casse de risk_level pour les comparaisons
    risk_lower = df["risk_level"].str.lower()

    total_accounts = int(len(df))
    high_count    = int((risk_lower == "high").sum())
    medium_count  = int((risk_lower == "medium").sum())
    low_count     = int((risk_lower == "low").sum())

    # MRR à risque : nécessite priorisation.csv pour la colonne MRR
    mrr_a_risque = 0
    if PRIORISATION_PATH.exists():
        df_prio = pd.read_csv(PRIORISATION_PATH)
        # Filtre les comptes high risk et somme leur MRR
        col_mrr = "MRR" if "MRR" in df_prio.columns else "mrr"
        df_high = df_prio[df_prio["risk_level"].str.lower() == "high"]
        if col_mrr in df_prio.columns:
            mrr_a_risque = int(round(df_high[col_mrr].sum()))

    # Moyenne du score de churn (colonne réelle : churn_score)
    col_score = "churn_score" if "churn_score" in df.columns else "churn_probability"
    avg_score = round(float(df[col_score].mean()), 3)

    return {
        "total_accounts": total_accounts,
        "high_count":     high_count,
        "medium_count":   medium_count,
        "low_count":      low_count,
        "mrr_a_risque":   mrr_a_risque,
        "avg_score":      avg_score,
    }


# ---------------------------------------------------------------------------
# Endpoint 5 : GET /priorisation
# ---------------------------------------------------------------------------

@app.get("/priorisation", tags=["Priorisation"])
def get_priorisation():
    """
    Retourne le contenu de priorisation.csv.
    Si le fichier n'existe pas, indique qu'il n'est pas encore généré.
    """
    if not PRIORISATION_PATH.exists():
        return {
            "status": "non_disponible",
            "message": "Le fichier priorisation.csv n'a pas encore été généré. "
                       "Appelez POST /run-pipeline pour le créer."
        }

    df = pd.read_csv(PRIORISATION_PATH)
    return df_vers_json(df)


# ---------------------------------------------------------------------------
# Endpoint 6 : POST /run-pipeline
# ---------------------------------------------------------------------------

@app.post("/run-pipeline", tags=["Pipeline"])
def run_pipeline():
    """
    Régénère les données en exécutant les scripts du pipeline dans l'ordre :
    1. generate_scores.py  → produit outputs/scores.csv
    2. generate_priorisation.py → produit outputs/priorisation.csv
    NE réentraîne PAS le modèle (train_model.py reste manuel).
    """
    etapes = []
    statut_global = "ok"

    # Liste des scripts à exécuter dans l'ordre
    scripts = [
        ("generate_scores.py", SCRIPT_SCORES),
        ("generate_priorisation.py", SCRIPT_PRIORISATION),
    ]

    for nom_script, chemin_script in scripts:
        if not chemin_script.exists():
            # Le script est introuvable : on enregistre l'erreur et on continue
            etapes.append({
                "script": nom_script,
                "statut": "erreur",
                "detail": f"Script introuvable : {chemin_script}"
            })
            statut_global = "erreur"
            continue

        try:
            # Lance le script avec le même interpréteur Python que l'API
            # On utilise la racine du projet comme répertoire de travail
            resultat = subprocess.run(
                [sys.executable, str(chemin_script)],
                capture_output=True,
                text=True,
                cwd=str(BASE_DIR),
                timeout=120,  # 2 minutes max par script
            )

            if resultat.returncode == 0:
                etapes.append({"script": nom_script, "statut": "ok"})
            else:
                # Le script a retourné un code d'erreur
                etapes.append({
                    "script": nom_script,
                    "statut": "erreur",
                    "detail": resultat.stderr.strip() or resultat.stdout.strip()
                })
                statut_global = "erreur"

        except subprocess.TimeoutExpired:
            etapes.append({
                "script": nom_script,
                "statut": "erreur",
                "detail": "Timeout : le script a dépassé 120 secondes"
            })
            statut_global = "erreur"

        except Exception as e:
            etapes.append({
                "script": nom_script,
                "statut": "erreur",
                "detail": str(e)
            })
            statut_global = "erreur"

    return {
        "status":       statut_global,
        "etapes":       etapes,
        "regenere_le":  datetime.now().isoformat(timespec="seconds"),
    }
