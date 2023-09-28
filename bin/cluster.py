#!/usr/bin/env python
import csv
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import sys
import seaborn as sns
import pandas as pd
import numpy as np
import umap
from sklearn.cluster import KMeans


msa_file = sys.argv[1]
mutations_data=sys.argv[2]

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
plt.gcf().set_size_inches(10, 25)

plt.savefig(tree_png)
plt.close()


 
# plot
dm_df = pd.read_csv(csv_filename)
sns.clustermap(dm_df, metric="correlation", method="single", cmap="icefire", standard_scale=1)
plt.xlabel('Sequence names')
plt.ylabel('Sequence names')
plt.title('Clustered heatmap over sequence identity')
plt.savefig('clustered_heatmap.png')  
plt.close()

pca = PCA()
pca.fit(dm)


# PCA plot
transformed_data = pca.transform(dm)
plt.scatter(transformed_data[:, 0], transformed_data[:, 1])
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('PCA-Plot')
plt.savefig('pca_plot.png')  
plt.close()
######

#construct umap using identity distance matrix
umap_results = umap.UMAP(metric="precomputed").fit_transform(dm)

num_clusters = 4 

kmeans = KMeans(n_clusters=num_clusters)
cluster_labels = kmeans.fit_predict(umap_results)

plt.scatter(umap_results[:, 0], umap_results[:, 1], c=cluster_labels, cmap='Spectral')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.title('UMAP Embedding')
plt.savefig('umap_plot_cluster.png')
plt.close()


#plot with metadata
metadata = {}
with open(mutations_data, mode="r", newline="") as tsv_file:
    reader = csv.DictReader(tsv_file, delimiter='\t')
    for row in reader:
        sequence_id = row["accession"]  
        lineage = row["lineage"] 
        metadata[sequence_id] = lineage

lineage_to_class = {}
lineage_classes = []
class_counter = 0

for sequence_id, lineage in metadata.items():
    if lineage not in lineage_to_class:
        lineage_to_class[lineage] = class_counter
        class_counter += 1
    lineage_classes.append(lineage_to_class[lineage])

scatter = plt.scatter(transformed_data[:, 0], transformed_data[:, 1], c=lineage_classes, cmap='viridis')
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('PCA-Plot with Lineage')

legend_labels = [lineage for lineage in lineage_to_class.keys()]
unique_colors = scatter.to_rgba(np.unique(lineage_classes))
legend_elements = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=10) for label, color in zip(legend_labels, unique_colors)]

plt.legend(handles=legend_elements, title='Lineage', loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('pca_plot_with_lineage.png', bbox_inches='tight')  
plt.close()

scatter = plt.scatter(umap_results[:, 0], umap_results[:, 1], c=lineage_classes, cmap='viridis')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.title('UMAP Embedding with Lineage')

plt.legend(handles=legend_elements, title='Lineage', loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('umap_plot_with_lineage.png', bbox_inches='tight')  
plt.close()