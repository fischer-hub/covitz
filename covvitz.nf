nextflow.enable.dsl = 2

input_seqs = Channel.fromPath( params.input, checkIfExists: true )

include { covsonar }                 from './modules/covsonar.nf'
include { count_ambigous }           from './modules/count_ambigous.nf'
include { count_mutations }          from './modules/count_mutations.nf'
include { breakfast }                from './modules/breakfast.nf'
include { cluster }                  from './modules/cluster.nf'
include { plots }                    from './modules/cluster.nf'
include { msa }                      from './modules/mafft.nf'
include { pangolin }                 from './modules/pangolin.nf'
include { risk_assessment }          from './modules/risk_assessment.nf'

log.info """\033[95m
     ____  _      __   ____                             
    / __ \\(_)____/ /__/ __ \\____ _____  ____ ____  _____
   / /_/ / / ___/ //_/ /_/ / __ `/ __ \\/ __ `/ _ \\/ ___/
  / _, _/ (__  ) ,< / _, _/ /_/ / / / / /_/ /  __/ /    
 /_/ |_/_/____/_/|_/_/ |_|\\__,_/_/ /_/\\__, /\\___/_/     
                                     /____/ 

 Saving the world one sequence at a time.
 = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
 \033[94m
 CONFIG:
 ---------------------------------------------------------------------
    input file:                     $params.input
    database file:                  $params.database
    output directory:               $params.outdir
    covsonar directory:             $params.sonar_py
    lineage alias file:             $params.lin_aliases
    de-escalated variants file:     $params.de_esc_vars
    escape calculator directory:    $params.esc_calc_path
    cpus per task:                  $params.cpu_per_task 
    yellow alert threshold:         $params.th_yellow 
    red alert threshold:            $params.th_red 
    allel frequency threshold:      $params.th_af
\033[0m""".stripIndent()


workflow {

  pangolin(input_seqs)
  covsonar(input_seqs, pangolin.out)
  count_ambigous(input_seqs)
  count_mutations(covsonar.out.mutations)
  breakfast(covsonar.out.mutations)
  msa(input_seqs)
  cluster(msa.out, covsonar.out.mutations)
  risk_assessment(pangolin.out, covsonar.out.mutations, breakfast.out, cluster.out.dist_matrix)
  plots(risk_assessment.out)
  
}
