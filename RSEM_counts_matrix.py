import argparse
import sys
from pathlib import Path
import pandas as pd


def process_rsem_results(input_path, output_path):
    rsem_result_dirs = list(input_path.glob('*'))
    print(f'There are {len(rsem_result_dirs)} sample directories to be processed...')
    sample_dfs = [] 
    for i, result in enumerate(rsem_result_dirs):
        sample_counts = result.glob('.genes.results')
        counts_path = list(sample_counts)

        if len(counts_path) > 0:
            #print(f'SampleID: {result.stem}, {counts_path}')
            try:
                df = pd.read_csv(counts_path[0], sep='\t')
                df = df.loc[:, ['gene_id', 'expected_count']]
                df.rename(columns={"expected_count": result.stem}, inplace=True)
                sample_dfs.append(df.set_index('gene_id'))
            except pd.io.common.EmptyDataError:
                print(f'EmptyDataError for file: {counts_path[0]}')
        else:
            print(result.stem)
            
    concat = pd.concat(sample_dfs, axis=1)
    print(f'Writing to {output_path}')
    concat.to_csv(output_path) 
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract the expected gene counts for all samples and output a .csv')

    parser.add_argument('input_path', metavar='input_path', type=str,
                        help='the path to directory of RSEM results')

    parser.add_argument('output_path', metavar='output_path', type=str,
                        help='the path to output the results')

    # Execute the parse_args() method
    args = parser.parse_args()
    input_path = Path(args.input_path)
    output_path = Path(args.output_path)
    
    if not input_path.is_dir():
        print('The path specified does not exist')
        sys.exit()

    
    process_rsem_results(input_path, output_path)
