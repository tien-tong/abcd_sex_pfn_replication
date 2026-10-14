import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

def create_behavior_df(original_df, df_to_merge, indepdent_vars, sexes, set):
    f = open(f"{cfg['PUBERTY_DATA_DIR']}/puberty_dataframe_shapes.txt", "a+")
    df_to_merge = df_to_merge[df_to_merge['eventname'] == "baseline_year_1_arm_1"]
    df_to_merge_ids = [sub_id[5:] for sub_id in df_to_merge['src_subject_id'].values]
    df_to_merge['subjectkey'] = df_to_merge_ids
    if len(indepdent_vars) == 2:
        print(indepdent_vars)
        print("IN HERE")
        pds_p_category = []
        for i in range(len(df_to_merge['pds_p_ss_female_category'])):
            if not pd.isnull(df_to_merge['pds_p_ss_female_category'].values[i]) and pd.isnull(df_to_merge['pds_p_ss_male_category'].values[i]) and original_df[original_df['subjectkey'] == df_to_merge['subjectkey'].values[i]]['sex'].values == "F":
                pds_p_category.append(df_to_merge['pds_p_ss_female_category'].values[i])
            elif pd.isnull(df_to_merge['pds_p_ss_female_category'].values[i]) and not pd.isnull(df_to_merge['pds_p_ss_male_category'].values[i]) and original_df[original_df['subjectkey'] == df_to_merge['subjectkey'].values[i]]['sex'].values == "M":
                pds_p_category.append(df_to_merge['pds_p_ss_male_category'].values[i])
            else:
                pds_p_category.append(None)
        df_to_merge['pds_p_category']= pds_p_category
        df_to_merge_final = df_to_merge[['pds_p_category', 'subjectkey']]
        indepdent_vars = df_to_merge_final.columns
    else:
        print("HERE")
        indepdent_vars.append('subjectkey')
        df_to_merge_final = df_to_merge[indepdent_vars]
    
    
    df_to_merge_final = df_to_merge_final.dropna()

    behavior_merged_df = original_df.merge(df_to_merge_final, on='subjectkey', how='inner')
    print(behavior_merged_df)
    behavior_df_final = behavior_merged_df[behavior_merged_df['sex'].isin(sexes)]
    behavior_df_final = behavior_df_final.drop(["Unnamed: 0.1", "Unnamed: 0"], axis=1)
    filename = f"{set}_behavior_{'_'.join(indepdent_vars)}_{'_'.join(sexes)}.csv"
    f.write(f"File: {filename}\n")
    f.write(f"Dataframe shape: {behavior_df_final.shape}\n\n")
    behavior_df_filename = f"{cfg['PUBERTY_DATA_DIR']}/{set}/{filename}"
    behavior_df_final.to_csv(behavior_df_filename, index=False)
    f.close()


if __name__ == "__main__":
    discovery_set = pd.read_csv(cfg["DISCOVERY_SAMPLE_CSV"])
    replication_set = pd.read_csv(cfg["REPLICATION_SAMPLE_CSV"])

    hormone_data = pd.read_csv(cfg["HORMONE_CSV"])
    pds_data = pd.read_csv(cfg["PDS_CSV"])
    dhea_data = pd.read_csv(cfg["DHEA_TXT"], sep='\t')
    dhea_data = dhea_data.drop([0], axis=0)
    
    # Make datasets for  discovery and replication sets separately while controlling for 1) pubertal stage, 2) pubertal timing, and 3) testosterone
    create_behavior_df(discovery_set, pds_data, ['pds_p_ss_female_category', 'pds_p_ss_male_category'], ['M', 'F'], "discovery")
    create_behavior_df(replication_set, pds_data, ['pds_p_ss_female_category', 'pds_p_ss_male_category'], ['M', 'F'], "replication")
    create_behavior_df(discovery_set, hormone_data, ['hormone_scr_ert_mean'], ['M', 'F'], "discovery")
    create_behavior_df(replication_set, hormone_data, ['hormone_scr_ert_mean'], ['M', 'F'], "replication")
    create_behavior_df(discovery_set, dhea_data, ['hormone_scr_dhea_mean'], ['M', 'F'], "discovery")
    create_behavior_df(replication_set, dhea_data, ['hormone_scr_dhea_mean'], ['M', 'F'], "replication")


    # pds females only
    create_behavior_df(discovery_set, pds_data, ['pds_p_ss_female_category'], ['F'], "discovery")
    create_behavior_df(replication_set, pds_data, ['pds_p_ss_female_category'], ['F'], "replication")
    # pds males only
    create_behavior_df(discovery_set, pds_data, ['pds_p_ss_male_category'], ['M'], "discovery")
    create_behavior_df(replication_set, pds_data, ['pds_p_ss_male_category'], ['M'], "replication")

    # hormone hse females only
    create_behavior_df(discovery_set, hormone_data, ['hormone_scr_hse_mean'], ['F'], "discovery")
    create_behavior_df(replication_set, hormone_data, ['hormone_scr_hse_mean'], ['F'], "replication")

    # hormone ert males only
    create_behavior_df(discovery_set, hormone_data, ['hormone_scr_ert_mean'], ['M'], "discovery")
    create_behavior_df(replication_set, hormone_data, ['hormone_scr_ert_mean'], ['M'], "replication")

    # hormone ert females only
    create_behavior_df(discovery_set, hormone_data, ['hormone_scr_ert_mean'], ['F'], "discovery")
    create_behavior_df(replication_set, hormone_data, ['hormone_scr_ert_mean'], ['F'], "replication")

    # hormone dhea males only
    create_behavior_df(discovery_set, dhea_data, ['hormone_scr_dhea_mean'], ['M'], "discovery")
    create_behavior_df(replication_set, dhea_data, ['hormone_scr_dhea_mean'], ['M'], "replication")

    # hormone dhea females only
    create_behavior_df(discovery_set, dhea_data, ['hormone_scr_dhea_mean'], ['F'], "discovery")
    create_behavior_df(replication_set, dhea_data, ['hormone_scr_dhea_mean'], ['F'], "replication")
