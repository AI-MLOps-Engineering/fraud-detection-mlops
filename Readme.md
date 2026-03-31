\# Structure du projet qu'on va créer

fraud-detection-mlops/

├── data/               # données brutes (gitignore)

├── src/

│   ├── train.py        # entraînement + MLflow

│   ├── predict.py      # logique de prédiction

│   └── features.py     # feature engineering

├── api/

│   └── main.py         # FastAPI

├── monitoring/

│   ├── prometheus.yml

│   └── grafana/

├── .github/workflows/  # CI/CD

├── Dockerfile

├── docker-compose.yml

└── requirements.txt

