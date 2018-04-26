import pandas as pd
import numpy as np

normal_qc = pd.read_csv("normal-query-concepts.tsv", header=0, sep="\t")
snippets = pd.read_csv("news-snippets.tsv", header=0, sep="\t")
concepts = normal_qc['concept'].unique()
num_concepts = len(concepts)
similarity_matrix_concept = np.zeros((num_concepts, num_concepts), dtype=np.float16)


