library(ciftiTools)
library(gifti)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))


pnc_gams_fslr_abs_sum <- readgii(cfg$PNC_GAMS_ABS_SUM_FSLR_GII)

pnc_gams_data <- pnc_gams_fslr_abs_sum$data$unknown

cifti_lh2 <- as.numeric(pnc_gams_data)[1:32492]
cifti_rh2 <- as.numeric(pnc_gams_data)[32493:64984]

medialwall.mask.leftcortex <- read.csv(cfg$MEDIAL_WALL_MASK_LH, header = F, colClasses = c("logical")) #left cortex medial wall mask
medialwall.mask.rightcortex <-read.csv(cfg$MEDIAL_WALL_MASK_RH, header = F, colClasses = c("logical")) #left cortex medial wall mask

original_map_cifti <- as_cifti(cortexL = cifti_lh2, cortexL_mwall = medialwall.mask.leftcortex$V1, cortexR =  cifti_rh2, cortexR_mwall = medialwall.mask.rightcortex$V1)

pnc_gams_no_medial_wall <- move_to_mwall(original_map_cifti)

pnc_gams_no_medial_wall_all <- data.frame(X0 = c(pnc_gams_no_medial_wall$data$cortex_left, pnc_gams_no_medial_wall$data$cortex_right))


write.csv(pnc_gams_no_medial_wall_all, cfg$PNC_GAMS_ABS_SUM_FSLR_NO_MEDIAL_WALL_CSV)
