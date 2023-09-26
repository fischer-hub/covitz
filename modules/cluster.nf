process cluster {

  publishDir "$params.outdir/03-CLUSTERING/cluster", pattern: 'pca_plot.png', mode: 'copy'
  label 'cluster'

  input:
    path seqs

  output:
    path 'pca_plot.png'

  script:
    """
    cluster.py $seqs
    """
}