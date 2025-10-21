from Bio import SeqIO  # type: ignore
import sys
import re 

def filter_blast_and_map_to_fasta(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and filter for oligos with alignment length of 20 and 0 mismatches
    valid_oligos = set()
    with open(blast_file, 'r') as blast:
        for line in blast:
            fields = line.strip().split('\t')
            query_id = fields[0]
            alignment_length = int(fields[3])  # Alignment length (4th column in BLAST format 6)
            mismatches = int(fields[4])  # Mismatches (5th column in BLAST format 6)

            if alignment_length == 20 and mismatches == 0:
                valid_oligos.add(query_id)

    # Step 2: Group primers by their primer ID 
    grouped_oligos = {} 
    for oligo in valid_oligos: 
        base_name = re.sub(r'_(left|right|internal)$', '', oligo) 
        grouped_oligos.setdefault(base_name, set()).add(oligo) 

    # Step 3: Keep groups that have only all three valid oligos 
    selected_oligos = {p for group in grouped_oligos.values() if len(group) == 3 for p in group}

    # Step 3: Map valid primer pairs back to the FASTA file
    with open(output_fasta, 'w') as out_fasta:
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id in selected_oligos:
                SeqIO.write(record, out_fasta, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <blast_output_file> <primers_fasta_file> <output_fasta_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    primers_fasta_file = sys.argv[2]
    output_fasta_file = sys.argv[3]

    filter_blast_and_map_to_fasta(blast_output_file, primers_fasta_file, output_fasta_file)