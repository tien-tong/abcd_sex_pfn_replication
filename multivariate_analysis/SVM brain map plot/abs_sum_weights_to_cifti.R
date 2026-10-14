library(ciftiTools)
library(RcppCNPy)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

ciftiTools.setOption('wb_path', cfg$WB_COMMAND)

# Which sample: "discovery" or "replication"; pass as the first argument or edit here
args <- commandArgs(trailingOnly = TRUE)
sample_set <- if (length(args) >= 1) args[1] else "replication"

#cifti_data2 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/abs_sum_weight_brain_mat.npy")
#cifit_data2 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/abs_sum_weight_brain_mat_replication.npy")
#cifti_data2 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/svm_correct_results/abs_sum_weight_brain_mat_discovery_haufe_100_runs.npy")
cifti_data2 <- npyLoad(cfg[[paste0("SVM_ABS_SUM_", toupper(sample_set), "_NPY")]])
cifti_lh2 <- as.numeric(cifti_data2)[0:29696]
cifti_rh2 <- as.numeric(cifti_data2)[29697:59412]

medialwall.mask.leftcortex <- read.csv(cfg$MEDIAL_WALL_MASK_LH, header = F, colClasses = c("logical")) #left cortex medial wall mask
medialwall.mask.rightcortex <-read.csv(cfg$MEDIAL_WALL_MASK_RH, header = F, colClasses = c("logical")) #left cortex medial wall mask

unicorn.dscalar <- as_cifti(cortexL = cifti_lh2, cortexL_mwall = medialwall.mask.leftcortex$V1, cortexR =  cifti_rh2, cortexR_mwall = medialwall.mask.rightcortex$V1)


# Write a CIFTI file --------------------------------------------
write_cifti(xifti = unicorn.dscalar, cifti_fname = file.path(cfg$SVM_OUTPUT_DIR, paste0("svm_abs_sum_weights_", sample_set, ".dscalar.nii")))
