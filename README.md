# Projet IoT : Architecture Edge Computing et Cloud (10H)

## Introduction

Ce projet vise à reproduire une architecture IoT classique en explorant les concepts de collecte, prétraitement et visualisation de données IoT. Vous construirez une architecture composée :

- D'une API simulant des objets IoT pour fournir des données (fournie au départ de ce projet).
- D'un serveur Edge chargé de prétraiter les données et de garantir leur sécurité.
- D'un tableau de bord cloud permettant de visualiser les données et de surveiller les performances.

Les concepts clés incluent le traitement local (Edge Computing), la sécurité des données (authentification, autorisation) et la visualisation dans un service cloud comme Grafana.

Organisation : projet à réaliser par 2 ou 3, évaluation basée sur une démonstration du fonctionnement des différents éléments du projet durant la dernière demi-heure de la dernière séance.

---

## Étape 1 : Exploration de l'API IoT

### Objectif

Découvrir les endpoints disponibles et comprendre les données fournies par l'API IoT: https://renderiotapi.onrender.com/ 

### Endpoints disponibles

- `GET /iot_objects`
- `GET /iot_data/{object_id}`
- `GET /iot_objects/by_client/{client}` 
- `GET /iot_objects/{object_id}/history`

### Tâches

1. Installer un outil de test d'API comme [Postman](https://www.postman.com/downloads/) ou utiliser `curl`.
2. Tester chaque endpoint et documenter les différents endpoints. 

**Q. Que permettent ils de récupérer ? Quels sont les clients existants ? Les objets ?**

## Étape 2 : Mise en place de l'applicatif du serveur Edge

### Objectif

Créer un service Edge qui récupère les données de l'API IoT, les prétraite et les expose via une nouvelle API locale.

### Détails des prétraitements

Les prétraitements peuvent être réalisés :

1. **Par objet** :
    - Calcul de statistiques (moyenne, maximum, minimum) pour un objet spécifique.
    - Détection d'anomalies (par exemple, dépassement d'un seuil pour la température).

2. **Par client** :
    - Agrégation des données de tous les objets appartenant à un client.
    - Statistiques globales (par exemple, moyenne de la température de tous les capteurs d'un client).

### Tâches

1. Créer un projet Python avec `Flask` :

```bash
pip install flask requests
```

2. Exemple de base de code pour le serveur Edge :

```python
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_URL = "http://<votre-api>"

@app.route("/processed_data", methods=["GET"])
def processed_data():
    object_id = request.args.get("object_id")
    response = requests.get(f"{API_URL}/iot_data/{object_id}")
    data = response.json()

    # Prétraitement des données par objet
    values = [entry['value'] for entry in data['measurements']]
    stats = {
        "average": xxxx,
        "max": xxxx,
        "min": xxxx
    }

    return jsonify({"object_id": object_id, "statistics": stats})

@app.route("/client_statistics", methods=["GET"])
def client_statistics():
    client_id = request.args.get("client_id")
    response = requests.get(f"{API_URL}/iot_objects/by_client/{client_id}")
    objects = response.json()

    # Prétraitement des données par client
    ............................

    return jsonify({"client_id": client_id, "statistics": stats})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

3. Tester le serveur localement :
    - Lancez le serveur avec `python app.py`.
    - Testez les endpoints `/processed_data` et `/client_statistics` via Postman, curl ou un navigateur.
    - Vérifiez que les données prétraitées sont correctement exposées.

## Étape 3 : Sécurisation de l'API

### Objectif

Ajouter une authentification via des clés API pour garantir que chaque client accède uniquement à ses données.

### Tâches

1. Créer des clés API pour chaque client :

```python
API_KEYS = {"client1": "key1", "client2": "key2"}
```

2. Associer chaque clé API à un client dans le code du serveur Edge.
3. Implémenter une vérification des clés :

```python
@app.before_request
def authenticate():
    api_key = request.headers.get("x-api-key")
    if api_key not in API_KEYS.values():
        return jsonify({"error": "Unauthorized"}), 401
```

4. Tester l'accès avec des clés valides et invalides :
    - Simulez des requêtes avec différentes clés API.
    - Assurez-vous que seules les clés valides permettent l'accès.


## Étape 4 : Conteneurisation avec Docker

### Objectif

Conteneuriser le serveur Edge pour le rendre facilement déployable.

### Tâches

1. Créer un fichier `Dockerfile` :

```dockerfile
FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

2. Construire et exécuter le conteneur :

```bash
docker build -t edge_server .
docker run -p 5000:5000 edge_server
```

3. Tester le fonctionnement :
    - Accédez aux endpoints exposés par le conteneur à l'adresse `http://localhost:5000`.
    - Vérifiez que les données prétraitées sont accessibles.

### Livrable attendu

Un conteneur Docker fonctionnel exécutant le serveur Edge.

---

## Étape 5 : Visualisation avec Grafana

### Objectif

Créer un tableau de bord pour visualiser les données IoT prétraitées.

### Tâches

1. Créer un compte Grafana Cloud (gratuit).
2. Ajouter une source de données :
    - Configurez une source de données Prometheus ou JSON.
    - Fournissez l'URL de votre serveur Edge comme source de données.
3. Configurer un tableau de bord :
    - Créez des panels pour afficher les moyennes des données IoT.
    - Ajoutez des graphiques pour visualiser les anomalies détectées.

### Livrable attendu

Un tableau de bord Grafana affichant les données prétraitées.

---

## Étape 6 : Monitoring des performances

### Objectif

Collecter et afficher les métriques système du serveur Edge (CPU, RAM, etc.).

### Tâches

1. Configurer `prom-client` pour exposer les métriques système :

```python
from prometheus_client import Gauge, start_http_server
import psutil

cpu_usage = Gauge('cpu_usage', 'Usage CPU')
ram_usage = Gauge('ram_usage', 'Usage RAM')

start_http_server(8000)

# Mettre à jour régulièrement les métriques
while True:
    cpu_usage.set(psutil.cpu_percent())
    ram_usage.set(psutil.virtual_memory().percent)
```

2. Ajouter ces métriques dans Grafana :
    - Configurez une source de données Prometheus pointant vers le serveur Edge.
    - Ajoutez des panels pour surveiller le CPU, la RAM et d'autres paramètres.

### Livrable attendu

Un tableau de bord Grafana affichant les performances du serveur Edge.

---

## Extensions

- Déployer le serveur Edge avec Kubernetes pour explorer la scalabilité.
- Ajouter des notifications en cas d’anomalies via email ou webhook.
- Implémenter des certificats HTTPS entre Edge et Cloud.
