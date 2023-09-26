import csv
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


alignment = AlignIO.read("results/msa.fasta", "fasta")

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
plt.savefig(tree_png)


pca = PCA()
pca.fit(dm)


# PCA plot
transformed_data = pca.transform(dm)
plt.scatter(transformed_data[:, 0], transformed_data[:, 1])
plt.xlabel('PC 1')
plt.ylabel('PC 2')
plt.title('PCA-Plot')
plt.savefig('pca_plot.png')  
