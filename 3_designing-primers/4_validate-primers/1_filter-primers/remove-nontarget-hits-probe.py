from Bio import SeqIO  # type: ignore
import sys 
import re

def filter_primers_by_blast(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and identify primers to remove
    oligos_to_remove = set()
    with open(blast_file, 'r') as blast:
        for line in blast:
            fields = line.strip().split('\t')
            query_id = fields[0]
            alignment_length = int(fields[3])  # Alignment length (4th column in BLAST format 6)
            mismatches = int(fields[4])  # Mismatches (5th column in BLAST format 6)

            # Mark primers for removal if alignment length >= 16
            if alignment_length >= 17 and mismatches == 0:
                oligos_to_remove.add(query_id)

    # Step 2: Group primers by their primer ID for removal
    grouped_oligos = set() 
    for oligo in oligos_to_remove: 
        base_name = re.sub(r'_(left|right|internal)$', '', oligo) 
        grouped_oligos.add(base_name)  

 # Step 3: Write all sequences whose group is NOT in the removal list
    with open(output_fasta, 'w') as out_fasta:
        for record in SeqIO.parse(fasta_file, "fasta"):
            base_name = re.sub(r'_(left|right|internal)$', '', record.id)
            if base_name not in grouped_oligos:
                SeqIO.write(record, out_fasta, "fasta")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python remove-nontarget-hits.py <blast_output_file> <primers_fasta_file> <output_fasta_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    primers_fasta_file = sys.argv[2]
    output_fasta_file = sys.argv[3]

    filter_primers_by_blast(blast_output_file, primers_fasta_file, output_fasta_file)
