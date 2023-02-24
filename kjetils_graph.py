import numpy as np

def adjacency_from_edges(facet_edges, n):
    adjacency_matrix = np.zeros((n, n), dtype=int)
    for i_node, edges in enumerate(facet_edges):
        for edge in edges:
            for j_node in range(i_node + 1, n):
                if edge in facet_edges[j_node]:
                    adjacency_matrix[i_node, j_node] = 1
                    adjacency_matrix[j_node, i_node] = 1

    return adjacency_matrix

def adjacency_to_vertices(adjacency):
    n = len(adjacency)
    vertices = []
    for i in range(n):
        for j in range(i + 1, n):
            if adjacency[i, j]: vertices.append([i, j])
    
    return np.array(vertices)


def get_graph_description():
    adjacency_matrix =- np.array( [[0,-1,-1,0,-1,0,0],
                                   [-1,0,-1,-1,-1,0,-1],
                                   [-1,-1,0,-1,-1,-1, 0],
                                   [0,-1,-1,0,0,-1,-1],
                                   [-1,-1,-1,0,0,-1,-1],
                                   [0,0,-1,-1,-1,0,-1],
                                   [0,-1,0,-1,-1,-1,0]])
    
    vertices = np.array([[0, 1],
                         [0, 2],
                         [0, 4],
                         [1, 2],
                         [1, 3],
                         [1, 4],
                         [1, 6],
                         [2, 3],
                         [2, 4],
                         [2, 5],
                         [3, 5],
                         [3, 6],
                         [4, 5],
                         [4, 6],
                         [5, 6]])

    return adjacency_matrix, vertices

def get_verbose_graph_description(verbosity_level=1):
    facet_edges = [[0, 2, 1],
                            [0, 9, 10, 11, 3],
                            [2, 3, 4, 5, 6],
                            [1, 6, 7, 8, 9],
                            [12, 14, 7, 5],
                            [8, 14, 13, 10],
                            [11, 13, 12, 4]
                           ]
  
    facet_vertices = [[0, 1, 2],
                              [0, 5, 6, 7, 1],
                              [2, 1, 7, 8, 3],
                              [0, 2, 3, 4, 5],
                              [3, 8, 9, 4],
                              [5, 4, 9, 6],
                              [9, 8, 7, 6]]
        
    coordinates3d = [[0, 1, 2],
                              [1, 0, 2],
                              [0, 0, 1],
                              [0, 0, 0],
                              [0, 2, 0],
                              [0, 2, 2],
                              [3, 2, 2],
                              [3, 0, 2],
                              [3, 0, 0],
                              [3, 2, 0]]
        
    edge_vertices = [[0, 1],
                              [1, 2],
                              [2, 0],
                              [1, 7],
                              [7, 8],
                              [8, 3],
                              [3, 2],
                              [3, 4],
                              [4, 5],
                              [5, 0],
                              [5, 6],
                              [6, 7],
                              [8, 9],
                              [9, 6],
                              [4, 9]]

    adjacency_matrix = adjacency_from_edges(facet_edges, 7)
    vertices = adjacency_to_vertices(adjacency_matrix)

    if verbosity_level:
        return facet_edges, facet_vertices, coordinates3d, edge_vertices, adjacency_matrix, vertices
    else:
        return adjacency_matrix, vertices

