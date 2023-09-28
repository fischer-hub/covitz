process count_mutations {

  publishDir "$params.outdir/02-STATISTICS", pattern: 'mutation_count.csv', mode: 'copy'
  label 'count_mutations'

  input:
    path mutation

  output:
    path 'mutation_count.csv'

  script:
    """
      # print seq names to csv file
      echo "sequence_name," > seq_names.csv
      tail -n +2 $mutation | echo "\$(cut -d\$'\\t' -f 1)," >> seq_names.csv

      # count nuc mutations
      echo "nuc_mutations," >> nuc_mutations.csv
      tail -n +2 $mutation | cut -d\$'\\t' -f 20 | while read LINE; do echo "\$(echo \$LINE | wc -w)," >> nuc_mutations.csv ; done 

      # count aa mutations
      echo "aa_mutations," >> aa_mutations.csv
      tail -n +2 $mutation | cut -d\$'\\t' -f 21 | while read LINE; do echo "\$(echo \$LINE | wc -w)," >> aa_mutations.csv ; done 

      # merge seq names and nuc mutations
      paste seq_names.csv nuc_mutations.csv aa_mutations.csv > mutation_count.csv
    """
}
