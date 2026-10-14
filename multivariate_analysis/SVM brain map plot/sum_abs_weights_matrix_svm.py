import pandas as pd
import numpy as np
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

def create_abs_sum_matrix(matrix_filename, save_filename):
    # Load in haufe transformed weight matrix of shape (17, 59412)
    weight_brain_matrix = np.load(matrix_filename)
    # Make values absolute values
    abs_weight_brain_matrix = abs(weight_brain_matrix)
    # Sum along the rows so resulting matrix is of size (59412, )
    sum_abs_weight_brain_matrix = np.sum(abs_weight_brain_matrix, axis=0)
    # Save matrix
    np.save(save_filename, sum_abs_weight_brain_matrix)
    print("Job done!")

if __name__ == "__main__":
    create_abs_sum_matrix(cfg["HAUFE_WEIGHTS_DISCOVERY_NPY"], cfg["SVM_ABS_SUM_DISCOVERY_NPY"])
    create_abs_sum_matrix(cfg["HAUFE_WEIGHTS_REPLICATION_NPY"], cfg["SVM_ABS_SUM_REPLICATION_NPY"])
