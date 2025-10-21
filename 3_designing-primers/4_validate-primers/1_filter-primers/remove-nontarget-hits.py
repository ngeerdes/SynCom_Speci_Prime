from Bio import SeqIO  # type: ignore
import sys

def filter_primers_by_blast(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and identify primers to remove
    primers_to_remove = set()
    with open(blast_file, 'r') as blast:
        for line in blast:
            fields = line.strip().split('\t')
            query_id = fields[0]
            alignment_length = int(fields[3])  # Alignment length (4th column in BLAST format 6)
            mismatches = int(fields[4])  # Mismatches (5th column in BLAST format 6)

            # Mark primers for removal if alignment length >= 16
            if alignment_length >= 17 and mismatches == 0:
                primers_to_remove.add(query_id)

    # Step 2: Ensure both forward (_left) and reverse (_right) primers are removed if one is flagged
    paired_primers_to_remove = set()
    for primer in primers_to_remove:
        if primer.endswith("_left"):
            paired_primer = primer.replace("_left", "_right")
        elif primer.endswith("_right"):
            paired_primer = primer.replace("_right", "_left")
        else:
            continue  # Skip if the primer does not follow the naming convention

        # Add both primers to the removal set
        paired_primers_to_remove.add(primer)
        paired_primers_to_remove.add(paired_primer)

    # Step 3: Filter the FASTA file to exclude primers with non-target hits
    with open(output_fasta, 'w') as out_fasta:
        for record in SeqIO.parse(fasta_file, "fasta"):
            if record.id not in paired_primers_to_remove:
                SeqIO.write(record, out_fasta, "fasta")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python remove-nontarget-hits.py <blast_output_file> <primers_fasta_file> <output_fasta_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    primers_fasta_file = sys.argv[2]
    output_fasta_file = sys.argv[3]

    filter_primers_by_blast(blast_output_file, primers_fasta_file, output_fasta_file)

    ## USAGE example(s): This script filters primers based on BLAST results, removing those with non-target hits
    #    python remove-nontarget-hits.py PvR045-parsed-primers.fasta.renamed.syncom13.blast.out.nontarget ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits.filtered.syncom13 

    #    python remove-nontarget-hits.py PvR045-parsed-primers.fasta.renamed.filtered.syncom13.refsoil.blast.out ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits.filtered.syncom13 ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits.filtered.syncom13.refsoil

    #    python remove-nontarget-hits.py PvR045-parsed-primers.fasta.renamed.filtered.syncom13.refsoil.nt.blast.out ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits.filtered.syncom13.refsoil ../primer3-filtered/PvR045-parsed-primers.fasta.renamed.targethits.filtered.syncom13.refsoil.nt
