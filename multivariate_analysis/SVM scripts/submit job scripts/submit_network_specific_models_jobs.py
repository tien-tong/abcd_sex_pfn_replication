import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

SLURM_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "shell (job) wrappers", "network_specific_models_slurm.sh")

if __name__ == "__main__":
    results_folder = cfg["NETWORK_SPECIFIC_RESULTS_DIR"]
    for i in range(1, 18):
        if not os.path.exists(f"{results_folder}/network_{i}"):
            os.mkdir(f"{results_folder}/network_{i}")

        os.system(f"sbatch '{SLURM_SCRIPT}' {i}")
