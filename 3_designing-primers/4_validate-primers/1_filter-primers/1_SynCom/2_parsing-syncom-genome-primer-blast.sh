# Define the isolates array
isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate 
for isolate in "${isolates[@]}"; do
    python parsing-syncom-primer-blast.py \
        "${isolate}.syncom.blast.out" 
done

