# Define an array of isolate IDs
isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script
for isolates in "${isolates[@]}"; do
    python ../remove-nontarget-hits-lax-2.py \
        "../../validation/nt/blast-out/${isolates}.nt.blast.out" \
        "../../validation/refsoil/filtered/${isolates}.filtered.syncom.refsoil.primers.fasta" \
        "../../validation/nt/filtered/${isolates}.filtered.syncom.refsoil.nt.primers.fasta"
done


