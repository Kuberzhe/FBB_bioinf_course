#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--seq", type=str, required=True, help="Returns reverse complementary sequence")
args = parser.parse_args()

nucl = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
gc_count = 0
seq = args.seq.upper()
res = ''
for ch in seq[::-1]:
    res += nucl[ch]
    if (ch == 'G') or (ch == 'C'):
        gc_count += 1

print(f'Reverse complement is {res}')
print(f'GC content is {round(gc_count / len(res), 3)}')
