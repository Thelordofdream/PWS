import os
import re
from bs4 import BeautifulSoup

if os.path.exists("news-snippets.tsv"):
    os.remove("news-snippets.tsv")
with open("news-snippets.tsv", "a", encoding="utf-8") as f:
    f.write("query\tyear\tsource\ttitle\turl\tabstract\n")
    for query in ["apple", "apple computer", "apple mac", "iPhone", "iPod", "apple juice", "juice", "orange juice"]:
        for year in [2016, 2017]:
            for page in range(1, 6):
                file = open('news-snippets/%s-%d-%d.html' % (query, year, page), encoding='utf-8')
                content = file.read()
                soup = BeautifulSoup(content, "lxml")
                try:
                    titles = [re.findall(r'<a class="l lLrAF" .*?>(.*?)</a>', str(each))[0].replace("<em>", "").replace("</em>", "").replace(" ...", "").replace("\"", "").replace(u"\u201c", "").replace(u"\u201d", "").replace(u"\u2013", " ").replace(u"\u2014", " ").replace(u"\u20ac", "").replace(u"\u200b", "").replace(u"\u2026", " ").replace(u"\u2318", "") for each in soup.find_all("h3", class_="r dO0Ag")]
                    abstracts = [re.findall(r'st">(.*?)</div>', str(each))[0].replace("<em>", "").replace("</em>", "").replace("\xa0...", "").replace("\"", "").replace(u"\u201c", "").replace(u"\u201d", "").replace(u"\u2013", " ").replace(u"\u2014", " ").replace(u"\u20ac", "").replace(u"\u200b", "").replace(u"\u2026", " ").replace(u"\u2318", "") for each in soup.find_all("div", class_="st")]
                    medias = [re.findall(r'<span class=".*?xQ82C e8fRJf">(.*?)</span>', str(each))[0] for each in soup.find_all("div", class_="slp")]
                    urls = [re.findall(r'<a class="l lLrAF" href="(.*?)"', str(each))[0] for each in
                              soup.find_all("h3", class_="r dO0Ag")]
                    if len(titles) == len(abstracts) and len(titles) == len(medias) and len(titles) == len(urls):
                        for i in range(len(titles)):
                            print(titles[i] + "\t" + abstracts[i])
                            f.write(query + "\t" + str(year) + "\t" + medias[i] + "\t" + titles[i] + "\t" + urls[i] + "\t" + abstracts[i] + "\n")
                    else:
                        print("Alignment Error!")
                except IndexError:
                    print("Not English!")
