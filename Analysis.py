import pandas as pd
import numpy as np


concept_sim = pd.read_csv("similarity-matrix-concept.tsv", header=0, sep="\t")
query_sim = pd.read_csv("similarity-matrix-query.tsv", header=0, sep="\t")

q_2016 = query_sim[query_sim['year'] == 2016]
q_2017 = query_sim[query_sim['year'] == 2017]
num_q = query_sim['query'].count()
c_2016 = concept_sim[concept_sim['year'] == 2016]
c_2017 = concept_sim[concept_sim['year'] == 2017]
num_c = concept_sim['concept'].count()

dif_q = np.zeros((num_q, num_q), dtype=np.float16)
dif_c = np.zeros((num_c, num_c), dtype=np.float16)

concepts = concept_sim['concept'].unique()
queries = query_sim['query'].unique()

for each_a in range(num_q):
    for each_b in range(num_q):
        print(query_sim[query_sim['query'] == queries[each_a]][query_sim['year'] == 2017][queries[each_b]])
        # dif_q[each_a][each_b] = query_sim[query_sim['query'] == queries[each_a]][query_sim['year'] == 2017][queries[each_b]] - query_sim[query_sim['query'] == queries[each_a]][query_sim['year'] == 2016][queries[each_b]]