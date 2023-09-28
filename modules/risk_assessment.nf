process risk_assessment {

  publishDir "$params.outdir/05-RISK-ASSESSMENT", pattern: 'risk_assessment.csv', mode: 'copy'
  label 'risk_assessment'

  input:
    path clades
    path mutations
    path breakfast_clusters
    path identity_clusters

  output:
    path 'risk_assessment.csv'

  script:
    """
        risk_score.py $clades $mutations $params.esc_calc_path $breakfast_clusters $identity_clusters $params.lin_aliases $params.de_esc_vars $params.th_yellow $params.th_red
    """
}