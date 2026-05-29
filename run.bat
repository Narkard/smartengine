@echo off
chcp 65001 >nul
title SmartEngine

echo ==========================================
echo     SmartEngine - Demarrage
echo ==========================================
echo.

:: Se positionner a la racine du projet
cd /d "%~dp0"

:: Stocker le chemin de la racine dans une variable
set ROOT=%~dp0

:: Verifier que Python est installe
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python introuvable. Verifiez votre installation.
    pause
    exit /b 1
)

:: Installer les dependances
echo [1/3] Installation des dependances...
pip install -q -r src\requirements.txt
if errorlevel 1 (
    echo [ERREUR] L'installation des dependances a echoue.
    pause
    exit /b 1
)
echo       OK

echo.

:: Lancer l'API FastAPI dans une nouvelle fenetre
echo [2/3] Demarrage de l'API FastAPI sur le port 8000...
start "SmartEngine API" cmd /k "cd /d %ROOT% && uvicorn src.api:app --reload --host 0.0.0.0 --port 8000"
echo       OK - http://localhost:8000

echo.

:: Attendre 2 secondes avant de lancer Streamlit
timeout /t 2 /nobreak >nul

:: Lancer le Dashboard Streamlit dans une nouvelle fenetre
echo [3/3] Demarrage du Dashboard Streamlit sur le port 8501...
start "SmartEngine Dashboard" cmd /k "cd /d %ROOT% && streamlit run src\dashboard.py"
echo       OK - http://localhost:8501

echo.
echo ==========================================
echo   Services lances :
echo   API       : http://localhost:8000
echo   Swagger   : http://localhost:8000/docs
echo   Dashboard : http://localhost:8501
echo ==========================================
echo.
echo Fermez les fenetres de terminal pour arreter les services.
echo.
pause
