library(ggplot2)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))
theme_set(theme_classic(base_size = 16))
discovery_accuracies <- read.csv(cfg$PERMUTATION_ACCURACY_DISCOVERY_CSV)
replication_accuracies <- read.csv(cfg$PERMUTATION_ACCURACY_REPLICATION_CSV)
# True (non-permuted) average balanced accuracies from get_svm_metrics.py, drawn as the red dashed lines.
# Balanced accuracy, not accuracy, because the ACE groups differ in size
svm_metrics <- read.csv(cfg$SVM_METRICS_CSV)
discovery_accuracy <- svm_metrics$Avg.Balanced.Accuracy[svm_metrics$set == "discovery"]
replication_accuracy <- svm_metrics$Avg.Balanced.Accuracy[svm_metrics$set == "replication"]


ggplot(discovery_accuracies, aes(x=Balanced.Accuracy)) + geom_histogram(fill="black")


disc_hist <- ggplot(discovery_accuracies, aes(x=Balanced.Accuracy)) + geom_histogram(fill="black", bins=200, size=0.02, color="black") + geom_vline(aes(xintercept = discovery_accuracy),
                                                                                    color = "red", linetype = "dashed", linewidth=1) + labs(x="Balanced accuracy", y="Count") +
  scale_y_continuous(limits = c(0, 80), breaks=seq(0, 80, 20), expand = c(0, 0)) +  
  scale_x_continuous(breaks=c(0.4, 0.6, 0.8), labels=c("0.4", "0.6", "0.8")) +
  theme(axis.text.y = element_text (size = 7)) +
  theme(axis.title = element_text (size = 10, colour= "black")) +
  theme(axis.text.x = element_text (size = 7)) + theme(axis.line=element_line(linewidth=1))

disc_hist


ggsave(file.path(cfg$SVM_OUTPUT_DIR, "discovery_permuation_histogram.png"), 
       disc_hist, width=2, height=2, dpi=500)


rep_hist <- ggplot(replication_accuracies, aes(x=Balanced.Accuracy)) + geom_histogram(color="black", bins=200, size=0.02, fill="black") + geom_vline(aes(xintercept = replication_accuracy),
                                                                                    color = "red", linetype = "dashed", linewidth=1) + labs(x="Balanced accuracy", y="Count") +
  scale_y_continuous(name="Count", limits = c(0, 80), breaks=seq(0, 80, 20), expand = c(0, 0)) +  
  scale_x_continuous(breaks=c(0.4, 0.6, 0.8), labels=c("0.4", "0.6", "0.8")) +
  theme(axis.text.y = element_text (size = 7)) +
  theme(axis.title = element_text (size = 10, colour= "black")) +
  theme(axis.text.x = element_text (size = 7)) + theme(axis.line=element_line(linewidth=1))

ggsave(file.path(cfg$SVM_OUTPUT_DIR, "replication_permuation_histogram.png"), 
       rep_hist, width=2, height=2, dpi=500)
