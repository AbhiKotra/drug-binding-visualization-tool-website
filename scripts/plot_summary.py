import pandas as pd
import matplotlib
matplotlib.use('Agg')   # IMPORTANT: use non-interactive backend so it works on a server (no display needed)
import matplotlib.pyplot as plt
import os
import sys

# ─────────────────────────────────────────────────────────────────
# Usage: python plot_summary.py <results_dir> <images_dir>
# ─────────────────────────────────────────────────────────────────

if len(sys.argv) < 3:
    print("Usage: python plot_summary.py <results_dir> <images_dir>")
    sys.exit(1)

results_dir = sys.argv[1]
images_dir  = sys.argv[2]

csv_file     = os.path.join(results_dir, "structure_summary.csv")
output_image = os.path.join(images_dir,  "structure_comparison.png")

os.makedirs(images_dir, exist_ok=True)

df = pd.read_csv(csv_file)

# ── Plot 1: Atom count comparison ──────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(14, 5))
fig.suptitle("Structure Comparison Summary", fontsize=14, fontweight='bold')

colors = ['#2196F3', '#FF5722']

axes[0].bar(df["file"], df["atoms"], color=colors)
axes[0].set_title("Atom Count")
axes[0].set_ylabel("Number of Atoms")
axes[0].tick_params(axis='x', rotation=15)

axes[1].bar(df["file"], df["residues"], color=colors)
axes[1].set_title("Residue Count")
axes[1].set_ylabel("Number of Residues")
axes[1].tick_params(axis='x', rotation=15)

axes[2].bar(df["file"], df["chains"], color=colors)
axes[2].set_title("Chain Count")
axes[2].set_ylabel("Number of Chains")
axes[2].tick_params(axis='x', rotation=15)

plt.tight_layout()
plt.savefig(output_image, dpi=150)
plt.close()

print("Saved plot to:", output_image)
