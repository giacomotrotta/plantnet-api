from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "2b10gDdQqkjMJ5gucOEEJ13e"

@app.route("/")
def index():
    return "API PlantNet attiva!"

@app.route("/identify", methods=["POST"])
def identify():
    if 'image' not in request.files:
        return jsonify({"error": "Nessuna immagine ricevuta"}), 400

    image = request.files['image']
    plantnet_url = "https://my-api.plantnet.org/v2/identify/all"

    files = {'images': image.stream}
    data = {
        'organs': 'leaf',
        'api-key': API_KEY
    }

    response = requests.post(plantnet_url, files=files, data=data)
    response.raise_for_status()
    result = response.json()

    top = []
    for r in result['results'][:3]:
        top.append({
            'scientific_name': r['species']['scientificNameWithoutAuthor'],
            'common_name': r['species'].get('commonNames', []),
            'score': round(r['score'] * 100, 2)
        })

    return jsonify({"matches": top})
