#!/usr/bin/env python
import csv
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import pandas as pd


msa_file = sys.argv[1]

alignment = AlignIO.read(msa_file, "fasta")

calculator = DistanceCalculator("identity")  # percent
dm = calculator.get_distance(alignment)


csv_filename = "distance_matrix_identity.csv"

with open(csv_filename, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    for row in dm:
        writer.writerow(row)

constructor = DistanceTreeConstructor(calculator, method="nj")
tree = constructor.build_tree(alignment)

tree_filename = "phylogenetic_tree.nwk"
Phylo.write(tree, tree_filename, "newick")

#phylogenetic tree
tree_png="phylogenetic_tree.png"
Phylo.draw(tree, do_show=False)
plt.title("Phylogenetic tree over all sequences")
#plt.figure(figsize=(20, 6)) 

plt.gcf().set_size_inches(10, 25)

plt.savefig(tree_png)
plt.close()


pca = PCA()
pca.fit(1-dm)


# PCA plot
transformed_data = pca.transform(dm)
plt.scatter(transformed_data[:, 0], transformed_data[:, 1])
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('PCA-Plot')
plt.savefig('pca_plot.png')  
plt.close()


 
# plot
dm_df = pd.read_csv(csv_filename)
sns.clustermap(dm_df, metric="correlation", method="single", cmap="icefire", standard_scale=1)
plt.xlabel('Sequence names')
plt.ylabel('Sequence names')
plt.title('Clustered heatmap over sequence identity')
plt.savefig('clustered_heatmap.png')  
plt.close()