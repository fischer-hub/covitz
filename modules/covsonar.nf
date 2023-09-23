process covsonar {

  label 'covsonar'

  input:
    seqs

  output:
    path 'mutations.csv'

  script:
    """
      # add sequences to covsonar database
      $sonar_py add --db $params.database -f $seqs -t $task.cpus

      # get mutation information
      $sonar_py match --db $params.database > mutations.csv
    """
}
