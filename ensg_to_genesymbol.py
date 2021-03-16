import argparse
import sys
from pathlib import Path
import pandas as pd


def convert_gene_ids_to_symbols(input_path, conversion_table, output_path):
    print(f'Reading in counts matrix from {input_path}')
    counts_matrix = pd.read_csv(input_path)
    print(f'Reading gene conversion table from {conversion_table}')
    convert_genes = pd.read_table(conversion_table, sep='\t', header=None, names=['gene_id', 'gene_symbol'])
    counts_matrix = counts_matrix.merge(convert_genes, on=['gene_id']).set_index('gene_symbol').drop('gene_id', axis=1)
    print(f'Merged counts matrix with gene symbols info and dropped ENSG id, writing output to {output_path}')
    counts_matrix.to_csv(output_path) 
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract the expected gene counts for all samples and output a .csv')

    parser.add_argument('input_path', metavar='input_path', type=str,
                        help='the path to csv with row indices as ENSG')
    
    parser.add_argument('conversion_table', metavar='conversion_table', type=str,
                        help='path to .tsv file with ensembl gene id to gene_symbol')

    parser.add_argument('output_path', metavar='output_path', type=str,
                        help='the path to output the results csv')

    # Execute the parse_args() method
    args = parser.parse_args()
    
    input_path = Path(args.input_path)
    conversion_table = Path(args.conversion_table)
    output_path = Path(args.output_path)
    
    if not input_path.is_file():
        print('The input path specified does not exist')
        sys.exit()
    if not conversion_table.is_file():
        print('The conversion table path specified does not exist')
        sys.exit()

    
    convert_gene_ids_to_symbols(input_path, conversion_table, output_path)

