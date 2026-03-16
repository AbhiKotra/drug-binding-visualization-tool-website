from Bio.PDB import PDBParser
import os
import pandas as pd
import sys

# ─────────────────────────────────────────────────────────────────
# This script now accepts file paths as arguments from app.py
# instead of having hardcoded filenames.
# Usage: python analyze_structure.py <alphafold.pdb> <bound.pdb> <results_dir>
# ─────────────────────────────────────────────────────────────────

def count_atoms_residues(pdb_file):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", pdb_file)

    atom_count = 0
    residue_count = 0
    chain_ids = set()

    for model in structure:
        for chain in model:
            chain_ids.add(chain.id)
            for residue in chain:
                residue_count += 1
                for atom in residue:
                    atom_count += 1

    return {
        "file": os.path.basename(pdb_file),
        "chains": len(chain_ids),
        "residues": residue_count,
        "atoms": atom_count
    }

# Get arguments passed in from app.py
# sys.argv[0] = this script's name (ignored)
# sys.argv[1] = path to alphafold PDB file
# sys.argv[2] = path to drug-bound PDB file
# sys.argv[3] = path to results folder
if len(sys.argv) < 4:
    print("Usage: python analyze_structure.py <alphafold.pdb> <bound.pdb> <results_dir>")
    sys.exit(1)

alphafold_path = sys.argv[1]
bound_path     = sys.argv[2]
results_dir    = sys.argv[3]

files = [alphafold_path, bound_path]
results = []

for f in files:
    if os.path.exists(f):
        results.append(count_atoms_residues(f))
    else:
        print(f"Missing file: {f}")

df = pd.DataFrame(results)

os.makedirs(results_dir, exist_ok=True)
csv_out = os.path.join(results_dir, "structure_summary.csv")
df.to_csv(csv_out, index=False)

print(df)
print("Saved results to", csv_out)
