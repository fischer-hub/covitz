process count_ambigous {

  publishDir "$params.outdir/02-STATISTICS", pattern: 'ambig_base_count.csv', mode: 'copy'
  label 'count_ambigous'

  input:
    seqs

  output:
    path 'ambig_base_count.csv'

  script:
    """
    count_ambig.py $seqs
    """
}
