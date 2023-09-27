nextflow.enable.dsl = 2

input_seqs = Channel.fromPath( params.input, checkIfExists: true )

include { covsonar }                 from './modules/covsonar.nf'
include { count_ambigous }           from './modules/count_ambigous.nf'
include { count_mutations }          from './modules/count_mutations.nf'
include { breakfast }                from './modules/breakfast.nf'
include { cluster }                  from './modules/cluster.nf'
include { msa }                      from './modules/mafft.nf'
include { pangolin }                 from './modules/pangolin.nf'

workflow {

  pangolin(input_seqs)
  covsonar(input_seqs, pangolin.out)
  count_ambigous(input_seqs)
  count_mutations(covsonar.out.mutations)
  breakfast(covsonar.out.mutations)
  msa(input_seqs)
  cluster(msa.out)
  
}
