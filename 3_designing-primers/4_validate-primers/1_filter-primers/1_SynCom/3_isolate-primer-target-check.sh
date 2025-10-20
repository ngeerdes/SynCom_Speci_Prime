
# Define an array of isolate IDs 

isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script 
for isolates in "${isolates[@]}"; do
    python isolate-primer-target-check.py \
        "../../validation/syncom/blast-out/${isolates}.syncom.blast.out.target" \
        "../../primers/primers-fasta/${isolates}.primers.fasta.renamed" \
        "../hit-target/${isolates}.hit.target.fasta"
done
