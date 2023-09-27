process risk_assessment {

  publishDir "$params.outdir/03-RISK-ASSESSMENT", pattern: 'clusters.tsv', mode: 'copy'
  label 'risk_assessment'

  input:
    path clades
    path mutations
    path breakfast_clusters
    path identity_clusters
    path lineage_aliases

  output:
    path 'risk.csv'

  script:
    """
        risk_score.py $clades $mutations $breakfast_clusters $identity_clusters $params.lin_aliases $params.de_esc_vars $params.th_yellow $params.th_red
    """
}
