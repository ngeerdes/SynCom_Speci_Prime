# Define the isolates array
isolates=("PvR061" "PvR090" "PvR096" "PvR101" "PvR102" "PvR112" "PvR115")

# Loop through each isolate 
for isolate in "${isolates[@]}"; do
    python parsing-syncom-primer-blast.py \
        "${isolate}.syncom.blast.out" 
done

