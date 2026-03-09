from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="smartEngine API",
    description="API de prédiction de churn pour RavenStack",
    version="1.0.0"
)

# Configuration CORS pour autoriser le frontend Vue.js (par défaut port 5173 avec Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "smartEngine API is running"}
