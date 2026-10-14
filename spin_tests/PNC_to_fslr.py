import pandas as pd
from neuromaps import transforms
import nibabel as nib
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root


if __name__ == "__main__":
    os.environ["PATH"] += os.pathsep + os.path.dirname(cfg["WB_COMMAND"])
    pnc_gams_fslr = transforms.fsaverage_to_fslr((cfg["PNC_GAMS_ABS_SUM_LH_GII"], cfg["PNC_GAMS_ABS_SUM_RH_GII"]), target_density='32k')
    # pnc_gams_fslr = transforms.fsaverage_to_fslr(("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/spin_tests/data/PNC_data/GamSexAbssum_lh.gii", "/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/spin_tests/data/PNC_data/GamSexAbssum_rh.gii"), target_density='32k')
    pnc_gams_fslr_full_data = list(pnc_gams_fslr[0].agg_data()) + list(pnc_gams_fslr[1].agg_data()) 
    pnc_gams_fslr_full_gii = nib.gifti.gifti.GiftiImage()
    pnc_gams_fslr_full_gii.add_gifti_data_array(nib.gifti.gifti.GiftiDataArray(data=pnc_gams_fslr_full_data))
    nib.loadsave.save(pnc_gams_fslr_full_gii, cfg["PNC_GAMS_ABS_SUM_FSLR_GII"])

