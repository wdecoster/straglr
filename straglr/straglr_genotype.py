#!/usr/bin/env python
import argparse
import sys
import tempfile
import os

from straglr.ins import INSFinder
from straglr.tre import TREFinder
from straglr.version import __version__


def parse_args():
    trf_args_meta = ('Match', 'Mismatch', 'Delta', 'PM', 'PI', 'Minscore', 'MaxPeriod')
    parser = argparse.ArgumentParser()
    parser.add_argument("bam", type=str, help="bam file")
    parser.add_argument("genome_fasta", type=str, help="genome_fasta")
    parser.add_argument("--vcf", "-v", type=str, required=True, help="Path to output VCF file.")
    parser.add_argument("--tsv", type=str, required=False, help="Output per read stats to TSV file.")
    #parser.add_argument("--min_ins_size", type=int, default=100, help="minimum insertion size. Default:100")
    #parser.add_argument("--exclude", type=str, help="bed file to exclude regions")
    #parser.add_argument("--regions", type=str, help="bed file for scanning only specific regions")
    parser.add_argument("--threads", "-t", type=int, help="Number of processes", default=1)
    #parser.add_argument("--chroms", type=str, nargs="+", help="chromosomes")
    parser.add_argument("--sample", type=str, required=True, help="Sample name to use in output VCF file")
    parser.add_argument("--sex", type=str, default='female', choices=['male', 'female'], help="Sex of sample")
    parser.add_argument("--loci", type=str, required=True,  help="bed file of loci for genotyping")
    parser.add_argument("--min_support", type=int, help="minimum number of supporting reads for detecting expansion. Default:2", default=5)
    parser.add_argument("--min_cluster_size", type=int, help="minimum number of supporting reads for allele clustering. Default:2", default=5)
    parser.add_argument("--genotype_in_size", action="store_true", help="report genotype in size instead of copy numbers")
    #parser.add_argument("--max_str_len", type=int, help="maximum STR length. Default:50", default=50)
    #parser.add_argument("--min_str_len", type=int, help="minimum STR length. Default:2", default=2)
    #parser.add_argument("--max_num_clusters", type=int, help="maximum number of clusters to try. Default:2", default=2)
    parser.add_argument("--max_cov", type=int, help="maximum allowed coverage for ins inspection. Default:1000", default=1000)
    parser.add_argument("--trf_args", type=int, nargs=7, help="tandem repeat finder arguments. Default:2 5 5 80 10 10 500", metavar=trf_args_meta, default=[2,5,5,80,10,10,500])
    parser.add_argument("--working_dir", type=str, help="working directory. Default:current directory")
    parser.add_argument("--tmpdir", type=str, help="directory to use for generating tmp files instead of system TEMP")
    parser.add_argument("--debug", action='store_true', help="debug mode i.e. keep trf output")
    parser.add_argument("--version", action='version', version=__version__)
    args = parser.parse_args()
    return args

def main():
    args = parse_args()

    if args.tmpdir:
        tempfile.tempdir = args.tmpdir

    if args.working_dir:
        if not os.path.exists(args.working_dir):
            os.makedirs(args.working_dir)
        elif not os.path.isdir(args.working_dir):
            sys.exit('Error: working directory given "{}" is not a directory'.format(args.working_dir))
        os.chdir(args.working_dir)

    min_cluster_size = args.min_cluster_size if args.min_cluster_size < args.min_support else args.min_support

    tre_finder = TREFinder(args.bam,
                           args.genome_fasta,
                           sex=args.sex,
                           nprocs=args.threads,
                           reads_fasta=None,
                           max_str_len=50,
                           min_str_len=2,
                           min_support=args.min_support,
                           min_cluster_size=min_cluster_size,
                           genotype_in_size=args.genotype_in_size,
                           max_num_clusters=2, # This is now defined by "sex" + "chromosome"
                           trf_args=' '.join(map(str, args.trf_args + ['-d', '-h'])),
                           debug=args.debug)

    variants = []

    tre_finder.min_cluster_size = args.min_cluster_size
    variants = tre_finder.genotype(args.loci)

    # output both bed and tsv
    #tre_finder.output_bed(variants, '{}.bed'.format(args.out_prefix))
    tre_finder.output_vcf(variants, args.vcf, args.sample, args.loci, args.genome_fasta)
    if args.tsv:
        tre_finder.output_tsv(variants, args.tsv, cmd=' '.join(sys.argv))

if __name__ == '__main__':
    main()
