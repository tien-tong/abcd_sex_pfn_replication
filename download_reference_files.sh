#!/bin/bash
# Download the medial-wall masks and the fsLR-32k -> fsaverage5 resampling files from
# github.com/PennLINC/S-A_ArchetypalAxis, and the two AHBA Schaefer-1000 files from
# figshare.com/articles/dataset/AHBAdata/6852911, into the paths CONFIG.txt expects.
# Usage (from the repo root): bash download_reference_files.sh
set -e
source "$(dirname "$0")/CONFIG.txt"
REPO=https://raw.githubusercontent.com/PennLINC/S-A_ArchetypalAxis/main

mkdir -p "$(dirname "$MEDIAL_WALL_MASK_LH")" "$(dirname "$MEDIAL_WALL_MASK_RH")" "$FSAVERAGE5_RESAMPLE_DIR"

# Medial-wall masks (Parts 3-6)
curl -fL "$REPO/FSLRVertex/medialwall.mask.leftcortex.csv" -o "$MEDIAL_WALL_MASK_LH"
curl -fL "$REPO/FSLRVertex/medialwall.mask.rightcortex.csv" -o "$MEDIAL_WALL_MASK_RH"

# Sphere and area files used by genetics/fslr_to_fsaverage5.sh (Part 5)
for f in FSLRVertex/fs_LR-deformed_to-fsaverage.L.sphere.32k_fs_LR.surf.gii \
         FSLRVertex/fs_LR-deformed_to-fsaverage.R.sphere.32k_fs_LR.surf.gii \
         FSLRVertex/fs_LR.L.midthickness_va_avg.32k_fs_LR.shape.gii \
         FSLRVertex/fs_LR.R.midthickness_va_avg.32k_fs_LR.shape.gii \
         FSaverage5/fsaverage5_std_sphere.L.10k_fsavg_L.surf.gii \
         FSaverage5/fsaverage5_std_sphere.R.10k_fsavg_R.surf.gii \
         FSaverage5/fsaverage5.L.midthickness_va_avg.10k_fsavg_L.shape.gii \
         FSaverage5/fsaverage5.R.midthickness_va_avg.10k_fsavg_R.shape.gii; do
    curl -fL "$REPO/$f" -o "$FSAVERAGE5_RESAMPLE_DIR/$(basename "$f")"
done

# AHBA Schaefer-1000 annotation and ROI x gene matrix (Part 5). Each is one file inside a
# ~2 GB zip, so the zips go to a temporary folder that is deleted afterwards.
mkdir -p "$(dirname "$AHBA_SCHAEFER1000_ANNOT")" "$(dirname "$AHBA_ROI_GENE_MAT")"
tmp=$(mktemp -d "$REFERENCE_DIR/ahba_tmp.XXXXXX")
trap 'rm -rf "$tmp"' EXIT
curl -fL https://ndownloader.figshare.com/files/23084357 -o "$tmp/AHBAdata.zip"
unzip -jo "$tmp/AHBAdata.zip" data/genes/parcellations/lh.Schaefer1000_7net.annot -d "$tmp"
mv "$tmp/lh.Schaefer1000_7net.annot" "$AHBA_SCHAEFER1000_ANNOT"
curl -fL https://ndownloader.figshare.com/files/23084366 -o "$tmp/AHBAprocessed.zip"
unzip -jo "$tmp/AHBAprocessed.zip" ROIxGene_Schaefer1000_INT.mat -d "$tmp"
mv "$tmp/ROIxGene_Schaefer1000_INT.mat" "$AHBA_ROI_GENE_MAT"

echo "Downloaded to $(dirname "$MEDIAL_WALL_MASK_LH"), $FSAVERAGE5_RESAMPLE_DIR and $(dirname "$AHBA_ROI_GENE_MAT")"
