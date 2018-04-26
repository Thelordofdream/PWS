import pandas as pd
import os

query_concept = pd.read_csv("query-concepts.tsv", header=0, sep="\t")
qc = {}

# Convert to dictionary and handle the same concepts with uper or lower and single or plural
if os.path.exists("normal-query-concepts.tsv"):
    os.remove("normal-query-concepts.tsv")
with open("normal-query-concepts.tsv", "a", encoding="utf-8") as f:
    f.write("query\tconcept\t2016\t2017\n")
    for query in ["apple", "apple computer", "apple mac", "iPhone", "iPod", "apple juice", "juice", "orange juice"]:
        qc[query] = {}
        keys = []
        subset = query_concept[query_concept['query'] == query]
        for index, row in subset.iterrows():
            qc[query][row['concept']] = {2016: row['2016'], 2017: row['2017']}
            keys.append(row['concept'])
        unique1 = []
        unique2 = []
        for each in keys:
            if each.lower() in unique1:
                unique1.index(each.lower())
                qc[query][unique2[unique1.index(each.lower())]][2016] += qc[query][each][2016]
                qc[query][unique2[unique1.index(each.lower())]][2017] += qc[query][each][2017]
                qc[query].pop(each)
            elif each.lower() + "s" in unique1:
                qc[query][each][2016] += qc[query][unique2[unique1.index(each.lower() + "s")]][2016]
                qc[query][each][2017] += qc[query][unique2[unique1.index(each.lower() + "s")]][2017]
                qc[query].pop(unique2[unique1.index(each.lower() + "s")])
            elif each.lower() + "es" in unique1:
                qc[query][each][2016] += qc[query][unique2[unique1.index(each.lower() + "es")]][2016]
                qc[query][each][2017] += qc[query][unique2[unique1.index(each.lower() + "es")]][2017]
                qc[query].pop(unique2[unique1.index(each.lower() + "es")])
            elif each.lower()[:-1] in unique1 and each.lower()[-1] == "s":
                qc[query][unique2[unique1.index(each.lower()[:-1])]][2016] += qc[query][each][2016]
                qc[query][unique2[unique1.index(each.lower()[:-1])]][2017] += qc[query][each][2017]
                qc[query].pop(each)
            elif each.lower()[:-2] in unique1 and each.lower()[-2:] == "es":
                qc[query][unique2[unique1.index(each.lower()[:-2])]][2016] += qc[query][each][2016]
                qc[query][unique2[unique1.index(each.lower()[:-2])]][2017] += qc[query][each][2017]
                qc[query].pop(each)
            else:
                unique1.append(each.lower())
                unique2.append(each)
        for each in qc[query].keys():
            f.write(query + "\t" + each + "\t" + str(qc[query][each][2016]) + "\t" + str(qc[query][each][2017]) + "\n")