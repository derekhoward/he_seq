# He et al sequencing

## DATA
### RNASeq reads
Raw data for for SRA accession # SRP065273 was downloaded from https://sra-explorer.info/
A total of 273 files were downloaded from human (102), chimpanzee (72) and macaque (99) datasets.

## Running STAR
### Creating a genome index
This step needs to be run only once for all samples using the same genome. 
These indices can take a large amount of space, so we will dedicate a directory for it on the shared lab space
(the arg for --genomeDir is the path where the genome index is stored)

- Fasta files (*.fa) are the genome reference assemblies
- Reference genome annotations are in *.gtf or .gff format. These are recommended to use to aid in better assigning reads to genes (improves alignment process).

STAR   --runMode genomeGenerate \
       --runThreadN 12 \
       --genomeDir /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/USE_THIS_genomeDir/ \
       --genomeFastaFiles /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/Raw/Homo_sapiens.GRCh38.dna.primary_assembly.fa \ 
       --sjdbGTFfile /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/Raw/Homo_sapiens.GRCh38.103.gtf


### Alignment process for multiple samples for downstream quantification with RSEM
Test out alignment process for a single sample first. This will give you an idea of the resources required and time to complete a single sample.

Example command used for STAR alignment for downstream RSEM (for single sample)
```
STAR --genomeDir /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/USE_THIS_genomeDir/ \
     --sjdbGTFfile /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/Raw/Homo_sapiens.GRCh38.103.gtf \
     --readFilesIn /genome/scratch/Neuroinformatics/dhoward/he_et_al/SRR2815952_RNA-Seq_of_Human_PFC_section_DS1-Human1-S1.fastq.gz \
     --quantMode TranscriptomeSAM \
     --outSAMtype None \
     --readFilesCommand zcat
```

To perform alignment for all samples, use the star_pipe.sh script as below
```
./star_pipe.sh /path/to/fastq_files/ /outputpath/ false /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/USE_THIS_genomeDir/ /external/rprshnas01/netdata_kcni/stlab/Genomic_references/Ensembl/Human/Release_103/Raw/Homo_sapiens.GRCh38.103.gtf
```

## Running RSEM
### Example to run all samples
run RSEM on output results from previous to lab folder
./rsem_pipe.sh /external/rprshnas01/netdata_kcni/stlab/he_human_processed/ /.../STAR_results/coord_bams/ /nethome/kcni/dhoward/rsem_reference/

### Creating counts matrix
To aggregate the counts from samples into a single counts matrix we use CLI scripts

```
module load PYTHON/3.6

python RSEM_counts_matrix.py /path/to/RSEM_results/ ./results/output_path.csv

python ensg_to_genesymbol.py ./results/output_path.csv ENSG_to_gene_name.tsv ./results/output_converted_genesymbols.csv
```