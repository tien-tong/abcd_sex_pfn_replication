library(pROC)
library(plotROC)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))
theme_set(theme_classic(base_size = 16))

#svm_discovery_data <- read.csv("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/svm_replication/roc_curve/discovery_svm_ROC_siblings_removed_data_092624.csv")
#svm_replication_data <- read.csv("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/svm_replication/roc_curve/replication_svm_ROC_siblings_removed_data_092624.csv")
svm_discovery_data <- read.csv(cfg$ROC_DATA_DISCOVERY_CSV)
svm_replication_data <- read.csv(cfg$ROC_DATA_REPLICATION_CSV)


svm_disc_roc <- roc(svm_discovery_data$binarizedACE ~ svm_discovery_data$decision_values)
svm_rep_roc <- roc(svm_replication_data$binarizedACE ~ svm_replication_data$decision_values)


svm_disc_rocplot <- ggplot(svm_discovery_data, aes(m = decision_values, d = binarizedACE)) + 
  geom_roc(n.cuts=0, labels=FALSE, size=2) + xlab("1 - Specificity") + ylab("Sensitivity") +
  scale_y_continuous(limits=c(0, 1), breaks=seq(0, 1, 0.2), labels=c(0, 0.2, 0.4, 0.6, 0.8, 1) , expand=expansion(0)) + scale_x_continuous(limits=c(0, 1), breaks=seq(0, 1, 0.2), labels=c(0, 0.2, 0.4, 0.6, 0.8, 1), expand=expansion(0)) +
  theme(axis.text.x=element_text(size=15), axis.text.y=element_text(size=15), axis.title=element_text(size=20))

ggsave(file.path(cfg$SVM_OUTPUT_DIR, "svm_discovery_roc_plot.png"), 
       svm_disc_rocplot, width=4.8, height=3.5, dpi=300)

svm_rep_rocplot <- ggplot(svm_replication_data, aes(m = decision_values, d = binarizedACE)) + 
  geom_roc(n.cuts=0, labels=FALSE, size=2) + xlab("1 - Specificity") + ylab("Sensitivity") +
  scale_y_continuous(limits=c(0, 1), breaks=seq(0, 1, 0.2), labels=c(0, 0.2, 0.4, 0.6, 0.8, 1) , expand=expansion(0)) + scale_x_continuous(limits=c(0, 1), breaks=seq(0, 1, 0.2), labels=c(0, 0.2, 0.4, 0.6, 0.8, 1), expand=expansion(0)) +
  theme(axis.text.x=element_text(size=15), axis.text.y=element_text(size=15), axis.title=element_text(size=20))

ggsave(file.path(cfg$SVM_OUTPUT_DIR, "svm_replication_roc_plot.png"), 
       svm_rep_rocplot, width =4.8, height=3.5, dpi=300)

