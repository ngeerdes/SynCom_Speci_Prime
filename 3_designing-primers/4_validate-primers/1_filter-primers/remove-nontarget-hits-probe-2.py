from Bio import SeqIO  # type: ignore
import sys 
import re

def filter_primers_by_blast(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and record significant hits
    hits = {}
    with open(blast_file, 'r') as blast:
        for line in blast:
            fields = line.strip().split('\t')
            query_id = fields[0]
            alignment_length = int(fields[3])  # Alignment length (4th column in BLAST format 6)
            mismatches = int(fields[4])        # Mismatches (5th column in BLAST format 6)

            # Record hits that meet the criteria
            if alignment_length >= 17 and mismatches == 0:
                base_name = re.sub(r'_(left|right|internal)$', '', query_id)
                hits.setdefault(base_name, set()).add(query_id.split('_')[-1])  # e.g., 'left', 'right', 'internal'

    # Step 2: Identify oligo groups to remove (L/R and internal both have hits)
    grouped_oligos = set()
    print("Hits found:")
    for base_name, hit_types in hits.items():
        print(f"{base_name}: {hit_types}")
        if ('left' in hit_types and 'right' in hit_types) and ('internal' in hit_types):
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