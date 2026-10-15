import scipy.io
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from pfn_config import cfg  # file paths come from CONFIG.txt at the repo root

if __name__ == "__main__":
    roi_gene_mat = scipy.io.loadmat(cfg["AHBA_ROI_GENE_MAT"])
    gene_dictionary = {"gene": []}
    for array in roi_gene_mat['probeInformation']['GeneSymbol']:
        for gene_arrays in array:
            for gene_array in gene_arrays:
                gene_dictionary['gene'].append(gene_array[0][0])

    gene_df = pd.DataFrame.from_dict(gene_dictionary)
    gene_df.to_csv(cfg["GENE_SYMBOL_CSV"], index=False)
    print("Job Done!")