import subprocess
import os
import sys

# Utilisation du chemin Python identifié
PYTHON_EXE = sys.executable

def run_sprint_pipeline():
    print("=== Pipeline smartEngine - Exécution Complète ===")
    
    # 1. Sprint 2: Data Pipeline
    print("\n--- Étape 1: Traitement des données ---")
    subprocess.run([PYTHON_EXE, "src/data_pipeline.py"], check=True)
    
    # 2. Sprint 3: Modélisation
    print("\n--- Étape 2: Entraînement du modèle ---")
    subprocess.run([PYTHON_EXE, "src/train_model.py"], check=True)
    
    print("\n=== Pipeline Terminé avec Succès ===")
    print("Pour lancer le dashboard : streamlit run src/dashboard.py")

if __name__ == "__main__":
    run_sprint_pipeline()
