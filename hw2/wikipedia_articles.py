#!/usr/bin/python3
import json
import random
import argparse
import requests
from bs4 import BeautifulSoup
from queue import Queue
#from collections import defaultdict as dd

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True)     # start article url
parser.add_argument('-d', '--max_depth', required=True)   # max depth for bfs
parser.add_argument('-l', '--max_links_per_page', default=100)  
args = parser.parse_args()
base = 'https://en.wikipedia.org'
#headers = {'User-Agent': 'EducationalScraper/1.0 (contact: Liza Fomenko)'}


def search(start, max_depth = 3):  
    seen = {start}
    out = {}
    q = Queue() 
    q.append([start, 0]) 
    while not len(q) == 0:  
        page, cur_depth = q.popleft()
        if cur_depth < max_depth:
            cur_links = find_next_links(page)
            if len(links) > int(args.max_links_per_page):
                links = random.sample(links, int(args.max_links_per_page))
            out[v.split("/")[-1]] = [kega.split("/")[-1] for kega in cur_links]
            for link in links: 
                if link not in seen: 
                    q.append([link, cur_depth + 1])  
                    seen.add(link)  
    return out

def find_next_links(url):
    req = requests.get(f'{base}{url}')#, headers = headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    article = soup.find('div', id = 'bodyContent')
    if len(article) != 0:
        return [link['href'] for link in article.find_all('a', href = re.compile(r"^(/wiki/)((?!:).)*$"))]
    else:
        return []



start_article = args.url.split(base)[-1]
#if base in args.url:
#    start_article = args.url.split(base_url)[1]
#else:
#    start_article = args.url

res = search(start_article, int(args.depth))   

with open(f'{start_article.split("/")[-1]}.json', 'w') as out:
    json.dump(res, out, indent=4)
