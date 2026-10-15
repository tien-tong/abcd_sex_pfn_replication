#!/usr/bin/env bash
# Create the ace environment: every Python library the scripts import, Connectome Workbench
# (wb_command) and R 4.4 with every R package the scripts load. Linux only: conda-forge's
# connectome-workbench package is built for Linux.
# Run with: bash setup_env.sh

set -e

ENV_PATH="${ENV_PATH:-${HOME}/miniforge3/envs/ace}"

echo "Creating environment at ${ENV_PATH} ..."
mamba create -p "${ENV_PATH}" -c conda-forge --strict-channel-priority -y \
  python=3.11 \
  numpy pandas scipy scikit-learn matplotlib h5py nibabel nilearn pyreadr jupyter \
  connectome-workbench \
  r-base=4.4 \
  r-essentials \
  r-remotes \
  pandoc \
  r-mgcv r-lme4 r-r.matlab r-rcppcnpy \
  r-ggplot2 r-ggpattern r-dplyr r-magrittr r-tibble r-data.table r-scales r-stringr \
  r-ciftitools r-gifti r-hexbin r-matrixstats r-plotrix r-proc r-plotroc r-freesurferformats r-sjmisc \
  r-cli r-lifecycle r-abind r-oro.nifti r-rnifti r-r.utils

# Packages that are not on conda-forge
# neuromaps: spin tests and PNC fsaverage -> fsLR (PyPI only)
"${ENV_PATH}/bin/pip" install neuromaps
# enigmatoolbox: only imported by spin_tests/convert_to_gifti.py; --no-deps skips its pandas<=1.3 pin
"${ENV_PATH}/bin/pip" install --no-deps git+https://github.com/MICA-MNI/ENIGMA.git
# freesurfer (used by genetics/read_gene_annot_files.R) and its dependency neurobase are CRAN-only and pure R;
# everything they import is installed from conda-forge above
"${ENV_PATH}/bin/Rscript" -e 'install.packages(c("neurobase", "freesurfer"), repos = "https://cloud.r-project.org", dependencies = FALSE)'

echo "Done. Activate with: mamba activate ace   (the SLURM job scripts activate it themselves)"
echo "CONFIG.txt expects wb_command at ${ENV_PATH}/bin/wb_command (CONDA_BASE / CONDA_ENV)"
