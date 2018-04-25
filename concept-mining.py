import pandas as pd

snippets = pd.read_csv("news-snippets.tsv", header=0, sep="\t")
print(snippets)