process cluster {

  publishDir "$params.outdir/03-CLUSTERING/cluster", pattern: 'clusters.tsv', mode: 'copy'
  label 'cluster'

  input:
    path seqs

  output:
    path 'pca_plot.png'

  script:
    """
    cluster.R $seqs
    """
}
