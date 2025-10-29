# this script similarly removes primers with too many hits as remove-nontarget-hits-lax, but instead keeps the primer pairs 
# with the 10 least hits. 

from Bio import SeqIO  # type: ignore
import sys
from collections import defaultdict

def filter_top_10_primers_by_hits(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and count hits for each primer
    primer_hit_counts = defaultdict(int) #Creates a dictionary with default value of 0
    with open(blast_file, 'r') as blast:
        for line in blast:
            fields = line.strip().split('\t')
            query_id = fields[0]  # Primer ID
            primer_hit_counts[query_id] +=1 #everytime you see a query id, add one to its hit count

    # Step 2: Calculate combined hit counts for primer pairs
    primer_pair_hits = {}
    for primer in primer_hit_counts:
        if primer.endswith("_left"):
            base = primer.replace("_left", "")
        elif primer.endswith("_right"):
            base = primer.replace("_right", "")
        elif primer.endswith("_internal"):
            base = primer.replace("_internal", "")

        left = f"{base}_left"
        right = f"{base}_right"
        internal = f"{base}_internal"

        # Calculate combined hits for the pair
        combined_hits = ( 
            primer_hit_counts.get(f"{base}_left", 0) + 
            primer_hit_counts.get(f"{base}_right", 0) +
            primer_hit_counts.get(f"{base}_internal", 0)
        ) 
        primer_pair_hits[base] = combined_hits
    

    # Step 3: Sort primer pairs by combined hit counts and select the top 10 pairs
    sorted_pairs = sorted(primer_pair_hits.items(), key=lambda x: x[1])  # Sort by combined hits 
    print(sorted_pairs)
    top_10_pairs = sorted_pairs[:10]  # Get the top 10 pairs

    # Step 4: Identify primers to keep
    primers_to_keep = set()
    for base, _ in top_10_pairs:
        primers_to_keep.add(f"{base}_left") # Add _left primer
        primers_to_keep.add(f"{base}_right")  # Add _right primer 
        primers_to_keep.add(f"{base}_internal") 

    print(primers_to_keep)

    # Step 5: Filter the FASTA file to include only primers in the top 10 pairs
    with open(output_fasta, 'w') as out_fasta:
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id in primers_to_keep:
                SeqIO.write(record, out_fasta, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python remove-nontarget-hits-lax.py <blast_output_file> <primers_fasta_file> <output_fasta_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    primers_fasta_file = sys.argv[2]
    output_fasta_file = sys.argv[3]

    filter_top_10_primers_by_hits(blast_output_file, primers_fasta_file, output_fasta_file)