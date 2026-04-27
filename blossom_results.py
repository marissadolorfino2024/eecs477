#!/bin/python

import matplotlib.pyplot as plt
import ast

with open('time-blossom_10to13.out', 'r') as f:
    content = f.read().strip()
    blossom_naive = ast.literal_eval(content)
    
r = list(range(10,13))

plt.figure(figsize=(12, 6))
plt.plot(r, blossom_naive, label=f'naive implementation', alpha=0.7, linewidth=1, color='magenta')
plt.legend()
plt.savefig('blossom_naive.png')