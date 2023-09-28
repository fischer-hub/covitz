process plots_alert {

  publishDir "$params.outdir/05-RISK-ASSESSMENT/plots",  pattern: '*.png', mode: 'copy'
  label 'plots_alert'

  input:
    path risk_assessment
    path dist_matrix

  output:
    path '*.png', emit: plots

  script:
    """
    plot_risk_alert.py $risk_assessment $dist_matrix
    """
}