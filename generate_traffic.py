import requests
import time
import random

url = "http://localhost:8000/predict"
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

print("Envoi de requetes... Ctrl+C pour arreter")
count = 0
while True:
    payload["Amount"] = round(random.uniform(0, 1000), 2)
    r = requests.post(url, json=payload)
    data = r.json()
    count += 1
    print(f"Requete {count}: {data['prediction']} ({data['latency_ms']}ms)")
    time.sleep(0.5)