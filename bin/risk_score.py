#!/usr/bin/env python
import pandas as pd
import sys
import re
import json


clades_file     = sys.argv[1]
mutations_file  = sys.argv[2]
escape_cal_path = sys.argv[3]
breakfast_file  = sys.argv[4]
identity_file   = sys.argv[5]
lineage_aliases = sys.argv[6]
de_esc_vars     = sys.argv[7]
th_yellow       = int(sys.argv[8])
th_red          = int(sys.argv[9])

# load breakfast file
breakfast_df = pd.read_csv(breakfast_file, sep = '\t')

# load de-escalated variants
with open(de_esc_vars) as f:
    de_esc_vars_lst = f.read().splitlines()

esc_calc_lineages = ['BA.1', 'BA.2', 'BA.2.75', 'BA.5', 'BQ.1.1', 'D614G', 'SARS', 'XBB'] # lineage xbb.1.5 crashes the caclulator smh
esc_calc_lineages_short = dict(zip([x.split('.')[0] for x in esc_calc_lineages], esc_calc_lineages))

# load aliases from alias_key.json
with open(lineage_aliases) as f_in:
    alias_dict = json.load(f_in)

# filter dict for lineages we actually have in the escape calc
alias_dict_long = {key: alias_dict[key] for key in esc_calc_lineages if key in alias_dict}
alias_dict_short = {key: alias_dict[key] for key in [x.split('.')[0] for x in esc_calc_lineages] if key in alias_dict}
alias_dict = dict(alias_dict_long)
alias_dict.update(alias_dict_short)


# load escapecalc module from lib path
sys.path.append(escape_cal_path)
import escapecalculator as ec

# open lineage csv file and drop unneccassary cols
clades_df = pd.read_csv(clades_file).iloc[:, :2]

mutations_df = pd.read_csv(mutations_file, sep = '\t')[['accession', 'aa_profile']]

spike_mutations = []

for index, row in mutations_df.iterrows():
    spike_mutations.append([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 331 and int(re.findall('[0-9]+', mut)[0]) <= 531])


mutations_df['rbd_aa_mutation_pos'] = spike_mutations


# get escape scores from escapecalc
calc = ec.EscapeCalculator()

# get escape scores for mutations
mutations_df['neutralization_retained'] = mutations_df["rbd_aa_mutation_pos"].map(calc.binding_retained)

# merge lineage information
mutations_df = pd.concat([mutations_df.set_index('accession'), clades_df.set_index('taxon')], axis=1, join='inner').reset_index()
mutations_df = mutations_df.sort_values(by=['lineage'], ascending=True)

relative_escape_score = []

# calculate escape score relative to closest lineage
for lineage in pd.unique(mutations_df['lineage']):
    
    spike_mutations = []

    if lineage in esc_calc_lineages:
        # lineage detected by pangolin is already available in esc calc
        calc = ec.EscapeCalculator(virus = lineage)
        
        for index, row in mutations_df[mutations_df['lineage'] == lineage].iterrows():
            relative_escape_score.append(calc.binding_retained([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 331 and int(re.findall('[0-9]+', mut)[0]) <= 531]).round(3))
    
    elif lineage in alias_dict.values():
        # set esc calc lineage to closest mapped lineage from alias dict
        calc = ec.EscapeCalculator(virus = list(alias_dict.keys())[list(alias_dict.values()).index(lineage)])

        for index, row in mutations_df[mutations_df['lineage'] == lineage].iterrows():
            relative_escape_score.append(calc.binding_retained([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 331 and int(re.findall('[0-9]+', mut)[0]) <= 531]).round(3))
    
    elif lineage.split('.')[0] in esc_calc_lineages_short:
        # set esc calc lineage to closest mapped lineage from alias dict
        calc = ec.EscapeCalculator(virus = esc_calc_lineages_short[lineage.split('.')[0]])

        for index, row in mutations_df[mutations_df['lineage'] == lineage].iterrows():
            relative_escape_score.append(calc.binding_retained([int(re.findall('[0-9]+', mut)[0]) for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 331 and int(re.findall('[0-9]+', mut)[0]) <= 531]).round(3))
    
    else:
        # coulnt map detected lineage to available lineage in calc, put NA
        for index, row in mutations_df[mutations_df['lineage'] == lineage].iterrows():
            relative_escape_score.append('NA')

mutations_df['relative_neutralization_retained'] = relative_escape_score

# check if seq was linmeage assigned into a de escalated lineage
mutations_df['de_escalated'] = [ lineage in de_esc_vars_lst for lineage in mutations_df['lineage'] ]

# count ntd and rbd mutations
num_ntd_mut = []
num_rbd_mut = []

for index, row in mutations_df.iterrows():

    num_ntd_mut.append(sum(1 for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 14 and int(re.findall('[0-9]+', mut)[0]) <= 305))
    num_rbd_mut.append(sum(1 for mut in row['aa_profile'].split(' ') if mut.startswith('S') and int(re.findall('[0-9]+', mut)[0]) >= 319 and int(re.findall('[0-9]+', mut)[0]) <= 541))


mutations_df['num_ntd_mut'] = num_ntd_mut
mutations_df['num_rbd_mut'] = num_rbd_mut

# merge cluster information
mutations_df = pd.concat([mutations_df.set_index('index'), breakfast_df.set_index('id')], axis=1, join='inner').reset_index()

risk_scores = []
risk_level = []
risk_alert = ['green', 'yellow', 'red']
risk_alerts = []

for index, row in mutations_df.iterrows():

    # we scale rbd muts up with their escape score: x * (1 + 1 - y) - this is maybe not a good scaling but has to be enough for now
    immune_escape = row['relative_neutralization_retained'] * 2 if (row['relative_neutralization_retained'] != 'NA') else row['neutralization_retained']
    risk_score = int(row['num_rbd_mut']) * (1 + 1 - int(immune_escape)) + int(row['num_ntd_mut'])
    risk_scores.append(risk_score)

    # assign risk level based on risk scoring
    if risk_score < th_yellow:
    
        risk_level.append(1)
    
    elif risk_score < th_red:
        
        risk_level.append(2)
    else:

        risk_level.append(3)
    
    # lower risk level if lineage is de escalated lineage
    if row['de_escalated']:
        
        if risk_level[index] > 1:
            
            risk_level[index] - 1

    # scale risk with cluster info?


    # assign risk alert based on level
    risk_alerts.append(risk_alert[risk_level[index] - 1])



    
mutations_df['risk_score'] = risk_scores
mutations_df['risk_alert'] = risk_alerts

mutations_df = mutations_df.sort_values(by=['risk_score'], ascending=False)

mutations_df.to_csv('risk_assessment.csv')







