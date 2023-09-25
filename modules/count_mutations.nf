process count_mutations {

  publishDir "$params.outdir/02-STATISTICS", pattern: 'mutations.csv', mode: 'copy'
  label 'count_mutations'

  input:
    mutation

  output:
    path 'mutation_count.csv'

  script:
    """
      # print seq names to csv file
      echo "sequence_name," > seq_names.csv
      tail -n +2 test | echo "\$(cut -d, -f 1)," >> seq_names.csv

      # count nuc mutations
      echo "nuc_mutations," >> nuc_mutations.csv
      tail -n +2 test | cut -d, -f 20 | while read LINE; do echo "\$(\$LINE | wc -w)," > nuc_mutations.csv ; done 

      # count aa mutations
      echo "aa_mutations," >> aa_mutations.csv
      tail -n +2 test | cut -d, -f 21 | while read LINE; do echo "\$(\$LINE | wc -w)," > aa_mutations.csv ; done 

      # merge seq names and nuc mutations
      paste seq_names.csv nuc_mutations.csv aa_mutations.csv > mutation_count.csv
    """
}
