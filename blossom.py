#!/bin/python

from blossom_utils import *
import time

# g = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}

# matched = blossom_alg(g)
# print(matched)

times = []
for n in range(10, 15):
    starttime = time.perf_counter()
    g = generate_graph_with_odd_cycles(n, n_odd_cycles=n-8, cycle_length_range1 = 3, cycle_length_range2 = n-7)
    matched = blossom_alg(g)
    endtime = time.perf_counter()
    times.append(endtime-starttime)
print(times)