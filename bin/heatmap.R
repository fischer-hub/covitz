#!/usr/bin/env -S Rscript --vanilla
library(pheatmap)
library(dplyr)
library(tidyr)
library(viridis)

args <- commandArgs(trailingOnly = TRUE)

path_mutation = args[1]
threshold = args[2]
grouping_param = args[3]

mutation_data <- read.table(path_mutation, header = TRUE, sep = ",")

mutation_counts <- mutation_data %>%
  separate_rows(aa_profile, sep = " ") %>%
  group_by(aa_profile, !!! syms(grouping_param)) %>%
  summarise(count = n()) %>%
  pivot_wider(names_from = aa_profile, values_from = count, values_fill = 0)

#summarize lineages
mutation_counts <- mutation_counts %>%
  group_by(!!! syms(grouping_param)) %>%
  summarise_all(sum)

#number of sequences in each lineage
lineage_counts <- mutation_data %>%
  count(!!! syms(grouping_param))
lineage_counts <- lineage_counts[order(lineage_counts[, grouping_param]), ]


merged_counts <- cbind(mutation_counts,lineage_counts$n)
colnames(merged_counts)[which(colnames(merged_counts) == "lineage_counts$n")] <- "lineage_count"


merged_counts_percent <- merged_counts %>%
  mutate(across(-c(1, ncol(merged_counts)), ~ . / lineage_count))

#filter
merged_counts_filtered_percent <- merged_counts_percent[, apply(merged_counts_percent >= 0.2, 2, any)]


merged_counts_filtered_percent <- merged_counts_filtered_percent %>%
  select(-"lineage_count")

rownames(merged_counts_filtered_percent) <- merged_counts_filtered_percent$grouping_param


png(paste('mutation_profile_heatmap_by_', grouping_param, '.png'), width = 62, height = 9, units = 'cm', res = 300)

#heatmap
pheatmap(
  (merged_counts_filtered_percent[-1]),  
  cluster_rows = FALSE, 
  cluster_cols = FALSE,   
  color = viridis(100), 
  cellwidth = 10,
  cellheight = 20,
  display_numbers = FALSE, 
)

dev.off()


#####spike protein

#keep all mutations in spike protein
merged_counts_spike_percent<- merged_counts_filtered_percent %>%
  select(starts_with("S"))

ordner_mutation <- order(
  as.numeric(gsub("^[^0-9]*([0-9]+).*", "\\1", colnames(merged_counts_spike_percent)))
)

sort_col <- colnames(merged_counts_spike_percent)[ordner_mutation]
merged_counts_spike_percent <- merged_counts_spike_percent[, ordner_mutation]
colnames(merged_counts_spike_percent) <- sort_col


png(paste('mutation_profile_heatmap_by_', grouping_param, 'spike.png'), width = 25, height = 8, units = 'cm', res = 300)

#heatmap
pheatmap(
  (merged_counts_spike_percent[-1]), 
  cluster_rows = FALSE,  
  cluster_cols = FALSE,  
  color = viridis(100),  
  cellwidth = 10,
  cellheight = 20,
  display_numbers = FALSE,  
)

dev.off()

