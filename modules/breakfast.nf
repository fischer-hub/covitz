process breakfast {

  publishDir "$params.outdir/03-CLUSTERING/breakfast", pattern: 'clusters.tsv', mode: 'copy'
  label 'breakfast'

  input:
    path mutation_tsv

  output:
    path 'clusters.tsv'

  //when:
  //  params.cluster.contains('breakfast')

  script:
    """
      breakfast \
        --input-file $mutation_tsv \
        --max-dist 5 \
        --min-cluster-size 2 \
        --outdir results/ \
        --jobs $task.cpus
      
      cp results/clusters.tsv .
    """
}
