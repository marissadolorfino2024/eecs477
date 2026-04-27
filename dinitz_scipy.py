from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_flow

# naive graph reprsentation to csr matrix 
def graph_to_csr(g_naive, n):

    row_ind = []
    col_ind = []
    data = []
    
    for v in range(n):
        if v in g_naive:
            for u, cap in g_naive[v].items():
                row_ind.append(v)
                col_ind.append(u)
                data.append(cap)
    
    return csr_matrix((data, (row_ind, col_ind)), shape=(n, n))

# default maximum flow is dinitz alg
def scipy_dinitz(g, source, target):
    maximum_flow(g, source, target)
