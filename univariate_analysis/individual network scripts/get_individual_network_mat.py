import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

def get_individual_network_mat(all_networks_mat, network_num):
    individual_network_mat = all_networks_mat.iloc[network_num-1, :]
    filename = f"{cfg['INDIVIDUAL_NETWORK_DIR']}/individual_network_{network_num}_mat.csv"
    individual_network_mat.to_csv(filename, header=['0'], index=False)
    print(f"Network {network_num} matrix created!")

if __name__ == "__main__":
    discovery_gams_all_networks_mat = pd.read_csv(cfg["GAMS_BARPLOT_MAT_DISCOVERY_CSV"])
    if "Unnamed: 0" in discovery_gams_all_networks_mat.columns:
        discovery_gams_all_networks_mat = discovery_gams_all_networks_mat.drop(['Unnamed: 0'], axis=1)


    for i in range(1, 18):
        get_individual_network_mat(discovery_gams_all_networks_mat, i)
