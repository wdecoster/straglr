# Straglr - *S*hort-*t*andem *r*epe*a*t *g*enotyping using *l*ong *r*eads

This is a modified version of the original Straglr tool which focuses on genotyping of clinical tandem repeat(TR) expansions from targeted or whole genome long-read alignments.

## Installation
Straglr is implemented in Python 3.8 and has been tested in Linux environment.

Straglr depends on [Tandem Repeat Finder(TRF)](https://tandem.bu.edu/trf/trf.html) for identifying TRs and [blastn](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/) for iotif matching. (TRF and blastn executables must be in `$PATH`). Other Python dependencies are listed in `requirements.txt`.

The file `environment.yaml` can by used by conda to create an environment with all dependencies installed:
```
mamba env create --name straglr --file=environment.yaml
conda activate straglr
pip install git+https://github.com/bcgsc/straglr.git@v1.3.0#egg=straglr
```
## Quick start
```
conda activate straglr
straglr-genotype --loci repeat-annotation/hg38/clinical_repeats.bed --sample <sample name> --vcf <output vcf> --sex <male/female> input.bam reference.fasta
```

## Input
Long read alignments sorted by genomic coordindates in BAM format against the reference genome. Suggested aligner: [Minimap2](https://github.com/lh3/minimap2) **-- Please use the option `-Y` to enable soft-clipping so that read sequences can be assessed directly from the BAM file.** 

## Usage
```
usage: straglr-genotype [-h] --vcf VCF [--tsv TSV] [--threads THREADS] --sample SAMPLE [--sex {male,female}] --loci LOCI [--min_support MIN_SUPPORT] [--min_cluster_size MIN_CLUSTER_SIZE] [--genotype_in_size] [--max_cov MAX_COV] [--trf_args Match Mismatch Delta PM PI Minscore MaxPeriod] [--working_dir WORKING_DIR]
                        [--tmpdir TMPDIR] [--debug] [--version]
                        bam genome_fasta

positional arguments:
  bam                   bam file
  genome_fasta          genome_fasta

options:
  -h, --help            show this help message and exit
  --vcf VCF, -v VCF     Path to output VCF file.
  --tsv TSV             Output per read stats to TSV file.
  --threads THREADS, -t THREADS
                        Number of processes
  --sample SAMPLE       Sample name to use in output VCF file
  --sex {male,female}   Sex of sample
  --loci LOCI           bed file of loci for genotyping
  --min_support MIN_SUPPORT
                        minimum number of supporting reads for detecting expansion. Default:2
  --min_cluster_size MIN_CLUSTER_SIZE
                        minimum number of supporting reads for allele clustering. Default:2
  --genotype_in_size    report genotype in size instead of copy numbers
  --max_cov MAX_COV     maximum allowed coverage for ins inspection. Default:1000
  --trf_args Match Mismatch Delta PM PI Minscore MaxPeriod
                        tandem repeat finder arguments. Default:2 5 5 80 10 10 500
  --working_dir WORKING_DIR
                        working directory. Default:current directory
  --tmpdir TMPDIR       directory to use for generating tmp files instead of system TEMP
  --debug               debug mode i.e. keep trf output
  --version             show program's version number and exit	
```

## Output
1. VCF file
2. TSV file - detailed output one support read per line 
	* chrom - chromosome name
	* start - start coordinate of locus
	* end - end coordinate of locus
	* repeat_unit - repeat motif
	* genotype - copy numbers (default) or sizes (`--genotype_in_size`) of each allele detected for given locus, separate by semi-colon(";") if multiple alleles detected, with number of support reads in bracket following each allele copy number/size. An example of a heterozygyous allele in size: `990.8(10);30.9(10)`
	* read - name of support read
	* copy_number - number of copies of repeat in allele
	* size - size of allele
	* read_start - start position of repeat in support read
	* allele - allele that support read is assigned to

## Contact
[Readman Chiu](mailto:rchiu@bcgsc.ca)

## Citation
Chiu R, Rajan-Babu IS, Friedman JM, Birol I. Straglr: discovering and genotyping tandem repeat expansions using whole genome long-read sequences. *Genome Biol* 22, 224 (2021). https://doi.org/10.1186/s13059-021-02447-3

