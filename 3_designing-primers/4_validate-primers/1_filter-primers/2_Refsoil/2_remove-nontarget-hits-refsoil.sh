
# ended up using the rm-nt-hits-probe-lax.py script for PvR147 because the original was too strict 
# Used remove-nontarget-hits-probe.py for all other isolates... in the pipeline it would be useful to check if any of the isolates have zero
# output with the stricter script, and if so then run the lax version for those isolates only
# Define an array of isolate IDs
isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script
for isolates in "${isolates[@]}"; do
    python ../remove-nontarget-hits-probe.py \
        "../../validation/refsoil/blast-out/${isolates}.refsoil.blast.out" \
        "../../validation/syncom/filtered/${isolates}.filtered.syncom.primers.fasta" \
        "../../validation/refsoil/filtered/${isolates}.filtered.syncom.refsoil.primers.fasta"
done

