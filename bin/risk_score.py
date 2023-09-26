#!/usr/bin/env python
import pandas as pd
import sys


clades_file = sys.argv[1]
mutations_file = sys.argv[2]
escape_cal_path = sys.argv[3]
#clusters_file = sys.argv[3]

# load escapecalc module from lib path
sys.path.append(escape_cal_path)
import escapecalculator as ec

# open lineage csv file and drop unneccassary cols
clades_df = pd.read_csv(clades_file).iloc[:, :2]

mutations_df = pd.read_csv(mutations_file, sep = '\t')[['accession', 'aa_profile']]

spike_mutations = []

for index, row in mutations_df.iterrows():
    spike_mutations.append(' '.join([mut for mut in row['aa_profile'].split(' ') if mut.startswith('S')]))


mutations_df['spike_aa_mutations'] = spike_mutations

# get escape scores from escapecalc
calc = ec.EscapeCalculator()






