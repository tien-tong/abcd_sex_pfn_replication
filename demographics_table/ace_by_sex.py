"""ACE by sex in the full sample (discovery + replication), for the grant report.

Saves to ACE_BY_SEX_DIR:
- aces_proxy_histogram_by_sex.png/.pdf: histogram of aces_proxy, males and females side by side (% of each sex)
- ace_subtypes_mean_se_by_sex.png/.pdf: mean +/- SE of each ACE subtype by sex, * where p < .05
- ace_subtypes_ttest_by_sex.csv: t-test of each ACE subtype by sex (Welch's, the default of R's t.test),
  no correction for multiple comparisons; t > 0 means a higher mean in females

ACE values are the baseline rows of ACE_CSV, matched to the samples as in the GAM and SVM scripts.
Usage: python3 demographics_table/ace_by_sex.py
"""
import os
import sys
import textwrap
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root
from ace_data import load_baseline_ace, strip_id  # baseline rows of ACE_CSV, as in the GAM and SVM scripts

# ACE subtype columns and their full names, from the comments in the ACEs proxy scoring script
# (ELAfromABCD_ACEsproxy_revised.Rmd; it gives no full name for abuse_emo)
SUBTYPE_NAMES = {"abuse_phy": "Physical abuse", "abuse_sex": "Sexual abuse", "abuse_emo": "Emotional abuse",
                 "neglect_phy": "Physical neglect", "neglect_emo": "Emotional neglect",
                 "divorce": "Parents separated or divorced", "violence": "Violence in home",
                 "mental": "Family mental illness", "incar": "Incarcerated relative", "sud": "Family substance use"}
SUBTYPES = list(SUBTYPE_NAMES)
# (code in the sample csv, label, color); colors are the two ends of the pink-white-teal colorbar
SEXES = [("M", "Male", "#479CA2"), ("F", "Female", "#DD5584")]
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
    # Males and females side by side in each bin, as the % of that sex, so neither group hides the other
    values = sample["aces_proxy"].dropna()
    whole_numbers = np.allclose(values, np.round(values))
    if whole_numbers:  # one bin per score
        bins = np.arange(values.min() - 0.5, values.max() + 1.5)
    else:
        bins = np.histogram_bin_edges(values, bins="auto")
    centers = (bins[:-1] + bins[1:]) / 2
    width = (bins[1] - bins[0]) * 0.4

    fig, ax = plt.subplots(figsize=(6, 3.5))
    for offset, (code, label, color) in zip([-width / 2, width / 2], SEXES):
        sex_values = sample.loc[sample["sex"] == code, "aces_proxy"].dropna()
        counts, _ = np.histogram(sex_values, bins=bins)
        ax.bar(centers + offset, 100 * counts / len(sex_values), width=width, color=color,
               label=f"{label} (n = {len(sex_values)})")
    if whole_numbers:
        ax.set_xticks(centers, [f"{c:g}" for c in centers])
    ax.set_xlabel("aces_proxy")
    ax.set_ylabel("% of males / % of females")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    save_figure(fig, save_path_no_ext)


def plot_subtype_means(sample, ttests, save_path_no_ext):
    # Mean +/- SE of each subtype by sex (for a 0/1 subtype, the mean is the proportion with it)
    significant = ttests.set_index("subtype")["significant"]
    fig, axes = plt.subplots(2, 5, figsize=(15, 6))
    for ax, subtype in zip(axes.flat, SUBTYPES):
        data = [sample.loc[sample["sex"] == code, subtype].dropna() for code, _, _ in SEXES]
        means = [d.mean() for d in data]
        ses = [d.sem() for d in data]  # SD / sqrt(n)
        ax.bar([1, 2], means, yerr=ses, width=0.6, capsize=6, color=[color for _, _, color in SEXES], ecolor="black")
        ax.set_xticks([1, 2], [label for _, label, _ in SEXES])
        ax.set_xlim(0.4, 2.6)
        ax.set_title(textwrap.fill(SUBTYPE_NAMES[subtype], 22))  # long names on two lines
        ax.spines[["top", "right"]].set_visible(False)

        if significant[subtype]:
            # bracket between the two bars with a * above it
            high = max(m + se for m, se in zip(means, ses))
            step = high * 0.08 if high > 0 else 0.05
            ax.plot([1, 1, 2, 2], [high + step, high + 1.5 * step, high + 1.5 * step, high + step], color="black", linewidth=1)
            ax.text(1.5, high + 1.6 * step, "*", ha="center", va="bottom", fontsize=16)
            ax.set_ylim(top=high + 3 * step)
    for ax in axes[:, 0]:
        ax.set_ylabel("Mean ± SE")
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
    plot_subtype_means(sample, ttests, os.path.join(out_dir, "ace_subtypes_mean_se_by_sex"))
    print(f"\nSaved to {out_dir}")
