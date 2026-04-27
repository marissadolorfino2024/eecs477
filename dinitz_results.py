#!/bin/python

import matplotlib.pyplot as plt
import ast

with open('time_dinitz_10to30.out', 'r') as f:
    content = f.read().strip()
    dinitz_naive = ast.literal_eval(content)
    
with open('dinitz_opt_10to1000.out', 'r') as f:
    content = f.read().strip()
    dinitz_opt = ast.literal_eval(content)
    
with open('dinitz_scipy_10to1000.out', 'r') as f:
    content = f.read().strip()
    dinitz_scipy = ast.literal_eval(content)
    
r1 = list(range(10,30))
r2 = list(range(10,1000))

plt.figure(figsize=(12, 6))
plt.plot(r1, dinitz_naive, label=f'naive implementation', alpha=0.7, linewidth=1, color='magenta')
plt.legend()
plt.savefig('dinitz_naive.png')

plt.cla()

plt.figure(figsize=(12, 6))
plt.plot(r2, dinitz_opt, label=f'optimized implementation', alpha=0.7, linewidth=1, color='lightpink')
plt.plot(r2, dinitz_scipy, label=f'scipy implementation', alpha=0.7, linewidth=1, color='lightskyblue')
plt.legend()
plt.savefig('dinitz_opt_scipy.png')
