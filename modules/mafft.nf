process msa {

  publishDir "$params.outdir/03-CLUSTERING/cluster", pattern: 'msa.fasta', mode: 'copy'
  label 'msa'

  input:
    path seqs

  output:
    path 'msa.fasta'

  script:
    """
        if [[ $seqs == *".gz"* ]]; then
            echo "gzipped" 
            gunzip -c \$(realpath $seqs) > seqs.fasta
            mafft --maxiterate 0 --retree 1 --thread $task.cpus seqs.fasta > msa.fasta
        else
            mafft --maxiterate 0 --retree 1 --thread $task.cpus $seqs > msa.fasta
        fi
    """
}

