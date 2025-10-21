import sys

def parse_primer3_output(primer3_output, fasta_output):
    with open(primer3_output, "r") as infile, open(fasta_output, "w") as outfile:
        sequence_id = None
        primer_count = 1

        for line in infile:
            line = line.strip()
            if line.startswith("SEQUENCE_ID="):
                sequence_id = line.split("=")[1]
                primer_count = 1  # Reset primer count for each new sequence
            elif line.startswith("PRIMER_LEFT_") and "_SEQUENCE=" in line:
                primer_num = line.split("_")[2]  # Extract primer number
                primer_seq = line.split("=")[1]
                outfile.write(f">{sequence_id}_primer{primer_num}_left\n{primer_seq}\n")
            elif line.startswith("PRIMER_RIGHT_") and "_SEQUENCE=" in line:
                primer_num = line.split("_")[2]  # Extract primer number
                primer_seq = line.split("=")[1]
                outfile.write(f">{sequence_id}_primer{primer_num}_right\n{primer_seq}\n") 
            elif line.startswith("PRIMER_INTERNAL_") and "_SEQUENCE=" in line:
                primer_num = line.split("_")[2]  # Extract primer number
                primer_seq = line.split("=")[1]
                outfile.write(f">{sequence_id}_primer{primer_num}_internal\n{primer_seq}\n")

def main():
    if len(sys.argv) != 3:
        print("Usage: python primer3_probe_to_fasta.py <primer3_output_file> <fasta_output_file>")
        sys.exit(1)

    primer3_output = sys.argv[1]
    fasta_output = sys.argv[2]

    parse_primer3_output(primer3_output, fasta_output)
    print(f"FASTA file for BLAST query created: {fasta_output}")

if __name__ == "__main__":
    main()