import pandas as pd
import numpy as np
import os

normal_qc = pd.read_csv("normal-query-concepts.tsv", header=0, sep="\t")
snippets = pd.read_csv("news-snippets.tsv", header=0, sep="\t")
concepts = normal_qc['concept'].unique()
num_concepts = len(concepts)
similarity_matrix_concept = np.zeros((2, num_concepts, num_concepts), dtype=np.float16)
alpha = 0.4

for each_a in range(num_concepts):
    for each_b in range(each_a + 1, num_concepts):
        for year in [2016, 2017]:
            Fa_title = 0
            Fb_title = 0
            Dif_Fab_title = 0
            Fa_abstract = 0
            Fb_abstract = 0
            Dif_Fab_abstract = 0
            Fa_other = 0
            Fb_other = 0
            Dif_Fab_other = 0

            sub_snippets = snippets[snippets['year'] == year]
            num_doc = sub_snippets['query'].count()
            for index, row in sub_snippets.iterrows():
                title = row['title'].lower()
                abstract = row['abstract'].lower()
                Joint = [0, 0, 0, 0]

                if concepts[each_a].lower() in title:
                    Fa_title += 1
                    Joint[0] = 1
                if concepts[each_b].lower() in title:
                    Fb_title += 1
                    Joint[1] = 1
                if sum(Joint[:2]) == 2:
                    Dif_Fab_title += 1

                if concepts[each_a].lower() in abstract:
                    Fa_abstract += 1
                    Joint[2] = 1
                if concepts[each_b].lower() in abstract:
                    Fb_abstract += 1
                    Joint[3] = 1
                if sum(Joint[-2:]) == 2:
                    Dif_Fab_abstract += 1

                if Joint[0] + Joint[2] > 0:
                    Fa_other += 1
                if Joint[1] + Joint[3] > 0:
                    Fb_other += 1
                if sum(Joint) == 2 and not Joint[0] == Joint[1]:
                    Dif_Fab_other += 1
            if Dif_Fab_title > 0:
                similarity_title = alpha * np.log(
                    1.0 * num_doc * Dif_Fab_title / Fa_title / Fb_title) / np.log(1.0 * num_doc)
            else:
                similarity_title = 0

            if Dif_Fab_title > 0:
                similarity_abstract = alpha * np.log(
                    1.0 * num_doc * Dif_Fab_abstract / Fa_abstract / Fb_abstract) / np.log(
                    1.0 * num_doc)
            else:
                similarity_abstract = 0

            if Dif_Fab_other > 0:
                similarity_other = alpha * np.log(
                    1.0 * num_doc * Dif_Fab_other / Fa_other / Fb_other) / np.log(
                    1.0 * num_doc)
            else:
                similarity_other = 0
            # print(concepts[each_a], concepts[each_b], similarity_title, similarity_abstract)
            if similarity_abstract + similarity_title + similarity_other >= 0:
                similarity_matrix_concept[year - 2016][each_a][each_b] = similarity_abstract + similarity_title + similarity_other
            else:
                similarity_matrix_concept[year - 2016][each_a][each_b] = 0

if os.path.exists("similarity-matrix-concept.tsv"):
    os.remove("similarity-matrix-concept.tsv")
with open("similarity-matrix-concept.tsv", "a", encoding="utf-8") as f:
    header = "concept\tyear\t"
    for i in range(num_concepts - 1):
        header += concepts[i] + "\t"
    header += concepts[-1] + "\n"
    f.write(header)
    for a in range(2):
        sim = similarity_matrix_concept[a]
        for b in range(num_concepts):
            row = concepts[b] + "\t" + str(a + 2016) + "\t"
            for c in range(num_concepts - 1):
                row += str(sim[b][c]) + "\t"
            row += str(sim[b][-1]) + "\n"
            f.write(row)