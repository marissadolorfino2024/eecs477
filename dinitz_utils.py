#!/bin/python

import math 
import numpy as np
import heapq
import random
           
def get_allpaths(gf, source, target, path=None, all_paths=None, visited=None):
    if path is None:
        path = []
    if all_paths is None:
        all_paths = []
    if visited is None:
        visited = set()
    
    # add source vertex to path
    path = path + [source]
    visited.add(source)
    
    # save the path if we have reached the target
    if source == target:
        all_paths.append(path)
        return all_paths
    
    # if source is not in the graph, return
    if source not in gf:
        return all_paths
    
    # explore all neighbors of source
    for neighbor in gf[source]: 
        # only explore if not already visited to avoid cycles
        if neighbor not in visited and gf[source][neighbor] > 0:
            get_allpaths(gf, neighbor, target, path, all_paths, visited.copy())
    
    return all_paths

# dijkstra's algorithm for single source shortest path
# all edge weights here are 
def dijkstras(gf):
    V = len(list(gf.keys()))
    pq = []
    dist = {}
    
    dist[0] = 0
    heapq.heappush(pq, (0, 0))
    
    while pq:
        d, v = heapq.heappop(pq)
        
        if d > dist[v]:
            continue
        
        adj_v = list(gf[v].keys())
        for u in adj_v:
            # ONLY consider edges with positive capacity!
            if gf[v][u] <= 0:
                continue
                
            w = 1
            if u not in dist:
                dist[u] = float('inf')
                
            if dist[v] + w < dist[u]:
                dist[u] = dist[v] + w
                heapq.heappush(pq, (dist[u], u))
    
    # Handle case where sink is unreachable
    if V-1 not in dist:
        return float('inf')
        
    result = dist[V-1]
    # print(f'shortest path length from s to t: {result}')
    return result

def get_minpaths(gf, all_paths):
    # find min s-t path length
    mindist = dijkstras(gf)
    
    min_paths = []
    for p in all_paths:
        if len(p) - 1 == mindist: # ignore the target node in counting length of paths
            min_paths.append(p)
    
    # print(f'the current min paths: {min_paths}')
    return min_paths

def get_gprime(gf, min_paths):
    gprime = {}
    
    V = len(list(gf.keys()))
    
    for p in min_paths:
        for i in range(len(p)-1):
            v = p[i]
            vnext = p[i+1]
            if v not in list(gprime.keys()):
                gprime[v] = {vnext: gf[v][vnext]}
            else:
                gprime[v][vnext] = gf[v][vnext]
    
    # add the target vertex to the gprime dict
    gprime[V-1] = {}
        
    return gprime

def update_flow(gprime, p, currentflow):
    # get min capacity for this path
    mincap = math.inf
    for i in range(len(p)-1):
        v = p[i]
        v_next = p[i+1]
        if v in gprime and v_next in gprime[v]:
            mincap = min(gprime[v][v_next], mincap)
        else:
            return gprime, currentflow  # if not, then this edge doesn't have cap
    
    if mincap == 0: # no min path
        return gprime, currentflow
    
    currentflow += mincap
    
    # update forward and reverse edges based on mincap
    for i in range(len(p)-1):
        v = p[i]
        v_next = p[i+1]
        
        # reduce the forward capacity
        gprime[v][v_next] -= mincap
        
        # increase reverse capacity in gprime
        if v_next not in gprime:
            gprime[v_next] = {}
        if v not in gprime[v_next]:
            gprime[v_next][v] = mincap
        else:
            gprime[v_next][v] += mincap
    
    return gprime, currentflow

def dinitz_alg(gf):
    V = len(list(gf.keys()))
    currentflow = 0
    
    while True:
        # Check if sink is reachable from source using BFS/Dijkstra
        try:
            mindist = dijkstras(gf)
        except KeyError:  # If sink not reachable
            break
            
        # print(f'current gf: {gf}')
        
        all_paths = get_allpaths(gf, 0, V-1)
        
        # print(f'current allpaths: {all_paths}')
        
        # If no paths at all, we're done
        if len(all_paths) == 0:
            break
            
        min_paths = get_minpaths(gf, all_paths)
        
        gprime = get_gprime(gf, min_paths)
        
        # Find blocking flow in G'
        while True:
            all_paths_gprime = get_allpaths(gprime, 0, V-1)
            if len(all_paths_gprime) == 0:
                break
            gprime, currentflow = update_flow(gprime, all_paths_gprime[0], currentflow)
        
        # Update gf with G' contents
        for v in gprime:
            if v not in gf:
                gf[v] = {}
            for u, cap in gprime[v].items():
                gf[v][u] = cap
    
    # print(currentflow)
    return currentflow
            
# n = number of vertices, denisty = prob of edge between vertices
def generate_random_flow_network(n: int, density = 0.3, max_capacity = 100, ensure_connectivity = True):
    graph = {i: {} for i in range(n)}
    
    # add random forward edges, no self loops
    for u in range(n - 1):  # sink has no outgoing edges
        for v in range(u + 1, n): # avoid self-loops and backward edges
            if random.random() < density:
                if u < v:
                    graph[u][v] = random.randint(1, max_capacity)
    
    # nsure at least some paths exist
    if ensure_connectivity:
        # add a guaranteed path from source to sink
        path_length = random.randint(2, max(3, n // 4))
        path = [0]  # source
        available = list(range(1, n - 1))
        random.shuffle(available)
        path.extend(available[:path_length - 2])
        path.append(n - 1)  # sink
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            graph[u][v] = random.randint(max_capacity // 2, max_capacity)
    
    for _ in range(int(n * density * 2)):
        u = random.randint(0, n - 3)
        v = random.randint(u + 1, n - 1)
        if v not in graph[u]:
            graph[u][v] = random.randint(1, max_capacity)
    
    return graph
        
        
    
