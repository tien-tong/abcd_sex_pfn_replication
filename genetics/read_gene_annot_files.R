library(freesurferformats)
library(freesurfer)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

annot_file <- read.fs.annot(cfg$AHBA_SCHAEFER1000_ANNOT)

lh_Schaefer1000_7net_cttable <- annot_file$colortable$table[,5]
write.table(lh_Schaefer1000_7net_cttable, cfg$SCHAEFER1000_CTTABLE_CSV, row.names = FALSE, col.names = FALSE)

annot_file_2 <- read_annotation(cfg$AHBA_SCHAEFER1000_ANNOT)
L <- annot_file_2$label
write.table(L, cfg$SCHAEFER1000_LABELS_CSV,  row.names = FALSE, col.names = FALSE)
