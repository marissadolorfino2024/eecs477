#!/bin/python

from blossom_utils import *
import time

# g = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2, 4], 4: [3, 5], 5: [4]}


times = []
for n in range(10, 1000, 100):
    starttime = time.perf_counter()
    matched = blossom_alg(g)
    endtime = time.perf_counter()
    times.append(endtime-starttime)

print(times)