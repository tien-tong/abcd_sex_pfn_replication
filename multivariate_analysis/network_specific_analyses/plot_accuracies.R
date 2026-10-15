library(ggplot2)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

discovery_network_accuracies <- read.csv(cfg$NETWORK_ACCURACY_DISCOVERY_CSV)
replication_network_accuracies <- read.csv(cfg$NETWORK_ACCURACY_REPLICATION_CSV)

netColor <- c("#E76178", "#7499C2", "#F5BA2E", "#7499C2", "#00A131",  "#AF33AD", "#E443FF","#E76178"
              ,"#E443FF", "#AF33AD",  "#7499C2", "#E76178","#7499C2","#00A131", "#F5BA2E",
              "#4E31A8", "#F5BA2E")

discovery_network_accuracies <- cbind(discovery_network_accuracies, netColor)
discovery_ordered <- discovery_network_accuracies[order(discovery_network_accuracies$Accuracy, decreasing=FALSE), ]
discovery_network_accuracies$netColor <- factor(discovery_network_accuracies$netColor)


disc_plot <- ggplot(discovery_network_accuracies, aes(x=reorder(Network, +Accuracy), y=Accuracy, fill=netColor)) + geom_bar(stat='identity') + 
  scale_fill_identity() + theme(legend.position="none") + theme(axis.text.x = element_text(size= 12), axis.text.y = element_text(size= 12), axis.title = element_text(size=18)) +
  xlab("Network") + ylab("Model Performance") + coord_cartesian(ylim = c(0.55, 0.75)) + scale_y_continuous(breaks=seq(0.55, 0.75, 0.05))

ggsave(file.path(cfg$SVM_OUTPUT_DIR, "discovery_network_specific_analyses.png"), disc_plot, width=4.8, height=3.5, dpi=300)


disc_plot


replication_network_accuracies <- cbind(replication_network_accuracies, netColor)
replication_ordered <- replication_network_accuracies[order(replication_network_accuracies$Accuracy, decreasing=FALSE), ]
replication_network_accuracies$netColor <- factor(replication_network_accuracies$netColor)


rep_plot <- ggplot(replication_network_accuracies, aes(x=reorder(Network, +Accuracy), y=Accuracy, fill=netColor)) + geom_bar(stat='identity') + 
  scale_fill_identity() + theme(legend.position="none") + theme(axis.text.x = element_text(size= 12), axis.text.y = element_text(size= 12), axis.title = element_text(size=18)) +
  xlab("Network") + ylab("Model Performance") + coord_cartesian(ylim = c(0.55, 0.75)) + scale_y_continuous(breaks=seq(0.55, 0.75, 0.05))

ggsave(file.path(cfg$SVM_OUTPUT_DIR, "replication_network_specific_analyses.png"), rep_plot, width=4.8, height=3.5, dpi=300)

rep_plot