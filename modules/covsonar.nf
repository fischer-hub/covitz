process covsonar {

  publishDir "$params.outdir/01-MUTATIONS", pattern: 'mutations.tsv', mode: 'copy'
  publishDir "$params.outdir/01-MUTATIONS", pattern: '$params.database', mode: 'copy'
  label 'covsonar'

  input:
    path seqs

  output:
    path 'mutations.tsv'   , emit: mutations
    path "$params.database", emit: database

  script:
    """
      # add sequences to covsonar database
      $params.sonar_py add --db $params.database -f $seqs --cpus $task.cpus --force --cache .

      # get mutation information
      $params.sonar_py match --tsv --db $params.database > mutations.tsv
    """
}
