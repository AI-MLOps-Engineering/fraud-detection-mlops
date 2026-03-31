import mlflow
import mlflow.xgboost
import pandas as pd
import os  
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report

#mlflow.set_tracking_uri("http://127.0.0.1:5000")
#mlflow.set_experiment("fraud-detection")
MLFLOW_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
mlflow.set_tracking_uri(MLFLOW_URI)
mlflow.set_experiment("fraud-detection")

with mlflow.start_run():
    # Chargement données
    df = pd.read_csv("data/creditcard.csv")
    X = df.drop("Class", axis=1)
    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # Paramètres — MLflow les track automatiquement
    params = {"n_estimators": 200, "max_depth": 6, "scale_pos_weight": 577}
    mlflow.log_params(params)

    model = XGBClassifier(**params)
    model.fit(X_train, y_train)

    # Métriques
    preds = model.predict(X_test)
    f1 = f1_score(y_test, preds)
    mlflow.log_metric("f1_score", f1)
    print(f"F1-score : {f1:.3f}")

    # Sauvegarde du modèle dans le registry MLflow
    # mlflow.xgboost.log_model(model, "model", registered_model_name="fraud-detector")
    mlflow.xgboost.log_model(
        model,
        artifact_path="model",
        registered_model_name="fraud-detector"
    )
    print("✅ Modèle enregistré dans le registry MLflow")