# Define an array of isolate IDs 

isolates=("PvR021" "PvR079" "PvR083" "PvR122" "PvR147") 

# Loop through each isolate and execute the Python script 
for isolates in "${isolates[@]}"; do
    python ../primer3-probe-to-fasta.py \
        ../../primers/primer3-out/"${isolates}.txt" \
        ../../primers/primers-fasta/"${isolates}.primers.fasta"
done