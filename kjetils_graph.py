import numpy as np

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