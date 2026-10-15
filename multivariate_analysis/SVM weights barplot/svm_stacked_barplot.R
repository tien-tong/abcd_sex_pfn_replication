library(R.matlab)
library(dplyr)
library(magrittr)
library(tibble)
library(ggplot2)
library(data.table)
library(ggpattern)
theme_set(theme_classic(base_size = 16))
library(RcppCNPy)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))

# Which sample to plot: "discovery" or "replication" (Figure 3C); pass as the first argument or edit here
args <- commandArgs(trailingOnly = TRUE)
sample_set <- if (length(args) >= 1) args[1] else "replication"

#read in brain data
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/w_brain_sex_matrix_one_run.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/w_brain_sex_matrix_one_run_replication.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/discovery_haufe_transformed_one_run_weights.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/discovery_haufe_transformed_100_runs_weights_final.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/replication_haufe_transformed_100_runs_weights_final.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/discovery_haufe_transformed_100_runs_weights_071624.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/replication_haufe_transformed_100_runs_weights_071624.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/svm_072324_run/discovery_haufe_transformed_100_runs_weights_072324.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/ABCD GAMs replication/svm_072324_run/replication_haufe_transformed_100_runs_weights_072324.npy")
#data_brain1 <- npyLoad("/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/multivariate_analysis/svm_check_run/discovery_haufe_transformed_100_runs_weights_check.npy")
data_brain1 <- npyLoad(cfg[[paste0("HAUFE_WEIGHTS_", toupper(sample_set), "_NPY")]])
data_brain <-data_brain1

#function to sum negative weights
sumneg <- function(x) sum(x[x<0])
sums_neg<- as.data.frame(apply(data_brain,1,sumneg))

#function to sum positive weights
sumpos <- function(x) sum(x[x>0])
sums_pos<- as.data.frame(apply(data_brain,1,sumpos))

#name columns, make row number the network label, and combine positive and negative sums into 1 df
#the SVM predicts binarizedACE: negative weights = no ACE (0), positive weights = ACE (1).
#They keep the labels "male"/"female" in the sex column because figure_s8_barplots/ reads them.
colnames(sums_neg) <- "weights"
setDT(sums_neg, keep.rownames = "network")
sums_neg$sex <- "male"
sums_neg$weights <- abs(sums_neg$weights)
colnames(sums_pos) <- "weights"
setDT(sums_pos, keep.rownames = "network")
sums_pos$sex <- "female"
sums_all <- rbind(sums_pos, sums_neg)

#function to get sum of absolute value of weights and put in df w corresponding network
sumabs <- function(x) sum(abs(x))
sums_abs<- as.data.frame(apply(data_brain,1,sumabs))
colnames(sums_abs) <- "weights"
setDT(sums_abs, keep.rownames = "network")


#get network ranking based on absolute value so other plots can have networks in the same order
sums_abs$netrank <- rank(sums_abs$weights)
sum_ranks <- subset(sums_abs, select = -c(weights))


#create color labels for the networks
network <- c(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
             13, 14, 15, 16, 17)

netColor <- c("#E76178", "#7499C2", "#F5BA2E", "#7499C2", "#00A131",
              "#AF33AD", "#E443FF", "#E76178", "#E443FF", "#AF33AD",
              "#7499C2", "#E76178", "#7499C2", "#00A131", "#F5BA2E", 
              "#4E31A8", "#F5BA2E")

netName <- c("SM", "VS", "SM", "SM", "VS", "SM", "FP", "AU", "DM", "FP", "VA", 
             "DA", "DA", "DM", "DM", "VA", "FP")

netColorDf <- cbind(network, netColor, netName)


#combine df of sum of abs value of weights with color table
sums_all_col <- merge(sums_all, netColorDf, by = "network")

#make color label an ordered factor so ggplot can match the color to network
sums_all_col$netColorF <- factor(sums_all_col$netColor, ordered =T)



#merge df of rankings with df of pos +neg sums
sums_all_col_rank <- merge(sums_all_col, sum_ranks, by = "network")

sums_all_col_rank <- sums_all_col_rank %>% 
  mutate(network = as.factor(network),netColorF=as.character(netColorF))%>%
  mutate(network = reorder(network,netrank))%>%
  arrange (netrank)
colormap=sums_all_col_rank %>% select(network,netColorF)%>%unique()

colormap <- cbind(colormap, netName)

write.csv(sums_all_col_rank, file.path(cfg$FIGURE_S8_DIR, paste0("svm_", sample_set, "_network_sums_table_check.csv")))


barplot <- ggplot(sums_all_col_rank, aes(x = network, y = weights, fill=network, alpha=factor(sex)))+
  geom_col(position = "stack", color="black") + xlab("Network") + ylab("Weights")+
  scale_alpha_manual(values = c("male"=0.5, "female"=1), guide='none') + scale_fill_manual(values = colormap$netColorF) + scale_y_continuous(limits = c(0, 300), breaks=seq(0, 300, 50), expand = c(0, 0)) +
  geom_col_pattern(aes(pattern_alpha = sex),
                   fill = NA, pattern = 'stripe',
                   pattern_fill = "black",
                   pattern_angle = 45,
                   pattern_density = 0.05,
                   pattern_spacing = 0.03,
                   pattern_key_scale_factor = 0.5) + scale_pattern_alpha_discrete(range = c(0,0.5), labels =c("ACE", "No ACE")) + theme(axis.text.x = element_text(size= 12), axis.text.y = element_text(size= 12), axis.title = element_text(size=18)) + theme(legend.position = "none")

barplot
ggsave(file.path(cfg$SVM_OUTPUT_DIR, paste0("svm_", sample_set, "_barplot_check.png")), plot=barplot, width=4.8, height=3.5, dpi=300)
