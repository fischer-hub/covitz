process breakfast {

  publishDir "$params.outdir/03-CLUSTERING/breakfast", pattern: 'clusters.tsv', mode: 'copy'
  label 'breakfast'

  input:
    mutation_tsv

  output:
    path 'clusters.tsv'

  script:
    """
      breakfast \
        --input-file $mutation_tsv \
        --max-dist 1 \
        --min-cluster-size 5 \
        --outdir results/
      
      cp results/clusters.tsv .
    """
}
