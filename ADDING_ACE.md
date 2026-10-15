# Data inputs and run guide: Parts 3–10

Every file path lives in [CONFIG.txt](CONFIG.txt). The scripts read it themselves, so no paths are edited inside them.

## Layout

The project folder holds the git repo (`code/`) and three data folders next to it. Only `code/` is in git; the data folders are outside the repo. The analysis runs from `/mnt/isilon/pennlinc/tien/abcd_sex_pfn`. Setup stages the data on CUBIC home (`/cbica/home/tongt/abcd_sex_pfn`) and moves it there through Box.

```
/mnt/isilon/pennlinc/tien/abcd_sex_pfn/   the project (PROJECT_DIR)
├── code/                          # the git repo (CODE_DIR)
│   ├── CONFIG.txt                     # every file path
│   ├── pfn_config.py / pfn_config.R   # read CONFIG.txt for Python / R scripts
│   ├── ace_data.py                    # binarizedACE for the Part 4 SVM scripts
│   ├── download_reference_files.sh    # medial-wall masks, fsaverage5 resampling files, AHBA files
│   ├── setup_env.sh                   # creates the ace conda environment
│   ├── README.md                      # fork summary + link to Ashley's site
│   ├── ADDING_ACE.md                  # this guide
│   ├── index.md, _config.yml, _layouts/, Gemfile   # Ashley's GitHub Pages site
│   ├── discovery and replication sample setup scripts/   # Part 1, plus 3.1 convert_mat.py and 8.1 network matrices
│   ├── atlas_visualization/           # Part 2
│   ├── univariate_analysis/           # Part 3 and Part 9
│   │   ├── GAMs scripts/              #   oSex * binarizedACE GAMs (R) + SLURM wrappers
│   │   ├── workbench setup scripts/   #   abs-sum maps → CIFTI
│   │   ├── barplot scripts/
│   │   ├── individual network scripts/
│   │   └── pubertal_analyses/         #   Part 9: puberty_scripts/, puberty_submit_scripts/, abs_sum_maps/, barplots/, individual_network_maps/
│   ├── multivariate_analysis/         # Part 4 and Part 8
│   │   ├── nonzero matrix creation scripts/
│   │   ├── SVM scripts/               #   python scripts/, shell (job) wrappers/, submit job scripts/
│   │   ├── SVM workbench visualization/, haufe transformation scripts/
│   │   ├── SVM weights barplot/, SVM brain map plot/
│   │   ├── SVM accuracy histogram/, roc_curve/
│   │   └── network_specific_analyses/
│   ├── genetics/                      # Part 5: fslr_to_fsaverage5.sh + enrichment folders
│   ├── spin_tests/                    # Part 6
│   ├── hex_plots/, figure_s8_barplots/   # Part 7
│   └── demographics_table/            # Part 10 notebook + ace_by_sex.py (ACE by sex, grant report)
├── inputs/                        # not in git: copied from CUBIC (INPUT_DIR)
├── reference_files/               # not in git: downloaded reference files (REFERENCE_DIR)
└── results/                       # not in git: everything the pipeline writes (RESULTS_DIR)
```

## Setup

Setup happens in two places. **A** runs on CUBIC home, where Ashley's files are: it builds `inputs/`, `results/` (Ashley's converted matrices) and `reference_files/` in `/cbica/home/tongt/abcd_sex_pfn`. Those three folders then go to Box. **B** runs directly in `/mnt/isilon/pennlinc/tien/abcd_sex_pfn`, where the analysis runs: it clones the repo again and downloads the three folders from Box.

**A. On CUBIC home**

```bash
# 1. Code -> code/
mkdir -p /cbica/home/tongt/abcd_sex_pfn
git clone git@github.com:tien-tong/abcd_sex_pfn_replication.git /cbica/home/tongt/abcd_sex_pfn/code
cd /cbica/home/tongt/abcd_sex_pfn/code
git checkout refactor
# this clone works in the CUBIC home project folder
sed -i 's|^PROJECT_DIR=.*|PROJECT_DIR="/cbica/home/tongt/abcd_sex_pfn"|' CONFIG.txt
source CONFIG.txt
ASH=/cbica/projects/ash_pfn_sex_diff_abcd

# 2. Inputs from CUBIC -> inputs/
mkdir -p "$INPUT_DIR" "$PNC_SPINTEST_DIR"
cp -r "$ASH/dropbox/subject_data" "$INPUT_DIR/"
cp "$ASH/dropbox/discovery_sample_siblings_removed_071524.csv" "$ASH/dropbox/replication_sample_siblings_removed_071524.csv" "$INPUT_DIR/"
cp "$ASH/dropbox/unthresholded_abs_sum_replication_071624.dscalar.nii" "$INPUT_DIR/"
cp "$ASH/software/containers/sex_differences_replication_0.0.3.sif" "$INPUT_DIR/"
cp -r "$ASH/dropbox/genetics_files" "$ASH/dropbox/hormone_pds_data" "$INPUT_DIR/"
cp /cbica/projects/abcdfnets/scripts/FilesForAdam/DEAP-siteID.rds "$INPUT_DIR/"
cp "$ASH/dropbox/spintest/GamSexAbssum_lh.csv" "$ASH/dropbox/spintest/GamSexAbssum_rh.csv" "$PNC_SPINTEST_DIR/"

# 3. Ashley's converted matrices -> results/ (Part 3 step 1's output; it doesn't depend on ACE, so step 1 is skipped)
mkdir -p "$RESULTS_DIR"
cp -r "$ASH/results/converted_matrices" "$RESULTS_DIR/"

# 4. Reference files from GitHub and figshare (~4 GB download) -> reference_files/
bash download_reference_files.sh
```

Then upload `inputs/`, `results/` and `reference_files/` from `/cbica/home/tongt/abcd_sex_pfn` to Box.

**B. In /mnt/isilon/pennlinc/tien/abcd_sex_pfn**

```bash
# 1. Code -> code/ (CONFIG.txt already points at /mnt/isilon/pennlinc/tien/abcd_sex_pfn)
mkdir -p /mnt/isilon/pennlinc/tien/abcd_sex_pfn
git clone git@github.com:tien-tong/abcd_sex_pfn_replication.git /mnt/isilon/pennlinc/tien/abcd_sex_pfn/code
cd /mnt/isilon/pennlinc/tien/abcd_sex_pfn/code
git checkout refactor
source CONFIG.txt

# 2. Data from Box: download inputs/, results/ and reference_files/ (Box CLI must be set up first; see the note below)
DEST="/mnt/isilon/pennlinc/tien/abcd_sex_pfn/"
FILE_ID=2527284393565 # reference_files
box files:download $FILE_ID --destination $DEST
FILE_ID=2527456014183 # inputs
box files:download $FILE_ID --destination $DEST
FILE_ID=2527624900574 # results
box files:download $FILE_ID --destination $DEST

# 3. Output folders -> results/ (also restores any empty folders Box drops)
for v in $(grep -oE '^[A-Z0-9_]+_DIR=' CONFIG.txt | tr -d =); do
  case "${!v}" in "$RESULTS_DIR"*) mkdir -p "${!v}" ;; esac
done
mkdir -p "$(dirname "$DEMOGRAPHICS_TABLE_CSV")"
for set in discovery replication; do
  mkdir -p "$PUBERTY_DATA_DIR/$set" "$PUBERTY_ABS_SUM_DIR"/{matrices,cifti_files}/$set \
           "$PUBERTY_BARPLOTS_DIR"/{matrices,barplots}/$set "$PUBERTY_INDIVIDUAL_NETWORK_DIR/$set"
  for test in pds_male_female_{,oSex_}{age,no_age} hormone_{ert,dhea}_mf_{,oSex_}{age,no_age} \
              pds_{female,male}_only_{age,no_age} hormone_{hse,ert,dhea}_female_only_{age,no_age} hormone_{ert,dhea}_male_only_{age,no_age}; do
    mkdir -p "$PUBERTY_RESULTS_DIR/$set/$test"
  done
done
```

Box CLI has to be installed and authenticated through a Box app before step 2. The IDs are Box file IDs, from the file's Box address (`app.box.com/file/<ID>`), so they go with `box files:download`; a folder ID (`app.box.com/folder/<ID>`) needs `box folders:download` instead, and `files:download` returns 404 for it. If the downloads are archives (zip/tar), unpack them in `DEST` so `inputs/`, `results/` and `reference_files/` end up next to `code/`.

Then:

1. Put the ACE csv in `inputs/` and set `ACE_CSV` in CONFIG.txt to it. It needs the columns `src_subject_id` (`sub-<id>`), `eventname` and `binarizedACE` (0/1). The GAM and SVM scripts keep its `baseline_year_1_arm_1` rows and match them to the samples' `subjectkey` (`INV<id>`) with the prefixes stripped; subjects without a baseline ACE value are left out of the models.
2. If `reference_files/` from Box doesn't have the two AHBA files yet (it was uploaded before `download_reference_files.sh` fetched them), run `bash download_reference_files.sh` once more.

The commands below are written to run from the repo root (`code/`), after `source CONFIG.txt`, but the scripts themselves don't depend on the current folder: the SLURM job scripts find `CONFIG.txt` from their own location (so `sbatch` works from any folder, including the jobs that `submit_scripts.py` submits), and the Python and R scripts find it the same way; in RStudio, `setwd()` into the repo first.

## Software (Linux / Red Hat)

One conda environment, `ace`, holds everything the scripts need: the Python libraries, Connectome Workbench (`wb_command`) and R 4.4 with all the R packages. `setup_env.sh` (in the repo) creates it from conda-forge; the two packages that aren't on conda-forge come from PyPI/GitHub (`neuromaps`, `enigmatoolbox`) and CRAN (`freesurfer`, `neurobase`).

```bash
# 1. Miniforge (skip if already installed), then close and reopen the terminal
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"
bash "Miniforge3-$(uname)-$(uname -m).sh" -b -p "$HOME/miniforge3"
"$HOME/miniforge3/bin/conda" init bash

# 2. The ace environment (about 1 GB), from the repo root cloned in Setup
cd /mnt/isilon/pennlinc/tien/abcd_sex_pfn/code
bash setup_env.sh
```

- Every SLURM/SGE job script activates `ace` itself, using `CONDA_BASE` and `CONDA_ENV` in CONFIG.txt (defaults: `~/miniforge3` and `ace`). For anything run by hand, `mamba activate ace` first.
- `WB_COMMAND` in CONFIG.txt already points at the environment's `wb_command`.
- The GAM and puberty jobs still run R inside Ashley's container; the other R scripts use the environment's R.
- `neuromaps` downloads its fsLR atlas files to `~/neuromaps-data` the first time `spin_test.py` runs. If compute nodes have no internet, run the first spin test on a login node.

## Inputs

**Copied from CUBIC by the setup script:**

| Data | Source on CUBIC | CONFIG key (copied into `inputs/`) |
|---|---|---|
| Subject PFNs | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/subject_data/sub-NDAR<id>/IndividualParcel_Final_sbj1_comp17_alphaS21_1_alphaL300_vxInfo1_ard0_eta0/final_UV.mat` | `SUBJECT_DATA_DIR` |
| Discovery sample | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/discovery_sample_siblings_removed_071524.csv` | `DISCOVERY_SAMPLE_CSV` |
| Replication sample | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/replication_sample_siblings_removed_071524.csv` | `REPLICATION_SAMPLE_CSV` |
| Container | `/cbica/projects/ash_pfn_sex_diff_abcd/software/containers/sex_differences_replication_0.0.3.sif` | `CONTAINER_SIF` |
| CIFTI template (header only) | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/unthresholded_abs_sum_replication_071624.dscalar.nii` | `CIFTI_TEMPLATE_DSCALAR` |
| Gene and cell-type tables | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/genetics_files/` | `GENETICS_FILES_DIR` |
| Hormone and PDS data | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/hormone_pds_data/` | `HORMONE_PDS_DIR` |
| Site IDs | `/cbica/projects/abcdfnets/scripts/FilesForAdam/DEAP-siteID.rds` | `DEAP_SITE_RDS` |
| PNC maps | `/cbica/projects/ash_pfn_sex_diff_abcd/dropbox/spintest/GamSexAbssum_{lh,rh}.csv` | `PNC_SPINTEST_DIR` |
| ACE data (`src_subject_id`, `eventname`, `binarizedACE`) | the ACE csv, copied in by hand | `ACE_CSV` |

**Reference files in `reference_files/`:**

- Medial-wall masks and the 8 fsLR→fsaverage5 resampling files from [S-A_ArchetypalAxis](https://github.com/PennLINC/S-A_ArchetypalAxis): downloaded by `download_reference_files.sh` (setup step A4).
- AHBA `lh.Schaefer1000_7net.annot` and `ROIxGene_Schaefer1000_INT.mat` (Part 5 only), from the figshare dataset the website names ([6852911](https://figshare.com/articles/dataset/AHBAdata/6852911)): downloaded by `download_reference_files.sh`, which takes `data/genes/parcellations/lh.Schaefer1000_7net.annot` out of `AHBAdata.zip` and `ROIxGene_Schaefer1000_INT.mat` out of `AHBAprocessed.zip` and then deletes the zips.

## Run order

Each comment names what the step produces.

### Part 3: Univariate GAMs

The GAM and lmer use `oSex * binarizedACE`. Each network gets three sets of results in `GAMS_<SET>_DIR`:

- `SexEffect_*`: the sex difference in the no-ACE group (`binarizedACE` = 0)
- `ACEEffect_*`: the ACE vs no-ACE difference, averaged over sexes
- `SexByACEEffect_*`: how the sex difference changes between the ACE and no-ACE groups

The abs-sum, barplot and individual-network steps below still read `SexEffect_*` only.

```bash
U="$CODE_DIR/univariate_analysis"
# python3 "$CODE_DIR/discovery and replication sample setup scripts/convert_mat.py"          # skipped: setup copies Ashley's converted_matrices/
sbatch --mem=25G --time=1-00:00:00 "$U/GAMs scripts/shell (job) wrappers/run_univariate_analysis.sh"     # GAMS_DISCOVERY_DIR
sbatch --mem=25G --time=1-00:00:00 "$U/GAMs scripts/shell (job) wrappers/run_univariate_replication.sh"  # GAMS_REPLICATION_DIR
python3 "$U/workbench setup scripts/write_effect_map_abs_sum.py"                              # GAMS_ABS_SUM_*_CSV
python3 "$U/workbench setup scripts/write_effect_map_to_cifti.py" "$GAMS_ABS_SUM_DISCOVERY_CSV" "$GAMS_ABS_SUM_DISCOVERY_DSCALAR"      # Fig 2
python3 "$U/workbench setup scripts/write_effect_map_to_cifti.py" "$GAMS_ABS_SUM_REPLICATION_CSV" "$GAMS_ABS_SUM_REPLICATION_DSCALAR"
python3 "$U/barplot scripts/make_barplot_mat.py"                                              # GAMS_BARPLOT_MAT_*_CSV
Rscript "$U/barplot scripts/create_barplot.R" discovery                                      # Fig 2A
Rscript "$U/barplot scripts/create_barplot.R" replication                                    # Fig 2B
python3 "$U/individual network scripts/get_individual_network_mat.py"                         # Fig 2C / S1
python3 "$U/individual network scripts/individual_networks_to_cifti.py"
```

### Part 4: SVM

The SVM predicts `binarizedACE` (0 = no, 1 = yes) from the PFN loadings, with motion, age, sex (M = -1, F = 1) and site regressed out of the loadings in each training set. Subjects without a baseline ACE value are left out (`ace_data.py`). The ACE groups differ in size, so the SVM weights both groups equally (`class_weight='balanced'`), the splits keep the same ACE proportion in each half, C is chosen by balanced accuracy, and the results include balanced accuracy and AUC. Positive weights and decision values point toward ACE = 1.

```bash
M="$CODE_DIR/multivariate_analysis"
python3 "$M/nonzero matrix creation scripts/create_nonzero_matrix.py" discovery
python3 "$M/nonzero matrix creation scripts/create_nonzero_matrix.py" replication
sbatch "$M/SVM scripts/shell (job) wrappers/svm_resmulti_times_parallel_w_ROC_slurm.sh"       # SVM_RESULTS_DIR/time_1..100
python3 "$M/SVM workbench visualization/svm_workbench_visualization_multi_times_matrix.py"     # SVM_WEIGHTS_*_NPY
sbatch "$M/haufe transformation scripts/haufe_transform_weights_slurm.sh"                     # HAUFE_WEIGHTS_*_NPY
Rscript "$M/SVM weights barplot/svm_stacked_barplot.R" discovery                              # Fig 3C
Rscript "$M/SVM weights barplot/svm_stacked_barplot.R" replication
python3 "$M/SVM brain map plot/sum_abs_weights_matrix_svm.py"                                 # SVM_ABS_SUM_*_NPY
python3 "$M/SVM brain map plot/write_effect_map_to_cifti_svm.py" "$SVM_ABS_SUM_DISCOVERY_NPY" "$SVM_ABS_SUM_DISCOVERY_DSCALAR"      # Fig 3B
python3 "$M/SVM brain map plot/write_effect_map_to_cifti_svm.py" "$SVM_ABS_SUM_REPLICATION_NPY" "$SVM_ABS_SUM_REPLICATION_DSCALAR"
sbatch "$M/SVM scripts/shell (job) wrappers/svm_permutation_parallel.sh"                      # SVM_PERMUTATION_DIR/time_1..1000
python3 "$M/SVM accuracy histogram/get_accuracies.py"
python3 "$M/SVM accuracy histogram/get_svm_metrics.py"                                        # accuracy / sensitivity / specificity / balanced accuracy / AUC (SVM_METRICS_CSV)
Rscript "$M/SVM accuracy histogram/svm_accuracy_histogram.R"                                  # Fig 3A inset; balanced accuracy, red line = SVM_METRICS_CSV
python3 "$M/roc_curve/create_ROC_curve.py"
Rscript "$M/roc_curve/plot_roc.R"                                                             # Fig 3A
```

### Part 5: Genetics

The enrichment scripts take a map name: `gams_uncorrected_discovery` (the default), `gams_uncorrected_replication`, `gams_fdr_discovery` or `gams_fdr_replication`.

```bash
G="$CODE_DIR/genetics"
python3 "$CODE_DIR/univariate_analysis/workbench setup scripts/write_effect_map_abs_sum_fdr.py"
python3 "$CODE_DIR/univariate_analysis/workbench setup scripts/write_effect_map_to_cifti.py" "$GAMS_FDR_ABS_SUM_DISCOVERY_CSV" "$GAMS_FDR_ABS_SUM_DISCOVERY_DSCALAR"
python3 "$CODE_DIR/univariate_analysis/workbench setup scripts/write_effect_map_to_cifti.py" "$GAMS_FDR_ABS_SUM_REPLICATION_CSV" "$GAMS_FDR_ABS_SUM_REPLICATION_DSCALAR"
bash "$G/fslr_to_fsaverage5.sh" "$GAMS_ABS_SUM_DISCOVERY_DSCALAR" gams_uncorrected_discovery
bash "$G/fslr_to_fsaverage5.sh" "$GAMS_ABS_SUM_REPLICATION_DSCALAR" gams_uncorrected_replication
bash "$G/fslr_to_fsaverage5.sh" "$GAMS_FDR_ABS_SUM_DISCOVERY_DSCALAR" gams_fdr_discovery
bash "$G/fslr_to_fsaverage5.sh" "$GAMS_FDR_ABS_SUM_REPLICATION_DSCALAR" gams_fdr_replication
Rscript "$G/read_gene_annot_files.R"
python3 "$G/create_probe_annotation.py"
Rscript "$G/chromosome_enrichment/ABCD_wSex_cor_gene_schaefer403_net7_discovery_20242108.R" gams_uncorrected_discovery    # Fig 4A
Rscript "$G/chromosome_enrichment/ABCD_wSex_cor_gene_schaefer403_net7_discovery_20242108.R" gams_uncorrected_replication
Rscript "$G/chromosome_enrichment/correct_pvals.R"
Rscript "$G/celltype_enrichment/cell_types_LAKE.R" gams_uncorrected_discovery                # Fig 4B
Rscript "$G/PSP_enrichment/PSP_plots.R" gams_uncorrected_discovery
```

### Part 6: Spin tests

The website uses `Gam_abs_sum_fslr_test.gii` for the PNC comparison, but no script makes that file. The last command below uses the file the scripts actually produce.

```bash
S="$CODE_DIR/spin_tests"
for map in gams_discovery gams_replication svm_discovery svm_replication; do
  Rscript "$S/add_medial_wall.R" $map
  f="${map/gams/gam}"   # add_medial_wall.R names its output e.g. gam_abs_sum_discovery_medial_wall.csv
  python3 "$S/convert_to_gifti.py" "$MEDIAL_WALL_MAPS_DIR/${f/_/_abs_sum_}_medial_wall.csv" "$SPIN_GIFTI_DIR/${map}.gii" N
done
python3 "$S/spin_test.py" "$SPIN_GIFTI_DIR/gams_discovery.gii" "$SPIN_GIFTI_DIR/gams_replication.gii" fsLR "Gams discovery vs replication" "$SPIN_RESULTS_DIR"
python3 "$S/spin_test.py" "$SPIN_GIFTI_DIR/svm_discovery.gii" "$SPIN_GIFTI_DIR/svm_replication.gii" fsLR "SVM discovery vs replication" "$SPIN_RESULTS_DIR"
python3 "$S/spin_test.py" "$SPIN_GIFTI_DIR/gams_discovery.gii" "$SPIN_GIFTI_DIR/svm_discovery.gii" fsLR "Gams discovery vs SVM discovery" "$SPIN_RESULTS_DIR"
python3 "$S/spin_test.py" "$SPIN_GIFTI_DIR/gams_replication.gii" "$SPIN_GIFTI_DIR/svm_replication.gii" fsLR "Gams replication vs SVM replication" "$SPIN_RESULTS_DIR"
python3 "$S/compile_spin_tests.py" "$SPIN_RESULTS_DIR"
# PNC vs ABCD
python3 "$S/convert_to_gifti.py" "$PNC_GAMS_ABS_SUM_LH_CSV" "$PNC_GAMS_ABS_SUM_LH_GII" Y
python3 "$S/convert_to_gifti.py" "$PNC_GAMS_ABS_SUM_RH_CSV" "$PNC_GAMS_ABS_SUM_RH_GII" Y
python3 "$S/PNC_to_fslr.py"
python3 "$S/spin_test.py" "$PNC_GAMS_ABS_SUM_FSLR_GII" "$SPIN_GIFTI_DIR/gams_discovery.gii" fsLR "PNC gams discovery vs ABCD gams discovery fslr" "$SPIN_RESULTS_DIR"
```

### Part 7: Other figures

For Fig S8, set `grouped_table_name` in `figure_s8_barplot.R`, and comment out the GAMs or SVM code blocks as before.

```bash
H="$CODE_DIR/hex_plots/hex_plots.R"                                                           # Fig 2E, 2F, 3D
Rscript "$H" "$GAMS_ABS_SUM_DISCOVERY_CSV" "Discovery GAM Loadings" "$GAMS_ABS_SUM_REPLICATION_CSV" "Replication GAM Loadings" "$HEX_PLOTS_DIR/gams_disc_vs_rep.png"
Rscript "$H" "$SVM_ABS_SUM_DISCOVERY_NPY" "Discovery SVM Weights" "$SVM_ABS_SUM_REPLICATION_NPY" "Replication SVM Weights" "$HEX_PLOTS_DIR/svm_disc_vs_rep.png"
Rscript "$H" "$SVM_ABS_SUM_DISCOVERY_NPY" "Discovery SVM Weights" "$GAMS_ABS_SUM_DISCOVERY_CSV" "Discovery GAM Loadings" "$HEX_PLOTS_DIR/svm_vs_gams_disc.png"
Rscript "$H" "$SVM_ABS_SUM_REPLICATION_NPY" "Replication SVM Weights" "$GAMS_ABS_SUM_REPLICATION_CSV" "Replication GAM Loadings" "$HEX_PLOTS_DIR/svm_vs_gams_rep.png"
# Fig S8 (network-sums tables come from create_barplot.R / svm_stacked_barplot.R)
python3 "$CODE_DIR/figure_s8_barplots/group_networks.py" "$FIGURE_S8_DIR/svm_replication_network_sums_table_check.csv" "$FIGURE_S8_DIR/svm_replication_grouped_table_check.csv" svm
Rscript "$CODE_DIR/figure_s8_barplots/figure_s8_barplot.R"
```

### Part 8: Network-specific models

```bash
python3 "$CODE_DIR/discovery and replication sample setup scripts/create_network_specific_matrices.py"
python3 "$CODE_DIR/multivariate_analysis/SVM scripts/submit job scripts/submit_network_specific_models_jobs.py"   # 17 arrays x 100
python3 "$CODE_DIR/multivariate_analysis/network_specific_analyses/get_network_specific_accuracies.py"
Rscript "$CODE_DIR/multivariate_analysis/network_specific_analyses/plot_accuracies.R"
```

### Part 9: Puberty

Wait for every model job from `submit_scripts.py` and `submit_scripts_oSex.py` to finish before running the post-processing below them. Those scripts loop over every model folder, so an empty or incomplete folder stops them.

```bash
P="$CODE_DIR/univariate_analysis/pubertal_analyses"
python3 "$P/puberty_scripts/make_behavior_dfs.py"                  # PUBERTY_DATA_DIR
python3 "$P/submit_scripts.py"                                     # 40 jobs -> PUBERTY_RESULTS_DIR
python3 "$P/submit_scripts_oSex.py"                                # 12 jobs
python3 "$P/abs_sum_maps/write_effect_map_abs_sum.py"
python3 "$P/abs_sum_maps/cifti_wrapper.py"
python3 "$P/barplots/make_barplot_mats.py"
python3 "$P/barplots/create_barplot_wrapper.py"
python3 "$P/individual_network_maps/make_individual_mats.py"
python3 "$P/individual_network_maps/to_cifti_wrapper.py"
python3 "$P/individual_network_maps/identify_sig_networks.py"
```

### Part 10: Demographics

Open `demographics_table/demographics.ipynb` from inside `demographics_table/` and run the cells in order. It writes `DEMOGRAPHICS_TABLE_CSV`.

ACE by sex in the full sample (discovery + replication, baseline ACE), for the grant report:

```bash
python3 "$CODE_DIR/demographics_table/ace_by_sex.py"   # ACE_BY_SEX_DIR: aces_proxy histogram, ACE subtype violins, subtype ~ sex t-tests
```

The t-tests are Welch's (the default of R's `t.test`), female vs male, with no correction for multiple comparisons; subtypes with p < .05 get a * in the violin plot. The table is printed and saved as `ace_subtypes_ttest_by_sex.csv`.
