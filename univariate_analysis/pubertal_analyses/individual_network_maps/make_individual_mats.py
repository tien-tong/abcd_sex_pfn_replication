import os
import sys
import pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

if __name__ == "__main__":
    disc_matrices_folder = f"{cfg['PUBERTY_RESULTS_DIR']}/discovery"
    rep_matrices_folder = f"{cfg['PUBERTY_RESULTS_DIR']}/replication"
    disc_individual_networks_folder = f"{cfg['PUBERTY_INDIVIDUAL_NETWORK_DIR']}/discovery"
    rep_individual_networks_folder = f"{cfg['PUBERTY_INDIVIDUAL_NETWORK_DIR']}/replication"

    for folder_name in os.listdir(disc_matrices_folder):
        if not os.path.exists(f"{disc_individual_networks_folder}/{folder_name}"):
            os.mkdir(f"{disc_individual_networks_folder}/{folder_name}")
        
        if not os.path.exists(f"{rep_individual_networks_folder}/{folder_name}"):
            os.mkdir(f"{rep_individual_networks_folder}/{folder_name}")

        for network in range(1, 18):
            
            disc_result_filename = f"{disc_matrices_folder}/{folder_name}/SexEffect_AtlasLoading_Discovery_17_Network_{network}.csv"
            disc_network_matrix = pd.read_csv(disc_result_filename)
            disc_network_matrix['0'] = disc_network_matrix['Gam_Z_FDR_Sig_Vector_All']
            disc_network_matrix = disc_network_matrix['0']
            disc_network_matrix.to_csv(f"{disc_individual_networks_folder}/{folder_name}/network_{network}.csv", index=False)

            
            rep_result_filename = f"{rep_matrices_folder}/{folder_name}/SexEffect_AtlasLoading_Replication_17_Network_{network}.csv"
            rep_network_matrix = pd.read_csv(rep_result_filename)
            rep_network_matrix['0'] = rep_network_matrix['Gam_Z_FDR_Sig_Vector_All']
            rep_network_matrix = rep_network_matrix['0']
            rep_network_matrix.to_csv(f"{rep_individual_networks_folder}/{folder_name}/network_{network}.csv", index=False)



            
