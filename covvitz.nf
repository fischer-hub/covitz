input_seqs = Channel.fromPath( params.input_seqs, checkIfExists: true )


workflow {
  covsonar(input_seqs)
}
