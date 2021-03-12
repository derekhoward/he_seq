#!/bin/bash

# this version of the script is setup to run with the *.bam files of interest being in a single directory

##this code is RSEM quantification from reads previously aligned by STAR
##this code assumes data is given as STAR-acceptable files and are compressed... future to do: add argument/option for specifying data format and compression status
##it would be good if files have short names with unique identifiers, to improve prefix funcionality
# use it as ./rsem_pipev2.sh output_path/ /nethome/kcni/dhoward/he_seq/data/results/STAR_results/coord_bams/ /nethome/kcni/dhoward/rsem_reference/

# rsem-calculate-expression --bam /nethome/kcni/dhoward/test1/Aligned.toTranscriptome.out.bam /nethome/kcni/dhoward/test1/processed_rsem/ /nethome/kcni/dhoward/test1/rsem_output/

output_path=$1  #parent directory where all the data/fastqfiles are stored (absolute path)
bam_dir=$2 # directory which contains outputs from STAR (with directories for each sample that should contain *.bam outputs from STAR)
rsem_ref_path=$3 #path to preprocessed RSEM reference index


#initial setup/prep
cd $output_path
mkdir RSEM_scripts # will place each individual script for each sample in here
mkdir RSEM_results # will put each directory of RSEM outputs in here

scripts_dir="${output_path}RSEM_scripts/"
output_dir="${output_path}RSEM_results/" # path for output of RSEM processing

echo "Processing files from $bam_dir"

cd $bam_dir

for bamfile in *Human*.bam; do
    bam_fn_stem=$(basename "$bamfile" Aligned.toTranscriptome.out.bam) # extracts stem part of filename (removing extensions)
    echo "$bam_fn_stem"
    echo module load RSEM >> "${scripts_dir}RSEMParamScript_${bam_fn_stem}.sh"
    echo mkdir ${output_dir}${bam_fn_stem} >> "${scripts_dir}RSEMParamScript_${bam_fn_stem}.sh"
    echo rsem-calculate-expression --bam $bam_dir$bamfile $rsem_ref_path "${output_dir}${bam_fn_stem}/" >> "${scripts_dir}RSEMParamScript_${bam_fn_stem}.sh"
    
    chmod +x ${scripts_dir}RSEMParamScript_${bam_fn_stem}.sh
done
#######################################################################################################################

#generate list of all parallel commands to be run (i.e: parallel running of all scripts previously generated); DO NOT NEED "parallel" at beginning if you're not doing multiple scripts per node

cd $scripts_dir

for file in $(ls *.sh); do
  echo "$scripts_dir$file" >> RSEMParamCom.txt
done

mv RSEMParamCom.txt $output_path
