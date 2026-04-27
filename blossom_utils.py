#!/bin/python

from collections import deque
import random

# for u,v that form a cycle, find the common base/blossom vertex
def find_commonbase(matched, base, parent, v, u):
    # mark vertices on path from v to beginning of blossom
    visited = set()
    current = v
    while True:
        # find what blossom the vertex belongs to, search from blossom if it belongs to one
        current = base[current]
        visited.add(current)
        if parent[current] is None:
            break
        current = parent[current]
    
    # go from u until we find the common vertex between paths u and v. this is the blossom base
    current = u
    while True:
        current = base[current]
        if current in visited:
            return current
        current = parent[current]

# add vertices in cycle to blossom 
def add_blossom_vertices(matched, base, blossom_vertices, parent, v, u, blossombase):
    # get path from v to blossomebase, set new base to blossom baase
    current = v
    # traversal in one direction
    while base[current] != blossombase:
        # add matched vertex and matched neighbor to blossom vertices
        blossom_vertices.add(base[current])
        blossom_vertices.add(base[matched[current]])
        parent[current] = u  
        u = matched[current]
        current = parent[u]
    
    # traversal in the other
    # get path from u to blossombase, set new base to blossom base
    current = u
    while base[current] != blossombase:
        blossom_vertices.add(base[current])
        blossom_vertices.add(base[matched[current]])
        parent[current] = v
        v = matched[current]
        current = parent[v]

# contract the blossom to a single vertex
def contract_blossom(g, matched, base, parent, v, u):
    blossombase = find_commonbase(matched, base, parent, v, u)
    blossom_vertices = set()
    
    # when blossom is found, add the blossom vertices
    add_blossom_vertices(matched, base, blossom_vertices, parent, v, u, blossombase)
    
    # all the blossom vertices have the same base, contracting to one vertex
    for vertex in blossom_vertices:
        base[vertex] = blossombase
    
    return blossom_vertices

# expand path in contracted graph to original graph
def expand_path(path, base, matched):
    if len(path) <= 1: # only one vertex
        return path
    
    expanded = [path[0]]
    i = 1
    while i < len(path) - 1:
        v = path[i]
        v_next = path[i+1]
        
        # if v and v_next connected in blossom graph but not in 
        # original, need to expand graph
        if base[v] == base[v_next]:
            # if in the same blossom, find path within blossom
            expanded.append(v)
            i += 1
        else:
            expanded.append(v)
            i += 1
    
    expanded.append(path[-1])
    return expanded

def bfs_augmentpath(start, g, matched):
    n = len(g)
    # Initialize arrays for BFS
    parent = {start: None}
    base = {u: u for u in g} # all vertices start as their own base
    visited = set([start])
    qu = deque([start])
    
    while qu:
        v = qu.popleft()
        
        for u in g[v]:
            # if in same blossom, skip and don't go backwards
            if base[v] == base[u] or (v in matched and matched[v] == u):
                continue
            
            # found a blossom (odd cycle)
            if u == start or (u in matched and matched[u] in visited):
                # Set parent before contracting if not already set
                if u not in parent:
                    parent[u] = v
                blossom_vertices = contract_blossom(g, matched, base, parent, v, u)
                # add blossom vertices if not visited yet
                for vertex in blossom_vertices:
                    if vertex not in visited:
                        visited.add(vertex)
                        qu.append(vertex)
            
            elif u not in visited:
                # regular BFS
                visited.add(u)
                parent[u] = v
                
                if u not in matched:
                    # found augmenting path
                    path = []
                    current = u
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    return path[::-1]
                else:
                    # if not augmenting path, continue BFS
                    w = matched[u]
                    visited.add(w)
                    parent[w] = u
                    qu.append(w)
    
    return None

# swith edges in augmented path to increase M by 1
def switch_apath(g, apath, matched, exposed):
    for i in range(len(apath) - 1):
        if i % 2 == 0:  # even indices are exposed, add to matching
            u, v = apath[i], apath[i + 1]
            matched[u] = v
            matched[v] = u
            exposed.discard(u)
            exposed.discard(v)
        else:  # odd indices are matched, switch to exposed
            u, v = apath[i], apath[i + 1]
            if u in matched and matched[u] == v:
                del matched[u]
                del matched[v]
                exposed.add(u)
                exposed.add(v)

# fine augmented paths and switch edges
def improve_matching(g, matched, exposed):
    exposed_list = list(exposed)
    for v in exposed_list:
        if v not in exposed:
            continue
        
        apath = bfs_augmentpath(v, g, matched)
        if apath is not None:
            switch_apath(g, apath, matched, exposed)
            return True
    
    return False

# run blossoms until no more augmented paths
def blossom_alg(g):
    matched = {}
    exposed = set(g.keys())
    
    while improve_matching(g, matched, exposed):
        pass
    
    return list(matched.keys())

# for generating random graphs
def generate_graph_with_odd_cycles(n_vertices: int = 10, n_odd_cycles: int = 2, cycle_length_range: Tuple[int, int] = (3, 5), extra_edge_probability: float = 0.1)
    graph = {i: [] for i in range(n_vertices)}
    available_vertices = list(range(n_vertices))
    random.shuffle(available_vertices)
    
    # insert odd cycles
    for _ in range(n_odd_cycles):
        cycle_length = random.randrange(
            cycle_length_range[0], cycle_length_range[1] + 1, 2
        )
        
        if len(available_vertices) < cycle_length:
            break
        
        # take vertices for this cycle
        cycle_vertices = available_vertices[:cycle_length]
        available_vertices = available_vertices[cycle_length:]
        
        # create the odd cycle
        for i in range(cycle_length):
            v1 = cycle_vertices[i]
            v2 = cycle_vertices[(i + 1) % cycle_length]
            if v2 not in graph[v1]:
                graph[v1].append(v2)
            if v1 not in graph[v2]:
                graph[v2].append(v1)
    
    # add random extra edges to create more complex structure
    for i in range(n_vertices):
        for j in range(i + 1, n_vertices):
            if random.random() < extra_edge_probability and j not in graph[i]:
                graph[i].append(j)
                graph[j].append(i)
    
    return graph