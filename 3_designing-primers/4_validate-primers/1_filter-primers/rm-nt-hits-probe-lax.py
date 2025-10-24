# This script should be used if remove-nontarget-hits-probe.py is too strict (does not produce any primers in output)
from Bio import SeqIO  # type: ignore
import sys
import re

def filter_primers_by_blast(blast_file, fasta_file, output_fasta):
    # Step 1: Parse the BLAST output and record significant hits
    hits = {}
    print(f"Reading BLAST file: {blast_file}")
    with open(blast_file, 'r') as blast:
        for line_number, line in enumerate(blast, start=1):
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) < 5:
                print(f"Skipping line {line_number}, not enough columns: {line}")
                continue
            query_id = fields[0]
            try:
                alignment_length = int(fields[3])
                mismatches = int(fields[4])
            except ValueError:
                print(f"Skipping line {line_number}, non-integer values: {line}")
                continue

            print(f"Line {line_number}: Query={query_id}, Length={alignment_length}, Mismatches={mismatches}")

            # Record hits that meet the criteria
            if alignment_length >= 17 and mismatches == 0:
                base_name = re.sub(r'_(left|right|internal)$', '', query_id)
                hit_type = query_id.split('_')[-1]
                print(f"Recording hit: Base={base_name}, Type={hit_type}")
                hits.setdefault(base_name, set()).add(hit_type)

    # Step 2: Identify oligo groups to remove (any group with 2 or more hits)
    grouped_oligos = set()
    print("\nHits found per group:")
    for base_name, hit_types in hits.items():
        print(f"{base_name}: {hit_types}")
        if len(hit_types) >= 2:
            grouped_oligos.add(base_name)

    print(f"\nGroups to remove (>=2 hits): {grouped_oligos}\n")

    # Step 3: Write all sequences whose group is NOT in the removal list
    written_count = 0
    with open(output_fasta, 'w') as out_fasta:
        for record in SeqIO.parse(fasta_file, "fasta"):
            print(f"Checking FASTA record: {record.id}")
            base_name = re.sub(r'_(left|right|internal)$', '', record.id)
            if base_name not in grouped_oligos:
                SeqIO.write(record, out_fasta, "fasta")
                written_count += 1
                print(f"Writing record: {record.id}")
            else:
                print(f"Skipping record (grouped oligo): {record.id}")

    print(f"\nFinished writing {written_count} sequences to {output_fasta}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python remove-nontarget-hits.py <blast_output_file> <primers_fasta_file> <output_fasta_file>")
        sys.exit(1)

    blast_output_file = sys.argv[1]
    primers_fasta_file = sys.argv[2]
    output_fasta_file = sys.argv[3]

    filter_primers_by_blast(blast_output_file, primers_fasta_file, output_fasta_file)