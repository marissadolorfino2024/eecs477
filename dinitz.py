#!/bin/python

from dinitz_utils import *
import time

# naive implementation of a graph: dictionary with n-1 keys for vertices, where v has value that is itself a dictionary of vs neighbors, u where g[v][u] = cap(v,u)
# s and t vertices have key 0 and n-1
# g_naive = {0: {1: 10, 2: 10}, 1: {2: 2, 3: 4, 4: 8}, 2: {4: 9}, 3: {5: 10}, 4: {3: 6, 5: 10}, 5: {}}

# g_naive2 = {0: {1: 16, 2: 13}, 1: {2: 10, 3: 12}, 2: {1: 4, 4: 14}, 3: {2: 9, 5: 20}, 4: {3: 7, 5: 4}, 5: {}}

# times = []
# for n in range(10, 50):
#     grandom = generate_random_flow_network(n=n)
#     starttime = time.perf_counter()
#     dinitz_alg(grandom)
#     endtime = time.perf_counter()
#     times.append(endtime-starttime)
# print(times)

# from dinitz_opt_utils import *
# import time

# times = []
# for n in range(10, 1000):
#     grandom = generate_random_flow_network(n=n)
#     # convert graph format to adj list and cap arrauy
#     adj, cap, n = convert_graph_to_list_format(grandom)
#     starttime = time.perf_counter()
#     dinitz_list_alg(adj, cap, n)
#     endtime = time.perf_counter()
#     times.append(endtime-starttime)
# print(times)

from dinitz_scipy import *
import time

times = []
for n in range(10, 1000):
    grandom = generate_random_flow_network(n=n)
    # convert graph format to adj list and cap arrauy
    csr = graph_to_csr(grandom, n)
    starttime = time.perf_counter()
    targ = n-1
    scipy_dinitz(csr, 0, n-1)
    endtime = time.perf_counter()
    times.append(endtime-starttime)
print(times)
