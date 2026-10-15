"""ACE data, matched to the samples the same way as in the Part 3 GAM scripts:
baseline rows of ACE_CSV only, with subject IDs compared without their prefixes
(sample subjectkey: INV<id>; ACE csv src_subject_id: sub-<id>).

Scripts use it as:
    from ace_data import add_binarized_ace
    data_for_ridge = add_binarized_ace(pd.read_csv(cfg["DISCOVERY_SAMPLE_CSV"]))
"""
import pandas as pd
from pfn_config import cfg


def strip_id(ids):
    return pd.Series(ids).astype(str).str.replace(r"^(sub-)?(NDAR_?)?(INV)?", "", regex=True).values


def load_baseline_ace():
    """Baseline rows of ACE_CSV (all its columns), indexed by subject ID without its prefixes."""
    ace_df = pd.read_csv(cfg["ACE_CSV"])
    missing_cols = {"src_subject_id", "eventname", "binarizedACE"} - set(ace_df.columns)
    if missing_cols:
        raise ValueError(f"Missing column(s) {', '.join(sorted(missing_cols))} in {cfg['ACE_CSV']}")
    ace_df = ace_df[ace_df["eventname"] == "baseline_year_1_arm_1"]
    ace_df = ace_df.set_index(pd.Index(strip_id(ace_df["src_subject_id"])))
    if ace_df.index.duplicated().any():
        raise ValueError(f"More than one baseline row per subject in {cfg['ACE_CSV']}")
    return ace_df


def add_binarized_ace(data_for_ridge):
    """Return a copy of a sample csv's rows with a binarizedACE column (0/1, NaN if the subject has no baseline value).
    The rows keep the csv's order, which is also the row order of that sample's nonzero matrix."""
    ace = load_baseline_ace()["binarizedACE"]
    data_for_ridge = data_for_ridge.copy()
    data_for_ridge["binarizedACE"] = pd.to_numeric(ace.reindex(strip_id(data_for_ridge["subjectkey"])).values)
    if not data_for_ridge["binarizedACE"].dropna().isin([0, 1]).all():
        raise ValueError(f"binarizedACE must be 0/1 in {cfg['ACE_CSV']}")
    print(f"binarizedACE found for {data_for_ridge['binarizedACE'].notna().sum()} of {len(data_for_ridge)} subjects")
    return data_for_ridge
