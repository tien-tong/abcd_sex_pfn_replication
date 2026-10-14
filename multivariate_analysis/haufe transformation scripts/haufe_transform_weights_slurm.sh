#!/bin/bash
#SBATCH --mem=500G
#SBATCH --time=12:00:00

# File paths come from CONFIG.txt in the folder you ran sbatch from (the repo root)
source "$SLURM_SUBMIT_DIR/CONFIG.txt"

python3 "$CODE_DIR/multivariate_analysis/haufe transformation scripts/haufe_transform_weights.py"
