#!/bin/python

import math
from collections import deque
import random

# convert naive dictionary graphs to lists
def convert_graph_to_list_format(gf): 
    n = len(gf)
    
    adj = [[] for _ in range(n)]
    cap = [{} for _ in range(n)]
    
    for v in range(n):
        for u, capacity in gf[v].items():
            if capacity > 0:
                adj[v].append(u)
                cap[v][u] = capacity
    
    return adj, cap, n

# level graph using BFS
def bfs_level_graph(adj, cap, source, n):
    level = [-1] * n  
    level[source] = 0
    qu = deque([source])
    
    # for each node, check if neighbor does not have a level yet. if not, level is level + 1 
    while qu:
        v = qu.popleft()
        for u in adj[v]:
            if cap[v][u] > 0 and level[u] == -1:
                level[u] = level[v] + 1
                qu.append(u)
    
    return level

def dinitz_dfs_list(adj, cap, level, ptr, v, target, flow):
    # dfs on level graph for finding blocking flwos
    if v == target:
        return flow
    
    # pointer of current vertex instead
    while ptr[v] < len(adj[v]):
        u = adj[v][ptr[v]]
        
        # if more capacity and level is next level up (wrt v to nieghbor)
        if cap[v].get(u, 0) > 0 and level[v] + 1 == level[u]:
            # push flow
            pushed = dinitz_dfs_list(adj, cap, level, ptr, u, target, min(flow, cap[v][u]))
            
            # if flow was actually pushed
            if pushed > 0:
                # updated forward by decreasing cap
                cap[v][u] -= pushed
                
                # make backwards edge if not exist
                if v not in adj[u]:
                    adj[u].append(v)
                    cap[u][v] = 0
                
                # update backward edge by increasing cap
                cap[u][v] = cap[u].get(v, 0) + pushed
                
                return pushed
        
        ptr[v] += 1
    
    return 0

def dinitz_list_alg(adj, cap, n):
    source, target = 0, n - 1
    currentflow = 0
    
    # while still paths from source to targer
    while True:
        # construct level graph
        level = bfs_level_graph(adj, cap, source, n)
        
        # if there is no path from source to target, exit
        if level[target] == -1:
            break
        
        # find block flor with dfs
        # use list instead of dict for pointers, pre allocate 
        ptr = [0] * n  
        
        while True:
            pushed = dinitz_dfs_list(adj, cap, level, ptr, source, target, float('inf'))
            if pushed == 0:
                break
            currentflow += pushed
    
    return currentflow