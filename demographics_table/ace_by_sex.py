"""ACE by sex in the full sample (discovery + replication), for the grant report.

Saves to ACE_BY_SEX_DIR:
- aces_proxy_histogram_by_sex.png/.pdf: histogram of aces_proxy, males and females overlaid
- ace_subtypes_violin_by_sex.png/.pdf: violin plot of each ACE subtype by sex, * where p < .05
- ace_subtypes_ttest_by_sex.csv: t-test of each ACE subtype by sex (Welch's, the default of R's t.test),
  no correction for multiple comparisons; t > 0 means a higher mean in females

ACE values are the baseline rows of ACE_CSV, matched to the samples as in the GAM and SVM scripts.
Usage: python3 demographics_table/ace_by_sex.py
"""
import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root
from ace_data import load_baseline_ace, strip_id  # baseline rows of ACE_CSV, as in the GAM and SVM scripts

SUBTYPES = ["abuse_phy", "abuse_sex", "abuse_emo", "neglect_phy", "neglect_emo",
            "divorce", "violence", "mental", "incar", "sud"]
SEXES = [("M", "Male", "tab:blue"), ("F", "Female", "hotpink")]  # (code in the sample csv, label, color)
ALPHA = 0.05


def load_full_sample():
    # Discovery + replication samples with each subject's baseline ACE scores (NaN if the subject has none)
    sample = pd.concat([pd.read_csv(cfg["DISCOVERY_SAMPLE_CSV"]), pd.read_csv(cfg["REPLICATION_SAMPLE_CSV"])], ignore_index=True)
    sample = sample.drop_duplicates("subjectkey")[["subjectkey", "sex"]]
    ace = load_baseline_ace()
    missing_cols = set(["aces_proxy"] + SUBTYPES) - set(ace.columns)
    if missing_cols:
        raise ValueError(f"Missing column(s) {', '.join(sorted(missing_cols))} in {cfg['ACE_CSV']}")
    ace = ace.reindex(strip_id(sample["subjectkey"]))
    for col in ["aces_proxy"] + SUBTYPES:
        sample[col] = pd.to_numeric(ace[col]).values

    print(f"Full sample: {len(sample)} subjects; with a baseline aces_proxy: "
          + ", ".join(f"{label} {sample.loc[sample['sex'] == code, 'aces_proxy'].notna().sum()}" for code, label, _ in SEXES))
    return sample


def ttest_by_sex(sample):
    rows = []
    for subtype in SUBTYPES:
        male = sample.loc[sample["sex"] == "M", subtype].dropna()
        female = sample.loc[sample["sex"] == "F", subtype].dropna()
        result = stats.ttest_ind(female, male, equal_var=False)
        rows.append({"subtype": subtype,
                     "n_female": len(female), "mean_female": female.mean(), "sd_female": female.std(),
                     "n_male": len(male), "mean_male": male.mean(), "sd_male": male.std(),
                     "t": result.statistic, "df": result.df, "p": result.pvalue,
                     "significant": result.pvalue < ALPHA})
    return pd.DataFrame(rows)


def save_figure(fig, save_path_no_ext):
    for ext in [".png", ".pdf"]:
        fig.savefig(save_path_no_ext + ext, dpi=300)
    plt.close(fig)


def plot_aces_proxy_histogram(sample, save_path_no_ext):
    values = sample["aces_proxy"].dropna()
    if np.allclose(values, np.round(values)):  # whole-number scores: one bar per value
        bins = np.arange(values.min() - 0.5, values.max() + 1.5)
    else:
        bins = np.histogram_bin_edges(values, bins="auto")

    fig, ax = plt.subplots(figsize=(5, 3.5))
    for code, label, color in SEXES:
        sex_values = sample.loc[sample["sex"] == code, "aces_proxy"].dropna()
        ax.hist(sex_values, bins=bins, color=color, alpha=0.5, label=f"{label} (n = {len(sex_values)})")
    ax.set_xlabel("aces_proxy")
    ax.set_ylabel("Count")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_figure(fig, save_path_no_ext)


def plot_subtype_violins(sample, ttests, save_path_no_ext):
    significant = ttests.set_index("subtype")["significant"]
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    for ax, subtype in zip(axes.flat, SUBTYPES):
        data = [sample.loc[sample["sex"] == code, subtype].dropna() for code, _, _ in SEXES]
        parts = ax.violinplot(data, positions=[1, 2], showmeans=True, showextrema=False)
        for body, (_, _, color) in zip(parts["bodies"], SEXES):
            body.set_facecolor(color)
            body.set_edgecolor(color)
            body.set_alpha(0.6)
        parts["cmeans"].set_color("black")
        ax.set_xticks([1, 2], [label for _, label, _ in SEXES])
        ax.set_title(subtype)
        ax.spines[["top", "right"]].set_visible(False)

        if significant[subtype]:
            # bracket between the two violins with a * above it
            low = min(d.min() for d in data)
            high = max(d.max() for d in data)
            step = (high - low or 1) * 0.08
            ax.plot([1, 1, 2, 2], [high + step, high + 1.5 * step, high + 1.5 * step, high + step], color="black", linewidth=1)
            ax.text(1.5, high + 1.6 * step, "*", ha="center", va="bottom", fontsize=16)
            ax.set_ylim(top=high + 3 * step)
    fig.tight_layout()
    save_figure(fig, save_path_no_ext)


if __name__ == "__main__":
    out_dir = cfg["ACE_BY_SEX_DIR"]
    os.makedirs(out_dir, exist_ok=True)
    sample = load_full_sample()

    ttests = ttest_by_sex(sample)
    ttests.to_csv(os.path.join(out_dir, "ace_subtypes_ttest_by_sex.csv"), index=False)
    print(f"\nWelch t-tests, female vs male (t > 0: higher in females), p < {ALPHA} uncorrected:")
    print(ttests.to_string(index=False, float_format=lambda x: f"{x:.4g}"))

    plot_aces_proxy_histogram(sample, os.path.join(out_dir, "aces_proxy_histogram_by_sex"))
    plot_subtype_violins(sample, ttests, os.path.join(out_dir, "ace_subtypes_violin_by_sex"))
    print(f"\nSaved to {out_dir}")
