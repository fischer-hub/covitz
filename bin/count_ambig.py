#!/usr/bin/env python
from Bio import SeqIO
import sys

seq_file = sys.argv[1]
ambiguous_counts = []
sequence_headers = []

for record in SeqIO.parse(seq_file, "fasta"):
    sequence = str(record.seq)
    sequence_headers.append(sequence_headers)
    ambiguous_count = sum(1 for base in sequence if base not in ["A", "C", "G", "T"])
    ambiguous_counts.append(ambiguous_count)

with open('ambig_base_count.csv', 'w' ) as output:
    output.write('sequence_name,ambigous_base_count')
    for i, count in enumerate(ambiguous_counts):
        output.write(f"{sequence_headers[i]},{count}")
