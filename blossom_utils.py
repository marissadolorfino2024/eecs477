#!/bin/python

from collections import deque
import random

def find_commonbase(base, parent, v, u):
    visited = set()
    
    # mark path from v to root 
    current = v
    visited.add(current)
    while current in parent and parent[current] is not None:
        # go to matched neigbors parent
        current = parent[current]
        visited.add(current)
        if current in parent and parent[current] is not None:
            current = parent[current]
            visited.add(current)
        else:
            break
    
    # find first common bse from u
    current = u
    while current not in visited:
        if current in parent and parent[current] is not None:
            current = parent[current]
            if current in visited:
                break
            if current in parent and parent[current] is not None:
                current = parent[current]
        else:
            # if no common ancestor, return u 
            return u
    
    return current

def contract_blossom(g, matched, base, parent, v, u):
    blossombase = find_commonbase(base, parent, v, u)
    blossom_vertices = set()
    
    # mark vertices in the blossom
    def mark_path(start):
        current = start
        while current in base and base[current] != base[blossombase]:
            blossom_vertices.add(current)
            # always follow matched edge if exists
            if current in matched:
                v_next = matched[current]
                if v_next in base and base[v_next] != base[blossombase]:
                    blossom_vertices.add(v_next)
                    # set parent for matched neighbor 
                    if v_next not in parent or parent[v_next] is None:
                        parent[v_next] = current
                    current = v_next
                    # move to parent of matched vertex 
                    if current in parent and parent[current] is not None:
                        current = parent[current]
                    else:
                        break
                else:
                    break
            else:
                break
        blossom_vertices.add(blossombase)
    
    mark_path(v)
    mark_path(u)
    blossom_vertices.add(base[blossombase]) # add the base vertex
    
    # set all vertices in blossom to have same base
    for vertex in blossom_vertices:
        base[vertex] = base[blossombase]
    
    return blossom_vertices

# find the actual path within a blossom
def reconstruct_path(end_vertex, parent):
    path = []
    current = end_vertex
    while current is not None:
        path.append(current)
        current = parent.get(current)
    return path[::-1]

# expand path through contracted blossoms
def expand_path(path, base, matched):
    if len(path) <= 1:
        return path
    
    expanded = []
    
    for i in range(len(path) - 1):
        v = path[i]
        v_next = path[i + 1]
        
        if i == 0:
            expanded.append(v)
        
        # if different bases in original graph, or matched in oroginal graph, add to expanded path
        # not in a blossom
        if base[v] != base[v_next]:
            expanded.append(v_next)
        else:
            # in same blossom, must expand
            # add all v in the original graph between v and v_next in the blossom
            # if nothing in between
            if v in matched and matched[v] == v_next:
                expanded.append(v_next)
            elif v_next in matched and matched[v_next] == v:
                expanded.append(v_next)
            else:
                # find alternating path in the blossom
                current = v
                while current != v_next:
                    if current in matched:
                        match_n = matched[current]
                        expanded.append(match_n)
                        current = match_n
                    else:
                        break
    
    return expanded

def bfs_augmentpath(start, g, matched):
    parent = {start: None}
    base = {u: u for u in g}
    visited = set([start])
    qu = deque([start])
    
    while qu:
        v = qu.popleft()
        
        for u in g[v]:
            # Skip if same blossom or matched edge
            if base[v] == base[u] or (v in matched and matched[v] == u):
                continue
            
            # Found a blossom (odd cycle) - u is already visited, different bases, 
            # and creates an odd-length alternating path
            if u in visited:
                # This is the correct blossom detection:
                # Need to make sure u is in the same alternating tree
                # and we're not creating an even cycle
                if u not in parent:
                    parent[u] = v
                
                # Contract the blossom
                blossom_vertices = contract_blossom(g, matched, base, parent, v, u)
                
                # Add newly discovered vertices to queue
                for vertex in blossom_vertices:
                    if vertex not in visited:
                        visited.add(vertex)
                        qu.append(vertex)
                # Don't break - continue processing
            
            elif u not in visited:
                visited.add(u)
                parent[u] = v
                
                if u not in matched:
                    # Found augmenting path
                    return reconstruct_path(u, parent)
                else:
                    # Follow matched edge
                    w = matched[u]
                    visited.add(w)
                    parent[w] = u
                    qu.append(w)
    
    return None

# switch edges in augmented path to increase M by 1
def switch_apath(g, apath, matched, exposed):
    # add even vertices and neighbor to match
    for i in range(0, len(apath) - 1, 2):
        u = apath[i]
        v = apath[i + 1]
        # add to matching if exposed
        matched[u] = v
        matched[v] = u
        exposed.discard(u)
        exposed.discard(v)
    
    # add odd vertices and neighbor to exposed
    for i in range(1, len(apath) - 1, 2):
        u = apath[i]
        v = apath[i + 1]
        # add to exposed if matched
        if u in matched and matched[u] == v:
            del matched[u]
            del matched[v]
            exposed.add(u)
            exposed.add(v)

# find augmented paths and switch edges
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
def generate_graph_with_odd_cycles(n_vertices: int = 10, n_odd_cycles: int = 2, cycle_length_range1 = 3, cycle_length_range2 = 5, extra_edge_probability: float = 0.1):
    graph = {i: [] for i in range(n_vertices)}
    available_vertices = list(range(n_vertices))
    random.shuffle(available_vertices)
    
    cycle_length_range = (cycle_length_range1, cycle_length_range2)
    
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