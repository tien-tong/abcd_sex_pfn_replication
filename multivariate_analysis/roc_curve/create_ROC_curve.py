import pandas as pd
import numpy as np
import os
from sklearn.metrics import roc_curve, RocCurveDisplay, auc
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root
from ace_data import add_binarized_ace  # binarizedACE from ACE_CSV (baseline rows), as in the GAM scripts


def create_decision_df(data_for_ridge, res_multitimes_path):
    # Only the subjects with a baseline binarizedACE were in the SVM
    data_for_ridge = data_for_ridge[data_for_ridge['binarizedACE'].notna()]
    # Use the data for ridge discovery subject ids as the ordering for the ids
    data_for_ridge_subject_ids = data_for_ridge['subjectkey'].values
    # also use data for ridge for binarizedACE (the SVM outcome: 0 = no, 1 = yes)
    data_for_ridge_ace = data_for_ridge['binarizedACE'].astype(int).values

    # Make outer df to hold all the time decision values in order
    decision_values_all_runs_df = pd.DataFrame()
    # Fill subject id with data from ridge discovery subject ids
    decision_values_all_runs_df['subject_id'] = data_for_ridge_subject_ids
    # For each time folder
    print("Going through time folders....")
    for i in range(1, 101):
        time_folder_path = f"{res_multitimes_path}/time_{i}"
        # Load in the decision value arrays (fold1 first, fold2 second)
        decision_values_array = np.load(f"{time_folder_path}/discovery_decision_values_2_folds.npy", allow_pickle=True)
        decision_values_fold1 = list(decision_values_array[0])
        decision_values_fold2 = list(decision_values_array[1])
        decision_values_stacked = decision_values_fold1 + decision_values_fold2
        #print(decision_values_stacked)
        # Load in the csv of the subject ids for each fold
        subject_ids_folds = pd.read_csv(f"{time_folder_path}/discovery_subject_ids_2_folds.csv")
        subject_ids_fold1 = list(subject_ids_folds['fold1_ids'].values)
        subject_ids_fold2 = list(subject_ids_folds['fold2_ids'].values)
        # Combine (stack) fold 1 and fold 2 decision values and id's
        subject_ids_stacked = subject_ids_fold1 + subject_ids_fold2
        # Remove the NaN that pads the shorter fold when the sample size is odd
        subject_ids_stacked = [id for id in subject_ids_stacked if not pd.isnull(id)]
        #print(subject_ids_stacked)
        # Make df from stacked values (subject_id, decision_values)
        time_decision_values_df = pd.DataFrame()
        time_decision_values_df['subject_id'] = subject_ids_stacked
        time_decision_values_df['decision_values'] = list(decision_values_stacked)

        # Loop through data for ridge ids and get decision values in order
        #print(time_decision_values_df)
        print("Reordering decision values....")
        decision_values_in_order = []
        for subject_id in data_for_ridge_subject_ids:
            #print(subject_id)
            decision_value = time_decision_values_df[time_decision_values_df['subject_id'] == subject_id]['decision_values'].values[0]
            decision_values_in_order.append(decision_value)
        
        decision_values_all_runs_df[f"time_{i}"] = decision_values_in_order

    return decision_values_all_runs_df, data_for_ridge_ace


def create_decision_df_replication(data_for_ridge, res_multitimes_path):
    # Only the subjects with a baseline binarizedACE were in the SVM
    data_for_ridge = data_for_ridge[data_for_ridge['binarizedACE'].notna()]
    # Use the data for ridge discovery subject ids as the ordering for the ids
    data_for_ridge_subject_ids = data_for_ridge['subjectkey'].values
    # also use data for ridge for binarizedACE (the SVM outcome: 0 = no, 1 = yes)
    data_for_ridge_ace = data_for_ridge['binarizedACE'].astype(int).values

    # Make outer df to hold all the time decision values in order
    decision_values_all_runs_df = pd.DataFrame()
    # Fill subject id with data from ridge discovery subject ids
    decision_values_all_runs_df['subject_id'] = data_for_ridge_subject_ids

     # For each time folder
    print("Going through time folders....")
    for i in range(1, 101):
        time_folder_path = f"{res_multitimes_path}/time_{i}"
        # Load in the decision value arrays (fold1 first, fold2 second)
        decision_values_array = np.load(f"{time_folder_path}/replication_decision_values_2_folds.npy", allow_pickle=True)
        decision_values_fold1 = list(decision_values_array[0])
        decision_values_fold2 = list(decision_values_array[1])
        decision_values_stacked = decision_values_fold1 + decision_values_fold2

        # Load in the csv of the subject ids for each fold
        subject_ids_folds = pd.read_csv(f"{time_folder_path}/replication_subject_ids_2_folds.csv")
        subject_ids_fold1 = list(subject_ids_folds['fold1_ids'].values)
        subject_ids_fold2 = list(subject_ids_folds['fold2_ids'].values)
        # Combine (stack) fold 1 and fold 2 decision values and id's
        subject_ids_stacked = subject_ids_fold1 + subject_ids_fold2
        # Remove the NaN that pads the shorter fold when the sample size is odd
        subject_ids_final = [id for id in subject_ids_stacked if not pd.isnull(id)]

        # Make df from stacked values (subject_id, decision_values)
        time_decision_values_df = pd.DataFrame()
        time_decision_values_df['subject_id'] = subject_ids_final
        time_decision_values_df['decision_values'] = list(decision_values_stacked)

        # Loop through data for ridge ids and get decision values in order
        #print(time_decision_values_df)
        print("Reordering decision values....")
        decision_values_in_order = []
        #print(data_for_ridge_subject_ids)
        for subject_id in data_for_ridge_subject_ids:
            #print(subject_id)
            decision_value = time_decision_values_df[time_decision_values_df['subject_id'] == subject_id]['decision_values'].values[0]
            decision_values_in_order.append(decision_value)
        
        decision_values_all_runs_df[f"time_{i}"] = decision_values_in_order

    return decision_values_all_runs_df, data_for_ridge_ace



def plot_ROC_curve(ace, decision_values_df, save_filepath_png, save_filepath_df):
    print("Plotting ROC curve....")
    decision_values_df = decision_values_df.drop(['subject_id'], axis=1)
    decision_values = np.array(decision_values_df).mean(axis=1)
    
    roc_df = pd.DataFrame()
    roc_df['binarizedACE'] = ace
    roc_df['decision_values'] = decision_values
    roc_df.to_csv(save_filepath_df)

    fpr, tpr, thresholds = roc_curve(ace, decision_values)
    roc_auc = auc(fpr, tpr)
    print(f"AUC: {roc_auc}")
    display = RocCurveDisplay(fpr=fpr, tpr=tpr)
    display.plot()
    plt.rcParams.update({'font.size': 16})
    plt.legend().remove()
    plt.savefig(save_filepath_png)
    return roc_auc



if __name__ == "__main__":
    res_multitimes_path = cfg["SVM_RESULTS_DIR"]

    discovery_data_for_ridge = add_binarized_ace(pd.read_csv(cfg["DISCOVERY_SAMPLE_CSV"]))
    save_filepath = f"{cfg['SVM_OUTPUT_DIR']}/discovery_svm_ROC_siblings_removed_adjusted_font_check.png"
    save_filepath_df = cfg["ROC_DATA_DISCOVERY_CSV"]
    discovery_decision_df, ace = create_decision_df(discovery_data_for_ridge, res_multitimes_path)
    discovery_auc = plot_ROC_curve(ace, discovery_decision_df, save_filepath, save_filepath_df)

    replication_data_for_ridge = add_binarized_ace(pd.read_csv(cfg["REPLICATION_SAMPLE_CSV"]))
    save_filepath_replication = f"{cfg['SVM_OUTPUT_DIR']}/replication_svm_ROC_siblings_removed_adjusted_font_check.png"
    save_filepath_replication_df = cfg["ROC_DATA_REPLICATION_CSV"]
    replication_decision_df, rep_ace = create_decision_df_replication(replication_data_for_ridge, res_multitimes_path)
    replication_auc = plot_ROC_curve(rep_ace, replication_decision_df, save_filepath_replication, save_filepath_replication_df)

    auc_scores = pd.DataFrame()
    auc_scores['set'] = ['discovery', 'replication']
    auc_scores['auc'] = [discovery_auc, replication_auc]

    auc_scores.to_csv(f"{cfg['SVM_OUTPUT_DIR']}/auc_scores_svm_100_runs_check.csv")




