import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

SUBMIT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puberty_submit_scripts")
DATA_DIR = cfg["PUBERTY_DATA_DIR"]

if __name__ == "__main__":
    commands =[
        # Part A - discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_oSex_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_oSex_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_oSex_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_oSex_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_oSex_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_oSex_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_oSex_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_oSex_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_oSex_no_age"',
        # Part A - replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_oSex_no_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_oSex_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_oSex_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_oSex_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_oSex_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_oSex_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_oSex_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_oSex_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_oSex_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_oSex_no_age"'
    ]

    print(len(commands))
    for command in commands:
        os.system(command)