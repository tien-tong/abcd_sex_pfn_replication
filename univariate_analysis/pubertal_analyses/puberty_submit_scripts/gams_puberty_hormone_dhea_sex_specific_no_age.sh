#!/bin/bash
#SBATCH --propagate=NONE
#SBATCH --mem=50G
#SBATCH --time=1-00:00:00

# File paths come from CONFIG.txt in the folder you ran sbatch from (the repo root)
source "$SLURM_SUBMIT_DIR/CONFIG.txt"

set=$1
behavior_csv=$2
test_name=$3


singularity run --cleanenv \
    "$CONTAINER_SIF" \
    Rscript --save "$CODE_DIR/univariate_analysis/pubertal_analyses/puberty_scripts/abcd_puberty_hormones.R" $set "$behavior_csv" $test_name FALSE dhea FALSE