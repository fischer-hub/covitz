process risk_assessment {

  publishDir "$params.outdir/03-RISK-ASSESSMENT", pattern: 'clusters.tsv', mode: 'copy'
  label 'risk_assessment'

  input:
    path clades
    path mutations
    path breakfast_clusters
    path identity_clusters

  output:
    path 'risk.csv'

  script:
    """
        risk_score.py $clades $mutations $breakfast_clusters $identity_clusters
    """
}
