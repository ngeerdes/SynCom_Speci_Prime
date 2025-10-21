

# Define an array of isolate IDs
isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script
for isolates in "${isolates[@]}"; do
    python ../remove-nontarget-hits.py \
        "../../validation/refsoil/blast-out/${isolates}.refsoil.blast.out" \
        "../../validation/syncom/filtered/${isolates}.filtered.syncom.primers.fasta" \
        "../../validation/refsoil/filtered/${isolates}.filtered.syncom.refsoil.primers.fasta"
done

