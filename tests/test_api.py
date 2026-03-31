from fastapi.testclient import TestClient
import sys
import os

# Permet d'importer api/main.py sans charger le modèle MLflow
os.environ["MLFLOW_TRACKING_URI"] = "http://localhost:5000"

from api.main import app

client = TestClient(app)

def test_health():
    """L'endpoint /health doit retourner 200"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_health_response_format():
    """La réponse /health doit contenir status et model_loaded"""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data

def test_metrics_endpoint():
    """/metrics doit retourner des métriques Prometheus"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "predictions_total" in response.text

def test_predict_without_model():
    """Sans modèle chargé, /predict doit retourner une erreur propre"""
    payload = {
        "Time": 406.0,
        "V1": -2.31, "V2": 1.95, "V3": -1.60, "V4": 3.99, "V5": -0.52,
        "V6": -1.42, "V7": -2.53, "V8": 1.39, "V9": -2.77, "V10": -2.77,
        "V11": 3.20, "V12": -2.89, "V13": -0.59, "V14": -4.28, "V15": 0.38,
        "V16": -1.14, "V17": -2.83, "V18": -0.01, "V19": 0.41, "V20": 0.12,
        "V21": 0.51, "V22": -0.03, "V23": -0.46, "V24": 0.32, "V25": 0.04,
        "V26": 0.17, "V27": 0.26, "V28": -0.14,
        "Amount": 0.0
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    # Soit une prédiction, soit une erreur propre — pas un crash 500
    assert "prediction" in data or "error" in data