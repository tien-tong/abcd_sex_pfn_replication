library(R.matlab)
library(dplyr)
library(magrittr)
library(tibble)
library(ggplot2)
library(data.table)
library(ggplot2)
library(hexbin)
library(matrixStats)
library(plotrix)
library(scales)
library(gifti)

# File paths come from CONFIG.txt at the repo root (or $PFN_CONFIG); see pfn_config.R
.repo <- normalizePath(c(gsub("~+~", " ", sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE)), fixed = TRUE), getwd())[1])
while (!file.exists(file.path(.repo, "pfn_config.R")) && dirname(.repo) != .repo) .repo <- dirname(.repo)
source(file.path(.repo, "pfn_config.R"))
cfg <- load_config(Sys.getenv("PFN_CONFIG", file.path(.repo, "CONFIG.txt")))
theme_set(theme_classic(base_size = 16))

#brain input is from SVM run 100x
# read in LH parc
lh_schaefer1000 <- read.table(cfg$SCHAEFER1000_LABELS_CSV)
lh_schaefer1000 <- lh_schaefer1000[1:10242,]
# read in color lookup table
lh_schaefer1000_ct <- read.table(cfg$SCHAEFER1000_CTTABLE_CSV)
lh_schaefer1000_ct_500 <- as.data.frame(lh_schaefer1000_ct[-1,])
colnames(lh_schaefer1000_ct_500) <- "V1"
setDT(lh_schaefer1000_ct_500, keep.rownames = "parcNum")

# read in brain img data
#data_brain1 <- readMat("/cbica/projects/funcParcelSexDiff/results/PredictionAnalysis/SVM/2fold_CSelect_Cov_SubIndex/Sex_CovAgeMotion/Permutation/res_MultiTimes/AtlasLoading/WeightVisualize_Sex_SVM_2fold_CSelect_Cov_MultiTimes/w_Brain_Sex_Abs_sum.mat")
#data_brain <-data_brain1$w.Brain.Sex.Abs.sum.lh
#data_brain1 <- readgii('/Users/ashfrana/Desktop/code/abcd_sex_pfn_replication/genetics/gams_gii_files/gams_uncorrected_discovery_LH.fsaverage5.func.gii')
# Which map to test: gams_uncorrected_discovery, gams_uncorrected_replication, gams_fdr_discovery or gams_fdr_replication
# (the <map_name>_LH.fsaverage5.func.gii files made by fslr_to_fsaverage5.sh); pass as the first argument or edit here
args <- commandArgs(trailingOnly = TRUE)
map_name <- if (length(args) >= 1) args[1] else "gams_uncorrected_replication"
map_label <- sub("^gams_", "", map_name)
data_brain1 <- readgii(file.path(cfg$GAMS_GII_DIR, paste0(map_name, "_LH.fsaverage5.func.gii")))
data_brain <- data_brain1$data$normal

# parcellate data
data_vec <- as.vector(data_brain)
data_parc_lh <- cbind(data_vec, lh_schaefer1000) %>% as_tibble() %>% group_by(lh_schaefer1000) %>% summarise(wt_mean = mean(data_vec))

#order by parcel number for rotations
data_parc_lh <- subset(data_parc_lh, lh_schaefer1000 != "65793")
data_parc_lh_parcnum <- data_parc_lh
data_parc_lh_parcnum$parcNum <- "NA"

for (i in 1:500){
  for (j in 1:500){
    if (data_parc_lh_parcnum$lh_schaefer1000[i] == lh_schaefer1000_ct_500$V1[j]){
      data_parc_lh_parcnum$parcNum[i] <- lh_schaefer1000_ct_500$parcNum[j] }}}

data_parc_lh_parcnum$parcNum <- as.numeric(data_parc_lh_parcnum$parcNum)
data_parc_lh_parcnum_sort <- data_parc_lh_parcnum[order(data_parc_lh_parcnum$parcNum),]


###read in gene data
geneinfo <- readMat(cfg$AHBA_ROI_GENE_MAT)
geneinfo1 <- lapply(geneinfo, unlist, use.names=FALSE)
geneMat <- as.data.frame(geneinfo1$parcelExpression)
geneMat1 <- subset(geneMat, select = -V1)
gene <- read.csv(cfg$GENE_SYMBOL_CSV,header=TRUE)
colnames(gene) <- "V1"
colnames(geneMat1) <- gene$V1
geneMat2 <- cbind(lh_schaefer1000_ct_500, geneMat1)
geneMat2$parcNum <- as.numeric(geneMat2$parcNum)
geneMat2_sort <- geneMat2[order(geneMat2$parcNum),]
geneMat2_sort_500 <- subset(geneMat2_sort, select=-V1)


#merge img, gene, and centroid coord. remove parcels with missing gene data
img_geneMatChrom_500 <- merge(data_parc_lh_parcnum_sort,geneMat2_sort_500, by="parcNum")


rois <- read.csv(cfg$SCHAEFER1000_CENTROIDS_CSV)
roislh <- rois[1:500,]

img_geneMatChrom_roi_500 <- merge(roislh, img_geneMatChrom_500, by.x = "RoiLabel", by.y= "parcNum",all = FALSE)
img_geneMatChrom_roi_500_comp <- subset(img_geneMatChrom_roi_500, !is.nan(img_geneMatChrom_roi_500[[10]])) ##if add more columns, change "10". This is the complete DF. Any subsets below should come from here/match this order.


data_parc_lh_sort_500_comp <- subset(img_geneMatChrom_roi_500_comp, select=wt_mean)


othercols <- c(colnames(rois), "lh_schaefer1000", "wt_mean")
geneMatChrom_500_comp <- img_geneMatChrom_roi_500_comp[(length(othercols)+1):(length(colnames(img_geneMatChrom_roi_500_comp)))]




#correlate sorted img and gene data (medial wall value removed in both) for GO enrichements
rankedGeneList <- sapply(1:15745, function(x) cor(data_parc_lh_sort_500_comp,geneMatChrom_500_comp[,x]))
rankedGeneList1<- cbind(gene, rankedGeneList)
rankedGeneList2 <- rankedGeneList1[with(rankedGeneList1, order(-rankedGeneList)),]
rankedGeneList3 <- subset(rankedGeneList2, select = V1)
write.csv(rankedGeneList3, file.path(cfg$GO_ENRICHMENT_DIR, paste0("RankedGeneList_", sub("^gams_(uncorrected|fdr)_(discovery|replication)$", "gams_\\2_\\1", map_name), "_Cor_schaefer1000Net7_20240808.csv")), row.names = FALSE,  quote=FALSE)