import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

WRITE_EFFECT_MAP_TO_CIFTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "workbench setup scripts", "write_effect_map_to_cifti.py")

if __name__ == "__main__":
    for i in range(1, 18):
        os.system(f"python3 '{WRITE_EFFECT_MAP_TO_CIFTI}' '{cfg['INDIVIDUAL_NETWORK_DIR']}/individual_network_{i}_mat.csv' '{cfg['UNIVARIATE_DIR']}/network_{i}_sig_discovery.dscalar.nii'")
