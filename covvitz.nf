input_seqs = Channel.fromPath( params.input_seqs, checkIfExists: true )


workflow {
  covsonar(input_seqs)
  count_ambigous(input_seqs)
  count_mutations(covsonar.out)
  breakfast(covsonar.out)
}
