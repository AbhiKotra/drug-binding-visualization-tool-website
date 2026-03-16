from flask import Flask, request, jsonify, render_template
import os
import subprocess
import base64
import uuid
import sys

# ─────────────────────────────────────────────────────────────────
# app.py — the Flask web server
#
# Think of this file as the "manager" of your restaurant.
# It receives files from the browser, tells the kitchen (your scripts)
# to run, then sends results back to the browser.
# ─────────────────────────────────────────────────────────────────

app = Flask(__name__)

# Where this file lives (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folders for temporary uploads and results
UPLOAD_FOLDER  = os.path.join(BASE_DIR, "data", "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "data", "results")
IMAGES_FOLDER  = os.path.join(BASE_DIR, "data", "images")
SCRIPTS_FOLDER = os.path.join(BASE_DIR, "scripts")

# Create these folders if they don't exist yet
os.makedirs(UPLOAD_FOLDER,  exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(IMAGES_FOLDER,  exist_ok=True)


# ── Route 1: Serve the main webpage ───────────────────────────────
# When someone visits your URL, this sends them index.html
@app.route('/')
def index():
    return render_template('index.html')


# ── Route 2: Receive uploaded files & run analysis ────────────────
# When the user clicks Analyze, the browser sends the files here
@app.route('/analyze', methods=['POST'])
def analyze():
    # ── Step 1: Get the uploaded files ──
    if 'alphafold' not in request.files or 'bound' not in request.files:
        return jsonify({'error': 'Please upload both PDB files.'}), 400

    alphafold_file = request.files['alphafold']
    bound_file     = request.files['bound']
    ligand_code    = request.form.get('ligand_code', 'IRE').strip().upper()

    # ── Step 2: Save with unique names so simultaneous users don't overwrite each other ──
    session_id     = str(uuid.uuid4())[:8]   # random 8-character ID
    alphafold_path = os.path.join(UPLOAD_FOLDER, f"{session_id}_alphafold.pdb")
    bound_path     = os.path.join(UPLOAD_FOLDER, f"{session_id}_bound.pdb")
    results_dir    = os.path.join(RESULTS_FOLDER, session_id)
    images_dir     = os.path.join(IMAGES_FOLDER,  session_id)

    os.makedirs(results_dir, exist_ok=True)
    os.makedirs(images_dir,  exist_ok=True)

    alphafold_file.save(alphafold_path)
    bound_file.save(bound_path)

    python = sys.executable  # use the same Python that's running Flask

    # ── Step 3: Run analyze_structure.py ──
    subprocess.run([
        python,
        os.path.join(SCRIPTS_FOLDER, 'analyze_structure.py'),
        alphafold_path,   # arg 1: alphafold PDB
        bound_path,       # arg 2: bound PDB
        results_dir       # arg 3: where to save the CSV
    ], check=True)

    # ── Step 4: Run find_binding_pocket.py ──
    subprocess.run([
        python,
        os.path.join(SCRIPTS_FOLDER, 'find_binding_pocket.py'),
        bound_path,    # arg 1: bound PDB
        ligand_code,   # arg 2: ligand residue name (e.g. "IRE")
        results_dir    # arg 3: where to save the TXT
    ], check=True)

    # ── Step 5: Run plot_summary.py ──
    subprocess.run([
        python,
        os.path.join(SCRIPTS_FOLDER, 'plot_summary.py'),
        results_dir,   # arg 1: folder with the CSV
        images_dir     # arg 2: where to save the PNG
    ], check=True)

    # ── Step 6: Read the results and send them back to the browser ──

    # Read the CSV stats
    csv_path = os.path.join(results_dir, "structure_summary.csv")
    stats = []
    if os.path.exists(csv_path):
        import csv
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            stats = list(reader)

    # Read the binding pocket residues text file
    pocket_path = os.path.join(results_dir, "binding_pocket_residues.txt")
    pocket_text = ""
    if os.path.exists(pocket_path):
        with open(pocket_path) as f:
            pocket_text = f.read()

    # Convert the graph PNG to base64 (a way to embed an image directly in JSON)
    graphs = []
    for filename in os.listdir(images_dir):
        if filename.endswith('.png'):
            filepath = os.path.join(images_dir, filename)
            with open(filepath, 'rb') as f:
                encoded = base64.b64encode(f.read()).decode('utf-8')
                graphs.append({'name': filename, 'data': encoded})

    # Send everything back to the browser as JSON
    return jsonify({
        'status': 'success',
        'stats': stats,
        'pocket': pocket_text,
        'graphs': graphs,
        # Also send back the file paths so the 3D viewer can load them
        'alphafold_id': f"{session_id}_alphafold",
        'bound_id': f"{session_id}_bound",
    })


# ── Route 3: Serve uploaded PDB files to the 3D viewer ────────────
# The NGL viewer in the browser needs to fetch the PDB file as a URL
@app.route('/pdb/<filename>')
def serve_pdb(filename):
    from flask import send_from_directory
    return send_from_directory(UPLOAD_FOLDER, filename + '.pdb',
                               mimetype='text/plain')


# ── Start the server ──────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True, port=5000)
