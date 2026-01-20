A primer design resource for the detection of bacterial isolates within a synthetic community

This repository contains scripts to annotate genomes, filter sequences, and design primers for detecting isolates in a synthetic bacterial community. The workflow moves from raw assemblies through annotation to targeted primer generation.

## Repository Structure & Workflow
- **0_set-up**: Environment setup and dependencies  
- **1_prokka**: Genome annotation using Prokka  
- **2_filtering-seqs**: Filtering for unique sequences  
- **3_designing-primers**: Primer design  
- **5_get-primers**: Collects and validates final primers  

## Getting Started
1. Clone repo and set up environments and databases (0_set-up)
   * Installations required: BLAST, Prokka (optional), Primer3
   * Set up a BLAST db containing the SynCom genomes
     ```bash
     # need to concatenate all of the genomes to a single file to make the syncom13 db
     cat *.fasta > combined-genomes.fasta
     # use makeblastdb command on the combined-genomes.fasta
     makeblastdb -in /whereever/genomes/are -dbtype nucl -out /whereever/genomes/are/genome-db
     
3. Annotate genomes (you can skip this step if your genomes have already been annotated)

4. Filter sequences
  * Follow scripts in 2_filtering-seqs in numerical order, replacing paths and file names as needed. 
5. Design primers
  * Follow scripts in 3_designing-primers in numerical order, replacing paths and file names as needed. 
6. Collect validated primers
  * Follow scripts in 5_get-primers in numerical order, replacing paths and file names as needed. 

## License 

## Contact 

Maintained by Nicole Geerdes (ngeerdes@iastate.edu). 
   
