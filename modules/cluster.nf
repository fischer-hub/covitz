process cluster {

  publishDir "$params.outdir/03-CLUSTERING/cluster", pattern: 'pca_plot.png', mode: 'copy'
  label 'cluster'

  input:
    path seqs

  output:
    path 'pca_plot.png'

  when:
    params.cluster.contains('kmeans')

  script:
    """
    cluster.R $seqs
    """
}
