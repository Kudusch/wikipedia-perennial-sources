#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv
import json
from itertools import chain
import re

def get_links_from_infobox(u):
    r = requests.get(u)
    html_doc = r.text
    html_soup = BeautifulSoup(html_doc, 'html.parser')
    
    try:
        html_table = html_soup.find("table", {"class": "infobox"})
        info_links = [a.get("href") for a in html_table.find_all("a") if a.get("href").startswith("http")]
        info_links = [u for u in info_links if not u.startswith("https://www.worldcat.org")]
        info_links = [u for u in info_links if not u.startswith("https://www.wikidata.org/wiki/Q9531#P856")]
    except:
        info_links = []
    
    try:
        offical_websites = list(chain(*[li.find_all("span", {"class":"official-website"}) for li in html_soup.find_all("li") if len(li.find_all("span", {"class":"official-website"})) > 0]))
        offical_websites = [a.get("href") for a in list(chain(*[span.find_all("a") for span in offical_websites]))]
    except:
        offical_websites = []

    links = list(chain(*[info_links, offical_websites]))
    links = [re.sub(r"^https?:\/\/", "", l) for l in links]
    links = [re.sub(r"\/$", "", l) for l in links]
    links = [l.lower() for l in links]
    links = list(set(links))
    return(links)

r = requests.get("https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources")
html_doc = r.text
html_soup = BeautifulSoup(html_doc, 'html.parser')
html_table = html_soup.find("table", {"class": "perennial-sources"})

all_sources = []
for row in html_table.find_all("tr"):
    source = {}
    cells = row.find_all("td")
    try:
        source["name"] = cells[0].find_all("a")[0].get_text()
        print("Getting info for {}".format(source["name"]))
        source["status"] =  json.dumps([a.get('title') for a in cells[1].find_all("a")])
        source["info"] = cells[4].get_text()
        source["wiki_url"] = "https://en.wikipedia.org" + cells[0].find_all("a")[0].get("href")
        source["urls"] = json.dumps(get_links_from_infobox(source["wiki_url"]))
        all_sources.append(source)
    except:
        pass

with open("perennial-sources.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "status", "wiki_url", "urls", "info"])
    for s in all_sources:
        writer.writerow([
            s["name"], 
            s["status"], 
            s["wiki_url"], 
            s["urls"],
            s["info"],
    ])