process covsonar {

  publishDir "$params.outdir/01-MUTATIONS", pattern: 'mutations.tsv', mode: 'copy'
  label 'covsonar'

  input:
    path seqs
    path sonar_py
    path database

  output:
    path 'mutations.tsv'

  script:
    """
      # add sequences to covsonar database
      $sonar_py add --noprogress --db $database -f $seqs -t $task.cpus

      # get mutation information
      $sonar_py match --tsv --db $database > mutations.tsv
    """
}
