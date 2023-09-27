process cluster {

  publishDir "$params.outdir/03-CLUSTERING/cluster", pattern: '*', mode: 'copy'
  label 'cluster'

  input:
    path msa

  output:
    path '*'

  script:
    """
    cluster.py $msa
    """
}