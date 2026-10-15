import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, roc_auc_score
import scipy.stats as st
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root
from ace_data import add_binarized_ace  # binarizedACE from ACE_CSV (baseline rows), as in the GAM scripts

def get_metrics(data_for_ridge, results_folder, set):
    # Only the subjects with a baseline binarizedACE were in the SVM
    data_for_ridge = data_for_ridge[data_for_ridge['binarizedACE'].notna()]
    # Use the data for ridge discovery subject ids as the ordering for the ids
    data_for_ridge_subject_ids = data_for_ridge['subjectkey'].values
    # also use data for ridge for binarizedACE (the SVM outcome: 0 = no, 1 = yes)
    data_for_ridge_ace = data_for_ridge['binarizedACE'].astype(int).values

    accuracies_all_runs = []
    balanced_accuracies_all_runs = []
    aucs_all_runs = []
    sensitivity_all_runs = []
    specificity_all_runs = []

    for i in range(1, 101):
        time_folder_path = f"{results_folder}/time_{i}"
        predicted_values_array = np.load(f"{time_folder_path}/{set}_predicted_values_2_folds.npy", allow_pickle=True)
        predicted_values_fold1 = list(predicted_values_array[0])
        predicted_values_fold2 = list(predicted_values_array[1])
        predicted_values_stacked = predicted_values_fold1 + predicted_values_fold2
        decision_values_array = np.load(f"{time_folder_path}/{set}_decision_values_2_folds.npy", allow_pickle=True)
        decision_values_stacked = list(decision_values_array[0]) + list(decision_values_array[1])

        # Load in the csv of the subject ids for each fold
        subject_ids_folds = pd.read_csv(f"{time_folder_path}/{set}_subject_ids_2_folds.csv")
        subject_ids_fold1 = list(subject_ids_folds['fold1_ids'].values)
        subject_ids_fold2 = list(subject_ids_folds['fold2_ids'].values)
        # Combine (stack) fold 1 and fold 2 decision values and id's
        subject_ids_stacked = subject_ids_fold1 + subject_ids_fold2
        # Remove the NaN that pads the shorter fold when the sample size is odd
        subject_ids_stacked = [id for id in subject_ids_stacked if not pd.isnull(id)]


        # Make df from stacked values (subject_id, decision_values)
        time_decision_values_df = pd.DataFrame()
        time_decision_values_df['subject_id'] = subject_ids_stacked
        time_decision_values_df['predicted_values'] = list(predicted_values_stacked)
        time_decision_values_df['decision_values'] = list(decision_values_stacked)

        # Loop through data for ridge ids and get decision values in order
        #print(time_decision_values_df)
        #print("Reordering predicted values....")
        predicted_values_in_order = []
        decision_values_in_order = []
        for subject_id in data_for_ridge_subject_ids:
            #print(subject_id)
            subject_row = time_decision_values_df[time_decision_values_df['subject_id'] == subject_id]
            predicted_values_in_order.append(subject_row['predicted_values'].values[0])
            decision_values_in_order.append(subject_row['decision_values'].values[0])

        # Calculate accuracy for run
        accuracy = accuracy_score(data_for_ridge_ace, predicted_values_in_order)
        accuracies_all_runs.append(accuracy)

        # Balanced accuracy (mean of sensitivity and specificity) and AUC (from the decision values) for run
        balanced_accuracies_all_runs.append(balanced_accuracy_score(data_for_ridge_ace, predicted_values_in_order))
        aucs_all_runs.append(roc_auc_score(data_for_ridge_ace, decision_values_in_order))

        # Calculate sensitivity (ACE = 1 detected) for run
        tn, fp, fn, tp = confusion_matrix(data_for_ridge_ace, predicted_values_in_order).ravel()
        sensitivity = tp / (tp + fn)
        sensitivity_all_runs.append(sensitivity)

        # Calculate specificity for run
        specificity = tn / (tn + fp)
        specificity_all_runs.append(specificity)

    return accuracies_all_runs, sensitivity_all_runs, specificity_all_runs, balanced_accuracies_all_runs, aucs_all_runs
    
def make_avg_table(save_file, set_order, accuracies, sensitivities, specificities, ci, balanced_accuracies, aucs):
    avg_table = pd.DataFrame()
    avg_table['set'] = set_order
    avg_table['Avg Accuracy'] = accuracies
    avg_table['Avg Sensitivity'] = sensitivities
    avg_table['Avg Specificity'] = specificities
    avg_table['95% CI'] = ci
    avg_table['Avg Balanced Accuracy'] = balanced_accuracies
    avg_table['Avg AUC'] = aucs
    avg_table.to_csv(save_file)


    
if __name__ == "__main__":
    discovery_data_for_ridge = add_binarized_ace(pd.read_csv(cfg["DISCOVERY_SAMPLE_CSV"]))
    res_multitimes_path = cfg["SVM_RESULTS_DIR"]
    avg_table_filename = cfg["SVM_METRICS_CSV"]
    accuracies_disc, sensitivity_disc, specificity_disc, balanced_accuracies_disc, aucs_disc = get_metrics(discovery_data_for_ridge, res_multitimes_path, "discovery")
    #print(accuracies_disc)
    print(f"Discovery - avg acc: {np.mean(accuracies_disc)}, CI: {st.t.interval(confidence=0.95, df=len(accuracies_disc)-1, loc=np.mean(accuracies_disc), scale=st.sem(accuracies_disc))}")
    print(f"Discovery - avg balanced acc: {np.mean(balanced_accuracies_disc)}, avg AUC: {np.mean(aucs_disc)}")


    replication_data_for_ridge = add_binarized_ace(pd.read_csv(cfg["REPLICATION_SAMPLE_CSV"]))
    accuracies_rep, sensitivity_rep, specificity_rep, balanced_accuracies_rep, aucs_rep = get_metrics(replication_data_for_ridge, res_multitimes_path, "replication")
    print(f"Replication - avg acc: {np.mean(accuracies_rep)}, CI: {st.t.interval(confidence=0.95, df=len(accuracies_rep)-1, loc=np.mean(accuracies_rep), scale=st.sem(accuracies_rep))}")
    print(f"Replication - avg balanced acc: {np.mean(balanced_accuracies_rep)}, avg AUC: {np.mean(aucs_rep)}")
    

    accuracies_100 = [np.mean(accuracies_disc), np.mean(accuracies_rep)]
    sensitivity_100 = [np.mean(sensitivity_disc), np.mean(sensitivity_rep)]
    specificity_100 = [np.mean(specificity_disc), np.mean(specificity_rep)]
    ci_100 = [str(st.t.interval(confidence=0.95, df=len(accuracies_disc)-1, loc=np.mean(accuracies_disc), scale=st.sem(accuracies_disc))), str(st.t.interval(confidence=0.95, df=len(accuracies_rep)-1, loc=np.mean(accuracies_rep), scale=st.sem(accuracies_rep)))]


    balanced_accuracy_100 = [np.mean(balanced_accuracies_disc), np.mean(balanced_accuracies_rep)]
    auc_100 = [np.mean(aucs_disc), np.mean(aucs_rep)]


    make_avg_table(avg_table_filename, ['discovery', 'replication'], accuracies_100, sensitivity_100, specificity_100, ci_100, balanced_accuracy_100, auc_100)

