input_seqs = Channel.fromPath( params.input, checkIfExists: true )
database = Channel.fromPath( params.database, checkIfExists: true )
sonar_py = Channel.fromPath( {params.sonar_py ? params.sonar_py : "$projectDir/lib/covsonar/sonar.py"}, checkIfExists: true )

include { covsonar }                 from './modules/covsonar.nf'
include { count_ambigous }           from './modules/count_ambigous.nf'
include { count_mutations }          from './modules/count_mutations.nf'
include { breakfast }                from './modules/breakfast.nf'

workflow {
  covsonar(input_seqs, sonar_py, database)
  count_ambigous(input_seqs)
  count_mutations(covsonar.out)
  breakfast(covsonar.out)
}
