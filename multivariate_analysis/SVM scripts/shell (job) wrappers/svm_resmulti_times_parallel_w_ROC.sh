#!/bin/bash

# File paths come from CONFIG.txt in the folder you ran qsub from (the repo root)
source "$SGE_O_WORKDIR/CONFIG.txt"

python3 "$CODE_DIR/multivariate_analysis/SVM scripts/python scripts/run_2fold_svm_resmulti_times_parallel_w_ROC.py" -5 10 $1
