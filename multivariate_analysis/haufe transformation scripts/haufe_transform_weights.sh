#!/bin/bash

# File paths come from CONFIG.txt in the folder you ran qsub from (the repo root)
source "$SGE_O_WORKDIR/CONFIG.txt"

python3 "$CODE_DIR/multivariate_analysis/haufe transformation scripts/haufe_transform_weights.py"
