library(ciftiTools)
library(RcppCNPy)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

ciftiTools.setOption('wb_path', cfg$WB_COMMAND)

# Which map: gams_discovery, gams_replication, svm_discovery or svm_replication; pass as the first argument or edit here
args <- commandArgs(trailingOnly = TRUE)
map_name <- if (length(args) >= 1) args[1] else "gams_replication"
input_files <- list(gams_discovery = cfg$GAMS_ABS_SUM_DISCOVERY_CSV, gams_replication = cfg$GAMS_ABS_SUM_REPLICATION_CSV,
                    svm_discovery = cfg$SVM_ABS_SUM_DISCOVERY_NPY, svm_replication = cfg$SVM_ABS_SUM_REPLICATION_NPY)

# gam z scores
#cifti_data2 <- read.csv("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/univariate_analysis/univariate_analysis_results/uncorrected_abs_sum_matrix_discovery.csv")
# svm weights
#cifti_data2 <- npyLoad("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/multivariate_analysis/svm_check_run/abs_sum_weight_brain_mat_discovery_haufe_100_runs_112124_check.npy")
#cifti_data2 <- npyLoad("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/multivariate_analysis/svm_check_run/abs_sum_weight_brain_mat_replication_haufe_100_runs_112124_check.npy")

# Include cifti_data2$XO for gams results and then take it off for svm results
# (gam z scores are csv files with the values in column X0; svm weights are npy files)
if (startsWith(map_name, "gams")) {
  cifti_data2 <- as.numeric(read.csv(input_files[[map_name]])$X0)
} else {
  cifti_data2 <- as.numeric(npyLoad(input_files[[map_name]]))
}
cifti_lh2 <- cifti_data2[1:29696]
cifti_rh2 <- cifti_data2[29697:59412]

#cifti_lh2 <- as.numeric(cifti_data2)[1:29696]
#cifti_rh2 <- as.numeric(cifti_data2)[29697:59412]

medialwall.mask.leftcortex <- read.csv(cfg$MEDIAL_WALL_MASK_LH, header = F, colClasses = c("logical")) #left cortex medial wall mask
medialwall.mask.rightcortex <-read.csv(cfg$MEDIAL_WALL_MASK_RH, header = F, colClasses = c("logical")) #left cortex medial wall mask

original_map_cifti <- as_cifti(cortexL = cifti_lh2, cortexL_mwall = medialwall.mask.leftcortex$V1, cortexR =  cifti_rh2, cortexR_mwall = medialwall.mask.rightcortex$V1)

map_medial_wall <- move_from_mwall(original_map_cifti)


# Original output name, e.g. gam_abs_sum_replication_medial_wall.csv or svm_abs_sum_discovery_medial_wall.csv
write.csv(as.matrix(map_medial_wall), file.path(cfg$MEDIAL_WALL_MAPS_DIR, paste0(sub("_", "_abs_sum_", sub("^gams", "gam", map_name)), "_medial_wall.csv")))

#write_cifti(xifti = map_medial_wall, cifti_fname = "/Users/ashfrana/Desktop/code/ABCD GAMs replication/medial_wall_maps/gams_replication_medial_wall_map.dscalar.nii")
