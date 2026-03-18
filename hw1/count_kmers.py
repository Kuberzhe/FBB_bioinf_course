#!/usr/bin/python3

import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--fa", type=str, required=True, help="Input fasta file")
parser.add_argument("--kmer_size", "-k", type=str, required=True, help="kmer size")
parser.add_argument("--out", type=str, required=True, help="Output file name")
args = parser.parse_args()

k = int(args.kmer_size)
kmers = {}
cur_seq = ''


with open(f'{args.fa}', 'r') as input:
    for line in input:
        if line.startswith('>'):
            if cur_seq != '':
                kmers[cur_seq_name] = {}
                for i in range(len(cur_seq) - k):
                    if cur_seq[i: i+k] not in kmers[cur_seq_name]:
                        kmers[cur_seq_name][cur_seq[i: i+k]] = 1
                    else:
                        kmers[cur_seq_name][cur_seq[i: i + k]] += 1
            cur_seq_name = line.strip()[1:]
            cur_seq = ''
        else:
            line = line.strip()
            cur_seq += line

kmers[cur_seq_name] = {}

for i in range(len(cur_seq) - k):
    if cur_seq[i: i + k] not in kmers[cur_seq_name]:
        kmers[cur_seq_name][cur_seq[i: i + k]] = 1
    else:
        kmers[cur_seq_name][cur_seq[i: i + k]] += 1

with open(f"{args.out}.json", "w") as out:
    json.dump(kmers, out, indent=3)
