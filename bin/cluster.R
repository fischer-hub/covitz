#!/usr/bin/env -S Rscript --vanilla
library(Biostrings)
library(ggplot2)

args <- commandArgs(trailingOnly = TRUE)

sequences <- readDNAStringSet(args[0])
dm <- stringDist(sequences)

write.table(dm, file = "distance_matrix.csv", sep = ",")

pca <- prcomp(dm, center = TRUE, scale = FALSE)
dtp <- data.frame(pca$x[,1:2])

pca_plot <- ggplot(data = dtp) + 
  geom_point(aes(x = PC1, y = PC2)) + 
  ggtitle("PCA over paiwise sequence distance matrix") +
  theme(plot.title = element_text(hjust = 0.5)) +
  xlab(paste0("PC1: ",   summary(pca)$importance[2,1] * 100, "% variance")) +
  ylab(paste0("PC2: ",   summary(pca)$importance[2,2] * 100,"% variance"))

ggsave('pca_plot.png', pca_plot)