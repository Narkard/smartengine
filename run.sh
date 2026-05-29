#!/bin/bash

# Aller à la racine du projet (dossier où se trouve ce script)
cd "$(dirname "$0")"

echo "=========================================="
echo "    SmartEngine - Demarrage"
echo "=========================================="
echo ""

# Verifier que Python est installe
if ! command -v python3 &>/dev/null; then
    echo "[ERREUR] python3 introuvable. Verifiez votre installation."
    exit 1
fi

# Installer les dependances
echo "[1/3] Installation des dependances..."
pip3 install -q -r src/requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERREUR] L'installation des dependances a echoue."
    exit 1
fi
echo "      OK"
echo ""

# Lancer l'API FastAPI dans un terminal en arriere-plan
echo "[2/3] Demarrage de l'API FastAPI sur le port 8000..."
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000 &
API_PID=$!
echo "      OK - http://localhost:8000"
echo "      Swagger : http://localhost:8000/docs"
echo ""

# Attendre 2 secondes que l'API demarre
sleep 2

# Lancer le Dashboard Streamlit en arriere-plan
echo "[3/3] Demarrage du Dashboard Streamlit sur le port 8501..."
streamlit run src/dashboard.py &
DASHBOARD_PID=$!
echo "      OK - http://localhost:8501"
echo ""

echo "=========================================="
echo "  Services lances :"
echo "  API       : http://localhost:8000"
echo "  Swagger   : http://localhost:8000/docs"
echo "  Dashboard : http://localhost:8501"
echo "=========================================="
echo ""
echo "  Appuyez sur Ctrl+C pour tout arreter."
echo ""

# Attendre et intercepter Ctrl+C pour tout stopper proprement
trap "echo ''; echo 'Arret des services...'; kill $API_PID $DASHBOARD_PID 2>/dev/null; exit 0" SIGINT SIGTERM
wait
