import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

SUBMIT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "puberty_submit_scripts")
DATA_DIR = cfg["PUBERTY_DATA_DIR"]

if __name__ == "__main__":
    commands =[
        # Part A - discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_no_age"',
        # Part A - replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_no_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_timing_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_category_subjectkey_M_F.csv "pds_male_female_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_mf_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M_F.csv "hormone_ert_mf_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_mf_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M_F.csv "hormone_dhea_mf_no_age"',
        # Part B  - pds sex specific discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_ss_female_category_subjectkey_F.csv "pds_female_only_age" "F"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_ss_female_category_subjectkey_F.csv "pds_female_only_no_age" "F"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_ss_male_category_subjectkey_M.csv "pds_male_only_age" "M"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_pds_p_ss_male_category_subjectkey_M.csv "pds_male_only_no_age" "M"',
        # Part B - pds sex specific replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_ss_female_category_subjectkey_F.csv "pds_female_only_age" "F"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_ss_female_category_subjectkey_F.csv "pds_female_only_no_age" "F"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_ss_male_category_subjectkey_M.csv "pds_male_only_age" "M"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_pds_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_pds_p_ss_male_category_subjectkey_M.csv "pds_male_only_no_age" "M"',
        # Part B - hse hormone female only discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_hse_female_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_hse_mean_subjectkey_F.csv "hormone_hse_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_hse_female_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_hse_mean_subjectkey_F.csv "hormone_hse_female_only_no_age"',
        # Part B - hse horomone female only replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_hse_female_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_hse_mean_subjectkey_F.csv "hormone_hse_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_hse_female_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_hse_mean_subjectkey_F.csv "hormone_hse_female_only_no_age"',
        # Part B - ert hormone sex specific discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_F.csv "hormone_ert_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_F.csv "hormone_ert_female_only_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M.csv "hormone_ert_male_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_ert_mean_subjectkey_M.csv "hormone_ert_male_only_no_age"',
        # Part B - ert horomone sex specific replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_F.csv "hormone_ert_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_F.csv "hormone_ert_female_only_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M.csv "hormone_ert_male_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_ert_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_ert_mean_subjectkey_M.csv "hormone_ert_male_only_no_age"',
        # Part C - dhea hormone sex specific discovery
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_F.csv "hormone_dhea_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_F.csv "hormone_dhea_female_only_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M.csv "hormone_dhea_male_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_no_age.sh discovery {DATA_DIR}/discovery/discovery_behavior_hormone_scr_dhea_mean_subjectkey_M.csv "hormone_dhea_male_only_no_age"',
        # Part C - dhea horomone sex specific replication
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_F.csv "hormone_dhea_female_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_F.csv "hormone_dhea_female_only_no_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M.csv "hormone_dhea_male_only_age"',
        f'sbatch {SUBMIT_DIR}/gams_puberty_hormone_dhea_sex_specific_no_age.sh replication {DATA_DIR}/replication/replication_behavior_hormone_scr_dhea_mean_subjectkey_M.csv "hormone_dhea_male_only_no_age"'
    ]

    print(len(commands))
    for command in commands:
        os.system(command)