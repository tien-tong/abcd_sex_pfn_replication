import pandas as pd
import numpy as np
import h5py
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

def create_network_matrices(data_for_ridge, discovery):
    data_for_ridge = pd.read_csv(data_for_ridge)
    subject_keys = data_for_ridge['subjectkey']
    for i in range(17):
        print(f"Creating network {i+1} matrix....")
        network_matrix = np.zeros((len(subject_keys), 59412))
        for j in range(len(subject_keys)):
            filename = f"{cfg['SUBJECT_DATA_DIR']}/sub-NDAR{subject_keys[j]}/IndividualParcel_Final_sbj1_comp17_alphaS21_1_alphaL300_vxInfo1_ard0_eta0/final_UV.mat"
            subject_loadings = h5py.File(filename, "r")['#refs#']['c'][()][i,:]
            network_matrix[j,] = subject_loadings

        network_matrix_nonzero_array = network_matrix[:, network_matrix.any(0)]
        if discovery == "discovery":
            save_matrix_filepath = f"{cfg['NETWORK_SPECIFIC_MATRICES_DIR']}/discovery_network_matrix_nonzero_{i+1}.npy"
        else:
            save_matrix_filepath = f"{cfg['NETWORK_SPECIFIC_MATRICES_DIR']}/replication_network_matrix_nonzero_{i+1}.npy"

        print(f"Size of matrix: {network_matrix_nonzero_array.shape}")
        np.save(save_matrix_filepath, network_matrix_nonzero_array)
        
        if discovery == "discovery":
            save_indices_filepath =  f"{cfg['NETWORK_SPECIFIC_MATRICES_DIR']}/discovery_nonzero_indices_network_{i+1}.npy"
        else:
            save_indices_filepath =  f"{cfg['NETWORK_SPECIFIC_MATRICES_DIR']}/replication_nonzero_indices_network_{i+1}.npy"
        nonzero_inds_df = pd.DataFrame()
        nonzero_inds_df['nonzero_indices'] = np.nonzero(np.any(network_matrix != 0, axis=0))[0]
        nonzero_inds_df.to_csv(save_indices_filepath)
    

if __name__ == "__main__":
    data_for_ridge_discovery = cfg["DISCOVERY_SAMPLE_CSV"]
    discovery_or_replication = "discovery"
    create_network_matrices(data_for_ridge_discovery, discovery=discovery_or_replication)

    data_for_ridge_replication = cfg["REPLICATION_SAMPLE_CSV"]
    discovery_or_replication = "replication"
    create_network_matrices(data_for_ridge_replication, discovery=discovery_or_replication)
    