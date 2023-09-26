process pangolin {

  publishDir "$params.outdir/03-LINEAGE-ASSIGNMENT", pattern: 'clades.csv', mode: 'copy'
  label 'pangolin'

  input:
    path seqs

  output:
    path 'clades.csv'

  script:
    """
        pangolin -t $task.cpus $seqs --outfile clades.csv
    """
}

