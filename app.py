
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import math

app = Flask(__name__, static_folder='frontend')
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

# Deterministic taxonomy assignment based on sequence prefixes
def assign_taxonomy(seq):
    if seq.startswith('A'):
        return "Animal"
    elif seq.startswith('T'):
        return "Plant"
    elif seq.startswith('C'):
        return "Bacteria"
    elif seq.startswith('G'):
        return "Fungi"
    else:
        return "Protist"

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

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

    # Assign taxonomy deterministically for consistency
    for seq in sequences:
        taxon = assign_taxonomy(seq)
        taxonomy_counts[taxon] += 1

    species_richness = sum(1 for count in taxonomy_counts.values() if count > 0)
    shannon_index = calculate_shannon_index(taxonomy_counts)

    return jsonify({
        "species_richness": species_richness,
        "shannon_index": shannon_index,
        "taxonomy_counts": taxonomy_counts
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
