from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "2b10gDdQqkjMJ5gucOEEJ13e"
PROJECT = "all"  # o un altro progetto specifico se serve

@app.route("/identify", methods=["POST"])
def identify():
    if 'image' not in request.files:
        return jsonify({"error": "Nessuna immagine ricevuta"}), 400

    image = request.files['image']
    organs = request.form.get('organs', 'leaf')

    plantnet_url = f"https://my-api.plantnet.org/v2/identify/{PROJECT}?api-key={API_KEY}"

    files = {'images': (image.filename, image.stream, image.mimetype)}
    data = {'organs': organs}

    response = requests.post(plantnet_url, files=files, data=data)
    try:
        response.raise_for_status()
    except requests.HTTPError as e:
        return jsonify({"error": str(e), "details": response.text}), 500

    result = response.json()

    top = []
    for r in result['results'][:3]:
        top.append({
            'scientific_name': r['species']['scientificNameWithoutAuthor'],
            'common_name': r['species'].get('commonNames', []),
            'score': round(r['score'] * 100, 2)
        })

    return jsonify({"matches": top})
