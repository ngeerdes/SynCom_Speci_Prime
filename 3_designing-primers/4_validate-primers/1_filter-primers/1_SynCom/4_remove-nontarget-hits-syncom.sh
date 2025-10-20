# Define an array of isolate IDs
isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script
for isolates in "${isolates[@]}"; do
    python ../remove-nontarget-hits.py \
        "../../validation/syncom/blast-out/${isolates}.syncom.blast.out.nontarget" \
        "../../validation/syncom/hit-target/${isolates}.hit.target.fasta" \
        "../../validation/syncom/filtered/${isolates}.filtered.syncom.primers.fasta"
done
