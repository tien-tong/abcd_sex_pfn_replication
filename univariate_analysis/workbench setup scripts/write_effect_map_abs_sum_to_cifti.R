library(ciftiTools)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

cifti_data2 <- read.csv(cfg$GAMS_ABS_SUM_REPLICATION_CSV)

cifti_lh2 <- as.numeric(cifti_data2$X0)[0:29696]
cifti_rh2 <- as.numeric(cifti_data2$X0)[29697:59412]

medialwall.mask.leftcortex <- read.csv(cfg$MEDIAL_WALL_MASK_LH, header = F, colClasses = c("logical")) #left cortex medial wall mask
medialwall.mask.rightcortex <-read.csv(cfg$MEDIAL_WALL_MASK_RH, header = F, colClasses = c("logical")) #left cortex medial wall mask

unicorn.dscalar <- as_cifti(cortexL = cifti_lh2, cortexL_mwall = medialwall.mask.leftcortex$V1, cortexR =  cifti_rh2, cortexR_mwall = medialwall.mask.rightcortex$V1)

# NOTE: We ended up not using this file for cifti creation because there is something wrong with the write_cifti function!!!!!
# Write a CIFTI file --------------------------------------------
write_cifti(xifti = unicorn.dscalar, cifti_fname = file.path(cfg$UNIVARIATE_DIR, "gam_sex_abs_sum_all_networks_replication_2.dscalar.nii"))
ciftiTools.setOption('wb_path', cfg$WB_COMMAND)
