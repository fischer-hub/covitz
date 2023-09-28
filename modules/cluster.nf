process cluster {

  publishDir "$params.outdir/03-CLUSTERING/cluster/plots", pattern: '*.png', mode: 'copy'
  publishDir "$params.outdir/03-CLUSTERING/cluster/data",  pattern: '*.csv', mode: 'copy'
  label 'cluster'

  input:
    path msa
    path mutations

  output:
    path '*.csv', emit: dist_matrix
    path '*.png', emit: plots

  script:
    """
    cluster.py $msa $mutations
    """
}

process plots {

  publishDir "$params.outdir/03-CLUSTERING/cluster/plots",  pattern: '*.png', mode: 'copy'
  label 'plots'

  input:
    path risk_assessment

  output:
    path '*.png', emit: plots

  script:
    """
    heatmap.R $risk_assessment $params.th_af lineage
    heatmap.R $risk_assessment $params.th_af risk_alert
    """
}