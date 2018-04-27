import pandas as pd
import numpy as np
import os

normal_qc = pd.read_csv("normal-query-concepts.tsv", header=0, sep="\t")
queries = normal_qc['query'].unique()
num_queries = len(queries)
similarity_matrix_query = np.zeros((2, num_queries, num_queries), dtype=np.float16)

for year in [2016, 2017]:
    for each_a in range(num_queries):
        a = normal_qc[normal_qc['query'] == queries[each_a]]
        sum_a = a[str(year)].sum()
        for each_b in range(each_a + 1, num_queries):
            b = normal_qc[normal_qc['query'] == queries[each_b]]
            sum_b = b[str(year)].sum()
            ab = 0
            for index, row in a.iterrows():
                same = b[b['concept'] == row['concept']]
                if same["query"].count() > 0:
                    ab += row[str(year)] + same[str(year)].sum()
            similarity_matrix_query[year -2016][each_a][each_b] = ab / (sum_a + sum_b)

if os.path.exists("similarity-matrix-query.tsv"):
    os.remove("similarity-matrix-query.tsv")
with open("similarity-matrix-query.tsv", "a", encoding="utf-8") as f:
    header = "query\tyear\t"
    for i in range(num_queries - 1):
        header += queries[i] + "\t"
    header += queries[-1] + "\n"
    f.write(header)
    for a in range(2):
        sim = similarity_matrix_query[a]
        for b in range(num_queries):
            row = queries[b] + "\t" + str(a + 2016) + "\t"
            for c in range(num_queries - 1):
                row += str(sim[b][c]) + "\t"
            row += str(sim[b][-1]) + "\n"
            f.write(row)