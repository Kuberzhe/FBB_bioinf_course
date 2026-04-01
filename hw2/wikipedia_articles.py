#!/Users/macbook/anaconda3/bin/python

import argparse
import requests
import random
from bs4 import BeautifulSoup
from collections import defaultdict as dd
import json

# get args
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url')     # start url
parser.add_argument('-d', '--depth')   # depth of search
parser.add_argument('-mlp', '--max_links_per_page')   # depth of search
args = parser.parse_args()

random.seed(42)

headers = {'User-Agent': 'EducationalScraper/1.0 (contact: Liza Fomenko)'}
base_url = 'https://en.wikipedia.org'

def find_next_links(url):
    r = requests.get(f'{base_url}{url}', headers = headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    content = soup.find('div', id = 'bodyContent')
    if content:
        return [link['href'] for link in content.find_all('a', href = re.compile(r"^(/wiki/)((?!:).)*$"))]
    return []

from collections import deque
def BFS(v_start, max_depth = 5):  
    queue = deque() 
    queue.append([v_start, 0]) 
    seen = {v_start}
    output = {}
    while not len(queue) == 0:  
        v, curr_d = queue.popleft()
        if curr_d < max_depth:
            links = find_next_links(v)
            if int(args.max_links_per_page) > 0 and len(links) > int(args.max_links_per_page):
                links = random.sample(links, int(args.max_links_per_page))
            output[v.split("/")[-1]] = [link.split("/")[-1] for link in links]
            for m_v in links: 
                if m_v not in seen: 
                    queue.append([m_v, curr_d + 1])  
                    seen.add(m_v)  
    return output

if base_url in args.url:
    start_article = args.url.split(base_url)[1]
else:
    start_article = args.url

output = BFS(start_article, int(args.depth))   

with open(f'{start_article.split("/")[-1]}.json', 'w') as out:
    json.dump(output, out, indent=4)
