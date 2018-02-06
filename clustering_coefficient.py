def clustering_coeff(node_count, edge_count):
    max_edge_count = (node_count * (node_count - 1)) / 2.0
    coeff = 0.0
    if max_edge_count != 0:
        coef = edge_count / float(max_edge_count)
    else:
        coef = 0.0
    return coeff