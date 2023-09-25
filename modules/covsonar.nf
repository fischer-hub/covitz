process covsonar {

  publishDir "$params.outdir/01-MUTATIONS", pattern: 'mutations.tsv', mode: 'copy'
  label 'covsonar'

  input:
    seqs

  output:
    path 'mutations.tsv'

  script:
    """
      # add sequences to covsonar database
      $sonar_py add --noprogress --db $params.database -f $seqs -t $task.cpus

      # get mutation information
      $sonar_py match --tsv --db $params.database > mutations.tsv
    """
}
