#!/bin/bash

# File paths come from CONFIG.txt in the folder you ran sbatch from (the repo root)
source "$SLURM_SUBMIT_DIR/CONFIG.txt"

singularity run --cleanenv \
    "$CONTAINER_SIF" \
    Rscript --save "$CODE_DIR/univariate_analysis/GAMs scripts/R scripts/abcd_univariate_analysis.R"
