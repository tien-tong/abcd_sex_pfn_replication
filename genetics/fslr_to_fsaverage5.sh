#!/bin/bash

# File paths come from CONFIG.txt at the repo root
source "$(dirname "$0")/../CONFIG.txt"

file_to_sep=$1
save_filename=$2
out="${GAMS_GII_DIR}/${save_filename}"
resample="${FSAVERAGE5_RESAMPLE_DIR}"


"$WB_COMMAND" -cifti-separate "${file_to_sep}" COLUMN -metric CORTEX_LEFT "${out}_LH.fslr32k.func.gii"
"$WB_COMMAND" -cifti-separate "${file_to_sep}" COLUMN -metric CORTEX_RIGHT "${out}_RH.fslr32k.func.gii"

#Resample S-A axis from fslr mesh to fsaverage5 mesh

"$WB_COMMAND" -metric-resample "${out}_LH.fslr32k.func.gii" "${resample}/fs_LR-deformed_to-fsaverage.L.sphere.32k_fs_LR.surf.gii" "${resample}/fsaverage5_std_sphere.L.10k_fsavg_L.surf.gii" ADAP_BARY_AREA "${out}_LH.fsaverage5.func.gii" -area-metrics "${resample}/fs_LR.L.midthickness_va_avg.32k_fs_LR.shape.gii" "${resample}/fsaverage5.L.midthickness_va_avg.10k_fsavg_L.shape.gii"

"$WB_COMMAND" -metric-resample "${out}_RH.fslr32k.func.gii" "${resample}/fs_LR-deformed_to-fsaverage.R.sphere.32k_fs_LR.surf.gii" "${resample}/fsaverage5_std_sphere.R.10k_fsavg_R.surf.gii" ADAP_BARY_AREA "${out}_RH.fsaverage5.func.gii" -area-metrics "${resample}/fs_LR.R.midthickness_va_avg.32k_fs_LR.shape.gii" "${resample}/fsaverage5.R.midthickness_va_avg.10k_fsavg_R.shape.gii"

# Save the command run in commands_run.txt
command="./fslr_to_fsaverage5.sh $file_to_sep $save_filename"
echo $command >> "$COMMANDS_LOG"
