#!/usr/bin/env python
import pandas as pd
import sys
import re


clades_file     = sys.argv[1]
mutations_file  = sys.argv[2]
escape_cal_path = sys.argv[3]
breakfast_file  = sys.argv[4]
identity_file   = sys.argv[5]

# load escapecalc module from lib path
sys.path.append(escape_cal_path)
import escapecalculator as ec

# open lineage csv file and drop unneccassary cols
clades_df = pd.read_csv(clades_file).iloc[:, :2]

mutations_df = pd.read_csv(mutations_file, sep = '\t')[['accession', 'aa_profile']]

spike_mutations = []

for index, row in mutations_df.iterrows():
    spike_mutations.append([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) > 331 and int(re.findall('[0-9]+', mut)[0]) < 531])


mutations_df['rbd_aa_mutation_pos'] = spike_mutations


# get escape scores from escapecalc
calc = ec.EscapeCalculator()

# get escape scores for mutations
mutations_df['neutralization_retained'] = mutations_df["rbd_aa_mutation_pos"].map(calc.binding_retained)

# merge lineage information
mutations_df = pd.concat([mutations_df.set_index('accession'), clades_df.set_index('taxon')], axis=1, join='inner').reset_index()
mutations_df = mutations_df.sort_values(by=['lineage'], ascending=True)


#for lineage in pd.unique(mutations_df['lineage']):
#    
#    spike_mutations = []
#
#    try:
#        calc = ec.EscapeCalculator(virus = lineage)
#
#        for index, row in mutations_df[mutations_df['lineage'] == lineage].iterrows():
#            spike_mutations.append([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) > 331 and int(re.findall('[0-9]+', mut)[0]) < 531])
#            print(spike_mutations)
#            break
#
#    except Exception as e:
#        print(e)
        
calc = ec.EscapeCalculator(virus = 'A.27')


print(pd.unique(mutations_df['lineage']))





