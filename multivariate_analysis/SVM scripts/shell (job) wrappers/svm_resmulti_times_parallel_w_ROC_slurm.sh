#!/bin/bash
#SBATCH --mem=50G
#SBATCH --array=1-100
#SBATCH --time=1-00:00:00

# File paths come from CONFIG.txt in the folder you ran sbatch from (the repo root)
source "$SLURM_SUBMIT_DIR/CONFIG.txt"

python3 "$CODE_DIR/multivariate_analysis/SVM scripts/python scripts/run_2fold_svm_resmulti_times_parallel_w_ROC.py" -5 10 $SLURM_ARRAY_TASK_ID
