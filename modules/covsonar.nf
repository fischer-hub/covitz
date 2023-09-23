process covsonar {
  input:
    seqs

  output:
    path ''

  script:
    """
      sonar.py add --db $params.database $seqs
      sonar.py match --db $params.database >
    """
}
