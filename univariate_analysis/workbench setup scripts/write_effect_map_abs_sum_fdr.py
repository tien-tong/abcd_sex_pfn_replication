import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

def create_abs_sum_mat(results_folder, sample_type, save_filename):
    all_z_vectors = pd.DataFrame()
    network = 1
    for i in range(17):
        if sample_type == "discovery":
            result_filename = f"{results_folder}/SexEffect_AtlasLoading_Discovery_17_Network_{network}.csv"
        else:
            result_filename = f"{results_folder}/SexEffect_AtlasLoading_Replication_17_Network_{network}.csv"
        network_matrix = pd.read_csv(result_filename)
        network_matrix = network_matrix['Gam_Z_FDR_Sig_Vector_All']
        all_z_vectors[f"network_{network}"] = abs(network_matrix)
        network += 1
        
    
    network_abs_sum = all_z_vectors.sum(axis=1)
    network_abs_sum.to_csv(save_filename, index=False)
    print("Job Done!")


if __name__ == "__main__":
    create_abs_sum_mat(cfg["GAMS_DISCOVERY_DIR"], "discovery", cfg["GAMS_FDR_ABS_SUM_DISCOVERY_CSV"])
    create_abs_sum_mat(cfg["GAMS_REPLICATION_DIR"], "replication", cfg["GAMS_FDR_ABS_SUM_REPLICATION_CSV"])



