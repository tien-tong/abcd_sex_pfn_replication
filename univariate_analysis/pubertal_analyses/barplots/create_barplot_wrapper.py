import os

CREATE_BARPLOTS_R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "create_barplots.R")

if __name__ == "__main__":
    tests = ['hormone_ert_mf_oSex_age_mat.csv', 'hormone_ert_mf_oSex_no_age_mat.csv', 'pds_male_female_oSex_age_mat.csv',
             'pds_male_female_oSex_no_age_mat.csv', 'hormone_dhea_mf_oSex_age_mat.csv', 'hormone_dhea_mf_oSex_no_age_mat.csv']
    
    for test in tests:
        # Discovery matrices
        os.system(f"Rscript '{CREATE_BARPLOTS_R}' discovery {test}")
        # Replication matrices
        os.system(f"Rscript '{CREATE_BARPLOTS_R}' replication {test}")