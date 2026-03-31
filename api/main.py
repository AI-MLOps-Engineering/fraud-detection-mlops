from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.xgboost
import mlflow
import pandas as pd
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse
import time

app = FastAPI(title="Fraud Detection API", version="1.0")

# Connexion MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Chargement du modèle
try:
    model = mlflow.xgboost.load_model("models:/fraud-detector@champion")
    print("✅ Modèle chargé avec succès")
except Exception as e:
    print(f"❌ Erreur chargement modèle : {e}")
    model = None

# Métriques Prometheus
PREDICTIONS = Counter("predictions_total", "Nombre de prédictions", ["result"])
LATENCY = Histogram("prediction_latency_seconds", "Latence des prédictions")

class Transaction(BaseModel):
    Time: float
    V1: float; V2: float; V3: float; V4: float; V5: float
    V6: float; V7: float; V8: float; V9: float; V10: float
    V11: float; V12: float; V13: float; V14: float; V15: float
    V16: float; V17: float; V18: float; V19: float; V20: float
    V21: float; V22: float; V23: float; V24: float; V25: float
    V26: float; V27: float; V28: float
    Amount: float

@app.post("/predict")
def predict(transaction: Transaction):
    if model is None:
        return {"error": "Modèle non disponible — vérifier MLflow"}

    start = time.time()
    df = pd.DataFrame([transaction.dict()])
    prediction = int(model.predict(df)[0])
    proba = float(model.predict_proba(df)[0][1])
    duration = time.time() - start

    label = "fraud" if prediction == 1 else "legit"
    PREDICTIONS.labels(result=label).inc()
    LATENCY.observe(duration)

    return {
        "prediction": label,
        "fraud_probability": round(proba, 4),
        "latency_ms": round(duration * 1000, 2)
    }

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    return generate_latest()

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}