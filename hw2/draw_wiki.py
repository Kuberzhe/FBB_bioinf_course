#!/usr/bin/python3

import json
import networkx as nx
from matplotlib import pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', required=True)     # start url
parser.add_argument('-o', '--output', required=True)     # start url
args = parser.parse_args()

with open(args.input) as file:
    data = json.load(file)

graph = nx.DiGraph()
for node, links in data.items():
    for link in links:
        graph.add_edge(node, link)

plt.figure(figsize=(15,15))
position = nx.spring_layout(graph, k=0.15)
nx.draw(graph, position, node_size=50, node_color='red', edge_color='black', linewidths=0.3, font_size = 10)

plt.savefig(f"{args.output}.png", dpi=150)
