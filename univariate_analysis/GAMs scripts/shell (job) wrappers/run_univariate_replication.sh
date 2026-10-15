#!/bin/bash

# Find CONFIG.txt from this script's own location, so sbatch works from any folder
# (SLURM runs a copy of the script; the original path comes from scontrol)
script="${BASH_SOURCE[0]}"
[ -n "$SLURM_JOB_ID" ] && script=$(scontrol show job "$SLURM_JOB_ID" 2>/dev/null | sed -n 's/^ *Command=\(.*\.sh\).*/\1/p')
[ -n "$script" ] || script="${SLURM_SUBMIT_DIR:-$PWD}/job"
[ "${script#/}" = "$script" ] && script="${SLURM_SUBMIT_DIR:-$PWD}/$script"
repo=$(dirname "$script"); while [ ! -f "$repo/CONFIG.txt" ] && [ "$repo" != / ]; do repo=$(dirname "$repo"); done
source "$repo/CONFIG.txt"
# Conda environment from setup_env.sh (CONDA_BASE / CONDA_ENV in CONFIG.txt)
source "$CONDA_BASE/bin/activate" "$CONDA_ENV"

singularity run --cleanenv --bind "$PROJECT_DIR" \
    "$CONTAINER_SIF" \
    Rscript --save "$CODE_DIR/univariate_analysis/GAMs scripts/R scripts/abcd_univariate_analysis_replication.R"
