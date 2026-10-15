#!/bin/bash

# File paths come from CONFIG.txt in the folder you ran qsub from (the repo root)
source "$SGE_O_WORKDIR/CONFIG.txt"
# Conda environment from setup_env.sh (CONDA_BASE / CONDA_ENV in CONFIG.txt)
source "$CONDA_BASE/bin/activate" "$CONDA_ENV"

python3 "$CODE_DIR/multivariate_analysis/haufe transformation scripts/haufe_transform_weights.py"
