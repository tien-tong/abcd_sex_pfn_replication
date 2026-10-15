library(stats)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

uncorrected_discovery_pvals <- read.csv(file.path(cfg$CHROMOSOME_ENRICHMENT_DIR, "uncorrected_discovery_pvals.csv"))
corrected_pvals <- p.adjust(uncorrected_discovery_pvals$pval, method="bonferroni")

corrected_pval_df <- as.data.frame(uncorrected_discovery_pvals$chromosome)
corrected_pval_df$uncorrected_pval <- uncorrected_discovery_pvals$pval
corrected_pval_df$corrected_pval <- corrected_pvals

write.csv(corrected_pval_df, file.path(cfg$CHROMOSOME_ENRICHMENT_DIR, "figure_4a_fdr_corrected_pvals_2.csv"))


uncorrected_rep_pvals <- read.csv(file.path(cfg$CHROMOSOME_ENRICHMENT_DIR, "uncorrected_replication_pvals.csv"))
corrected_rep_pvals <- p.adjust(uncorrected_rep_pvals$pval, method="bonferroni")

corrected_rep_pval_df <- as.data.frame(uncorrected_rep_pvals$chromosome)
corrected_rep_pval_df$uncorrected_pval <- uncorrected_rep_pvals$pval
corrected_rep_pval_df$corrected_pval <- corrected_rep_pvals

write.csv(corrected_rep_pval_df, file.path(cfg$CHROMOSOME_ENRICHMENT_DIR, "replication_corrected_pvals_bonf.csv"))
