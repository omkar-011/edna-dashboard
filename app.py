
from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

from flask import Flask, request, jsonify
from flask_cors import CORS
import math
import random

app = Flask(__name__)
CORS(app)

TAXONOMY = ["Bacteria", "Fungi", "Plant", "Animal", "Protist"]

def calculate_shannon_index(counts):
    total = sum(counts.values())
    if total == 0:
        return 0
    shannon = 0
    for count in counts.values():
        p = count / total
        if p > 0:
            shannon -= p * math.log(p)
    return round(shannon, 3)

@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if file is None:
        return jsonify({"error": "No file uploaded"}), 400

    content = file.read().decode('utf-8').strip()
    sequences = [line.strip() for line in content.splitlines() if line.strip()]

    if not sequences:
        return jsonify({"error": "Empty or invalid file content"}), 400

    taxonomy_counts = dict.fromkeys(TAXONOMY, 0)
    for seq in sequences:
        taxon = random.choice(TAXONOMY)
        taxonomy_counts[taxon] += 1

    species_richness = sum(1 for count in taxonomy_counts.values() if count > 0)
    shannon_index = calculate_shannon_index(taxonomy_counts)

    return jsonify({
        "species_richness": species_richness,
        "shannon_index": shannon_index,
        "taxonomy_counts": taxonomy_counts
    })
#withou host
if __name__ == '__main__':
    app.run(port=5000, debug=True)

# #for host
# if __name__ == "__main__":
#     import os
#     port = int(os.environ.get("PORT", 10000))
#     app.run(host="0.0.0.0", port=port)


