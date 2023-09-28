#!/usr/bin/env python
import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import umap
import sys

meta_data = sys.argv[1]
dm=sys.argv[2]

distance_matrix = pd.read_csv(dm, index_col=0, header=None)

metadata_df = pd.read_csv(meta_data)

pca = PCA(n_components=2) 
principal_components = pca.fit_transform(distance_matrix)

pca_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pca_df['risk_alert'] = metadata_df['risk_alert']  

# PCA
fig, ax = plt.subplots()
colors = {'green': 'green', 'yellow': 'yellow', 'red': 'red'}  

for risk_alert, data in pca_df.groupby('risk_alert'):
    ax.scatter(data['PC1'], data['PC2'], label=risk_alert, color=colors[risk_alert])

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_title('PCA Plot')
ax.legend()

plt.savefig('pca_plot_risk_alert.png')

plt.close()

reducer = umap.UMAP(n_components=2)  
umap_result = reducer.fit_transform(distance_matrix)

umap_df = pd.DataFrame(data=umap_result, columns=['UMAP1', 'UMAP2'])
umap_df['risk_alert'] = metadata_df['risk_alert'] 

# UMAP
fig, ax = plt.subplots()
colors = {'green': 'green', 'yellow': 'yellow', 'red': 'red'} 

for risk_alert, data in umap_df.groupby('risk_alert'):
    ax.scatter(data['UMAP1'], data['UMAP2'], label=risk_alert, color=colors[risk_alert])

ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.set_title('UMAP Plot')
ax.legend()
plt.savefig('umap_plot_risk_alert.png')
plt.close()


