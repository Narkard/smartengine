# smartEngine - Churn Prediction for SaaS B2B

## Project Status
- **Sprint 1 : Infrastructure & Exploration (Done ✅)**
- **Sprint 2 : Data Preparation & Feature Engineering (Done ✅)**
- **Sprint 3 : Modeling (Next)**

## Repository Structure (End of Sprint 2)
- `.gemini/agents/` : Specialized AI agents for data exploration and engineering.
- `data/` : 
    - `raw/` : Original CSV files (never modified).
    - `processed/` : Cleaned and analytical data (`analytics.csv`).
- `docs/` : Documentation (Design dossier, brief, standups).
- `outputs/` : Reports and results (`rapport-nettoyage.md`).
- `src/` : Scripts for cleaning, feature building, and merging.
- `GEMINI.md` : Orchestration context.

## Usage
1.  **Cleaning**: `python3 src/clean_data.py`
2.  **Features**: `python3 src/build_features.py`
3.  **Analytics Table**: `python3 src/build_analytics.py`

## Team (Sprint 2 Roles)
- **Product Owner** : [Nouveau Nom]
- **Scrum Master** : [Nouveau Nom]
- **IA Developer** : Sophie
