@echo off
chcp 65001 >nul
title SmartEngine - Démarrage

echo.
echo  ╔══════════════════════════════════════╗
echo  ║        SmartEngine - Démarrage       ║
echo  ╚══════════════════════════════════════╝
echo.

:: --- Se positionner à la racine du projet ---
cd /d "%~dp0"

:: --- Vérifier que Python est installé ---
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas trouvé. Vérifiez votre installation.
    pause
    exit /b 1
)

:: --- Installer les dépendances si nécessaire ---
echo [1/3] Vérification des dépendances...
pip install -q -r src\requirements.txt
if errorlevel 1 (
    echo [ERREUR] L'installation des dépendances a échoué.
    pause
    exit /b 1
)
echo       OK - Dépendances installées.
echo.

:: --- Lancer l'API FastAPI en arrière-plan ---
echo [2/3] Démarrage de l'API FastAPI (port 8000)...
start "SmartEngine API" cmd /k "cd /d "%~dp0" && uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"
echo       OK - API disponible sur http://localhost:8000
echo       Docs Swagger  : http://localhost:8000/docs
echo.

:: --- Attendre 2 secondes que l'API démarre avant le dashboard ---
timeout /t 2 /nobreak >nul

:: --- Lancer le Dashboard Streamlit ---
echo [3/3] Démarrage du Dashboard Streamlit (port 8501)...
start "SmartEngine Dashboard" cmd /k "cd /d "%~dp0" && streamlit run src\dashboard.py"
echo       OK - Dashboard disponible sur http://localhost:8501
echo.

echo  ╔══════════════════════════════════════╗
echo  ║   Les deux services sont lancés !    ║
echo  ║                                      ║
echo  ║  API     : http://localhost:8000     ║
echo  ║  Swagger : http://localhost:8000/docs║
echo  ║  Dashboard: http://localhost:8501    ║
echo  ╚══════════════════════════════════════╝
echo.
echo  Fermez les deux fenêtres de terminal pour arrêter les services.
echo.
pause
