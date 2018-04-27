import pandas as pd
import numpy as np


concept_sim = pd.read_csv("similarity-matrix-concept.tsv", header=0, sep="\t")
query_sim = pd.read_csv("similarity-matrix-query.tsv", header=0, sep="\t")

q_2016 = query_sim[query_sim['year'] == 2016]
q_2017 = query_sim[query_sim['year'] == 2017]
c_2016 = concept_sim[concept_sim['year'] == 2016]
c_2017 = concept_sim[concept_sim['year'] == 2017]

concepts = concept_sim['concept'].unique()
queries = query_sim['query'].unique()

num_q = len(queries)
num_c = len(concepts)

dif_q = np.zeros((num_q, num_q), dtype=np.float16)
dif_c = np.zeros((num_c, num_c), dtype=np.float16)

for each_a in range(num_q):
    for each_b in range(each_a + 1, num_q):
        dif_q[each_a][each_b] = query_sim[(query_sim['query'] == queries[each_a]) & (query_sim['year'] == 2017)][queries[each_b]].sum() - query_sim[(query_sim['query'] == queries[each_a]) & (query_sim['year'] == 2016)][queries[each_b]].sum()

with open("similarity-query-changes.tsv", "a", encoding="utf-8") as f:
    header = "query\t"
    for i in range(num_q - 1):
        header += queries[i] + "\t"
    header += queries[-1] + "\n"
    f.write(header)
    for b in range(num_q):
        row = queries[b] + "\t"
        for c in range(num_q - 1):
            row += str(dif_q[b][c]) + "\t"
        row += str(dif_q[b][-1]) + "\n"
        f.write(row)

for each_a in range(num_c):
    for each_b in range(each_a + 1, num_c):
        dif_c[each_a][each_b] = concept_sim[(concept_sim['concept'] == concepts[each_a]) & (concept_sim['year'] == 2017)][concepts[each_b]].sum() - concept_sim[(concept_sim['concept'] == concepts[each_a]) & (concept_sim['year'] == 2016)][concepts[each_b]].sum()

with open("similarity-concept-changes.tsv", "a", encoding="utf-8") as f:
    header = "concept\t"
    for i in range(num_c - 1):
        header += concepts[i] + "\t"
    header += concepts[-1] + "\n"
    f.write(header)
    for b in range(num_c):
        row = concepts[b] + "\t"
        for c in range(num_c - 1):
            row += str(dif_c[b][c]) + "\t"
        row += str(dif_c[b][-1]) + "\n"
        f.write(row)