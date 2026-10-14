import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

WRITE_EFFECT_MAP_TO_CIFTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "write_effect_map_to_cifti.py")

if __name__ == "__main__":
    disc_mats_path = f"{cfg['PUBERTY_ABS_SUM_DIR']}/matrices/discovery"
    rep_mats_path = f"{cfg['PUBERTY_ABS_SUM_DIR']}/matrices/replication"
    cifti_path = f"{cfg['PUBERTY_ABS_SUM_DIR']}/cifti_files"
    disc_mats = os.listdir(disc_mats_path)
    rep_mats = os.listdir(rep_mats_path)
    for mat in disc_mats:
        os.system(f"python3 '{WRITE_EFFECT_MAP_TO_CIFTI}' '{disc_mats_path}/{mat}' '{cifti_path}/discovery/{mat[0:len(mat)-4]}.dscalar.nii'")
        os.system(f"python3 '{WRITE_EFFECT_MAP_TO_CIFTI}' '{rep_mats_path}/{mat}' '{cifti_path}/replication/{mat[0:len(mat)-4]}.dscalar.nii'")
