# Drug Binding Visualization Tool

## Overview

This project analyzes how a drug molecule binds to a protein using structural biology data.

The workflow combines:

- AlphaFold predicted protein structures
- Experimental Protein Data Bank (PDB) structures
- Python structural analysis using Biopython
- Visualization using PyMOL

The project detects residues that form the binding pocket around the ligand.

---

## Biological Context

EGFR (Epidermal Growth Factor Receptor) plays a key role in cell signaling and growth.

Mutations in EGFR are associated with several cancers.

Understanding how drugs bind to EGFR helps researchers design targeted therapies.

---

## Project Workflow

1. Download AlphaFold predicted protein structure
2. Download experimental protein structure with bound ligand
3. Analyze structure using Python
4. Detect residues within 5 Å of the ligand
5. Generate structural visualizations
6. Create summary plots

---

## Technologies Used

- Python
- Biopython
- Pandas
- Matplotlib
- PyMOL
- GitHub

---

## Project Structure

```
drug-binding-visualization-tool
│
├── data
│   ├── alphafold
│   └── pdb
│
├── scripts
│   ├── analyze_structure.py
│   ├── find_binding_pocket.py
│   └── plot_summary.py
│
├── results
│   ├── structure_summary.csv
│   └── binding_pocket_residues.txt
│
├── images
│   ├── egfr_overview.png
│   ├── binding_pocket_zoom.png
│   ├── pocket_residues.png
│   └── structure_comparison.png
│
└── README.md
```

---

## Visualization

### Whole Protein Structure

![Protein Structure](images/egfr_overview.png)

---

### Drug Binding Pocket

![Binding Pocket](images/binding_pocket_zoom.png)

---

### Binding Pocket Residues

![Pocket Residues](images/pocket_residues.png)

---

### Structure Comparison Plot

![Structure Comparison](images/structure_comparison.png)

---

## Output Files

The scripts generate:

- `structure_summary.csv`
- `binding_pocket_residues.txt`

These contain structural metrics and detected binding pocket residues.

---

## Future Improvements

Possible extensions include:

- automatic ligand detection
- comparison across multiple inhibitors
- interactive 3D visualization
- machine learning analysis of binding interactions

---

## Author

Abhi K  
Biomedical / Mechanical Engineering Student