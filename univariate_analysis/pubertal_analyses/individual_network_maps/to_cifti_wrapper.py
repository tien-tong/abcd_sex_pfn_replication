import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

WRITE_EFFECT_MAP_TO_CIFTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "abs_sum_maps", "write_effect_map_to_cifti.py")

if __name__ == "__main__":
    disc_matrices_folders = f"{cfg['PUBERTY_INDIVIDUAL_NETWORK_DIR']}/discovery"
    rep_matrices_folders = f"{cfg['PUBERTY_INDIVIDUAL_NETWORK_DIR']}/replication"
    for folder in os.listdir(disc_matrices_folders):
        for i in range(1, 18):
            disc_filepath = f"{disc_matrices_folders}/{folder}/network_{i}.csv"
            rep_filepath = f"{rep_matrices_folders}/{folder}/network_{i}.csv"
            os.system(f"python3 '{WRITE_EFFECT_MAP_TO_CIFTI}' '{disc_filepath}' '{disc_matrices_folders}/{folder}/network_{i}.dscalar.nii'")
            os.system(f"python3 '{WRITE_EFFECT_MAP_TO_CIFTI}' '{rep_filepath}' '{rep_matrices_folders}/{folder}/network_{i}.dscalar.nii'")
