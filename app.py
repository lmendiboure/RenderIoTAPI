from flask import Flask, jsonify, request
import random
import datetime

app = Flask(__name__)

# Simuler une base de données de capteurs IoT
# Chaque client dispose d'au moins 2 objets de types différents
iot_objects = [
    {"id": "device_1", "client": "client_1", "type": "temperature_sensor"},
    {"id": "device_2", "client": "client_1", "type": "humidity_sensor"},
    {"id": "device_3", "client": "client_2", "type": "activity_tracker"},
    {"id": "device_4", "client": "client_2", "type": "temperature_sensor"},
    {"id": "device_5", "client": "client_3", "type": "humidity_sensor"},
    {"id": "device_6", "client": "client_3", "type": "activity_tracker"}
]

# Endpoint 1 : Liste des objets IoT
@app.route('/iot_objects', methods=['GET'])
def get_iot_objects():
    """
    Retourne la liste de tous les objets IoT disponibles.
    """
    return jsonify(iot_objects)

# Endpoint 2 : Données d’un objet IoT spécifique
@app.route('/iot_objects/<id>', methods=['GET'])
def get_iot_data(id):
    """
    Retourne les données en temps réel d’un objet IoT spécifique.
    """
    device = next((d for d in iot_objects if d["id"] == id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    # Générer des données dynamiques en fonction du type de capteur
    data = {
        "id": id,
        "client": device["client"],
        "type": device["type"],
        "metrics": {
            "temperature": round(random.uniform(20.0, 30.0), 2) if "temperature" in device["type"] else None,
            "humidity": random.randint(40, 80) if "humidity" in device["type"] else None,
            "battery_level": random.randint(10, 100),
            "activity_level": random.randint(0, 100) if "activity" in device["type"] else None
        },
        "timestamp": datetime.datetime.now().isoformat()
    }
    return jsonify(data)

# Endpoint 3 : Historique des données d’un objet IoT
@app.route('/iot_objects/<id>/history', methods=['GET'])
def get_iot_history(id):
    """
    Retourne l'historique des données d’un objet IoT spécifique (10 derniers points).
    """
    device = next((d for d in iot_objects if d["id"] == id), None)
    if not device:
        return jsonify({"error": "Device not found"}), 404

    # Générer des données historiques
    history = [
        {
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=i)).isoformat(),
            "value": round(random.uniform(20.0, 30.0), 2) if "temperature" in device["type"] else random.randint(40, 80)
        } for i in range(10)
    ]
    return jsonify({"id": id, "client": device["client"], "type": device["type"], "history": history})

# Endpoint 4 : Filtrage par client
@app.route('/iot_objects/by_client/<client>', methods=['GET'])
def get_objects_by_client(client):
    """
    Retourne tous les objets IoT appartenant à un client spécifique.
    """
    client_devices = [d for d in iot_objects if d["client"] == client]
    if not client_devices:
        return jsonify({"error": "No devices found for this client"}), 404

    return jsonify(client_devices)

# Endpoint racine pour orienter les élèves
@app.route('/', methods=['GET'])
def index():
    """
    Message d’accueil pour guider les élèves vers l’exploration.
    """
    return jsonify({
        "message": "Bienvenue sur l'API IoT. Explorez les endpoints disponibles pour récupérer les données.",
        "hint": "Commencez par /iot_objects pour voir les objets disponibles."
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
