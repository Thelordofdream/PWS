import pandas as pd
import spacy
import os

nlp = spacy.load('en')
# print(nlp.Defaults.stop_words)
nlp.Defaults.stop_words.add("'s")
candidate_keys = {}
keys = {}
threshold = 0.1
snippets = pd.read_csv("news-snippets.tsv", header=0, sep="\t")

if os.path.exists("query-concepts.tsv"):
    os.remove("query-concepts.tsv")
with open("query-concepts.tsv", "a", encoding="utf-8") as f:
    f.write("query\tconcept\t2016\t2017\n")
    for query in ["apple", "apple computer", "apple mac", "iPhone", "iPod", "apple juice", "juice", "orange juice"]:
        keys[query] = {}
        candidate_keys = {}
        sub_snippet = snippets[snippets['query'] == query]
        num = sub_snippet["query"].count()

        for index, row in sub_snippet.iterrows():
            title = nlp(row["title"])
            abstract = nlp(row["abstract"])
            for each in title.noun_chunks:
                if not str(each).lower() in nlp.Defaults.stop_words:
                    candidate_keys[str(each)] = {2016: 0, 2017: 0}
            for each in abstract.noun_chunks:
                if not str(each).lower() in nlp.Defaults.stop_words:
                    candidate_keys[str(each)] = {2016: 0, 2017: 0}

        candidate = candidate_keys.keys()
        for index, row in sub_snippet.iterrows():
            title = [str(i) for i in nlp(row["title"])]
            abstract = [str(i) for i in nlp(row["abstract"])]
            for each in candidate:
                if each in title or each in abstract:
                    candidate_keys[each][row["year"]] += 1

        for each in candidate:
            support = 1.0 * (candidate_keys[each][2016] + candidate_keys[each][2017]) / num * len(each.split(" "))
            if support >= threshold:
                # print(support, candidate_keys[each])
                keys[query][each] = candidate_keys[each]
        print(keys[query])
        for each in keys[query].keys():
            f.write(query + "\t" + each + "\t" + str(keys[query][each][2016]) + "\t" + str(keys[query][each][2017]) + "\n")
