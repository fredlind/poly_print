import numpy as np
import copy
import sympy as symp
from itertools import combinations
import sys
from kjetils_graph import get_graph_description

def compute_connections(graph_mat):
    #Return the Laplacian matrix from the adjancy matrix
    laplacian_mat = - copy.copy(graph_mat)
    n_nodes = laplacian_mat.shape[0] 
    for i_node in range(n_nodes):
        laplacian_mat[i_node, i_node] = -np.sum(laplacian_mat[i_node])
    
    return laplacian_mat

def get_all_combinations_to_remove(nodes):
    n_nodes = len(nodes)
    comb_to_remove = list()
    for n_to_remove in range(n_nodes):
        comb_to_remove += list(combinations(nodes, n_to_remove))
    
    return comb_to_remove

def get_complement(subset, omega):
    return omega.difference(subset)

def get_sub_graph(super_graph, nodes_to_keep):
    n_nodes = len(nodes_to_keep)
    cols = list(nodes_to_keep)
    rows = np.array(list(nodes_to_keep)).reshape(n_nodes, 1)
    sub_graph = super_graph[rows, cols]
    return sub_graph

def test_graph_vertex_mapping(adjacency_matrix, vertices):
    #TODO: Move to unittest
    s = 0
    for vert in vertices:
        s += adjacency_matrix[vert[0], vert[1]]
    if s != len(adjacency_matrix):
        print('Vertices does not fit adjacency matrix')
    else:
        print('Warning: test not complete!')

    return s, len(adjacency_matrix)

def get_subgraph(graph, vertices, n_nodes):
    mat = np.zeros((n_nodes, n_nodes))

    for vert0 in graph:
        vert = vertices[vert0]
        mat[vert[0], vert[1]] = 1
        mat[vert[1], vert[0]] = 1

    return mat

def check_n_of_spanning_trees(adjacency_matrix):
    laplacian = compute_connections(adjacency_matrix)
    sub_det = int(np.round(np.linalg.det(laplacian[1:,1:])))

    return sub_det

def find_all_spanning_trees(adjacency_mat, vertices, do_print=0):
    n_trees = check_n_of_spanning_trees(adjacency_mat)
    n_nodes = len(adjacency_mat)
    spanning_tree_vertices = np.zeros((n_trees, n_nodes - 1), dtype=int)
    graphs = combinations(np.arange(len(vertices)), n_nodes - 1)

    s = 0
    n = 0
    for graph in graphs:
        n += 1
        mat = get_subgraph(graph, vertices, n_nodes)
        is_spanning_tree = check_n_of_spanning_trees(mat)    
        #print(is_spanning_tree)
        

        if is_spanning_tree:
            spanning_tree_vertices[s] = graph
            if do_print:
                print(graph)
        
        s += is_spanning_tree
        #if n==5: break

    return spanning_tree_vertices

def remove_nodes(super_adjacency, super_vertices, nodes_to_remove):
    #Input original adjacency matrix and the vertices and nodes to remove
    n_remove = len(nodes_to_remove)
    n_super = len(super_adjacency)

    sub_adjacency = np.delete(super_adjacency, nodes_to_remove, 0)
    sub_adjacency = np.delete(sub_adjacency, nodes_to_remove, 1)

    sub_to_super_node_mapping = [i for i in range(len(super_adjacency)) if i not in nodes_to_remove]
    super_to_sub_node_mapping = n_super * np.ones(n_super)
    
    for i_sub in range(len(sub_adjacency)):
        super_to_sub_node_mapping[sub_to_super_node_mapping[i_sub]] = i_sub
    
    sub_vertices = []
    sub_to_super_vertex_mapping = []
    for i_vert, vertex in enumerate(super_vertices):
        if vertex[0] in nodes_to_remove or vertex[1] in nodes_to_remove:
            continue
        else:
            sub_vertices.append(vertex) 
            sub_to_super_vertex_mapping.append(i_vert) 

    super_coordinates_sub_vertices = copy.copy(sub_vertices)
    for sub_vertex in sub_vertices:
        sub_vertex[0] = super_to_sub_node_mapping[sub_vertex[0]]
        sub_vertex[1] = super_to_sub_node_mapping[sub_vertex[1]]
    print(sub_vertices)
    print(sub_to_super_vertex_mapping)
    #RECOPMPUTE vertex VALUES IN sub_vertices to subvalues

    return sub_adjacency, sub_vertices, sub_to_super_node_mapping, super_to_sub_node_mapping, super_coordinates_sub_vertices

def expand_to_full_size(sub_adjacency, removed_nodes):
    sorted_nodes = np.sort(removed_nodes)
    full_adjacency = np.insert(sub_adjacency, sorted_nodes, 0, axis=0)
    full_adjacency = np.insert(full_adjacency, sorted_nodes, 0, axis=1)

    return full_adjacency

def compute_adjacency_from_vertices(vertex_numbers, vertices):
    n_nodes = len(vertex_numbers) + 1
    adjacency_mat = np.zeros((n_nodes, n_nodes), dtype=int)
    for vertex in vertex_numbers:
        adjacency_mat[vertices[vertex][0], vertices[vertex][1]] = 1
        adjacency_mat[vertices[vertex][1], vertices[vertex][0]] = 1

    return adjacency_mat

#def full_size_vertices(sub_to_super_node_mapping, sub_vertices):

adjacency_mat, vertices = get_graph_description()

spanning_trees = find_all_spanning_trees(adjacency_mat, vertices, do_print=0)

print(spanning_trees)
print(len(spanning_trees))

comb_to_remove = get_all_combinations_to_remove(np.arange(len(adjacency_mat)))

#print(comb_to_remove)
n_combinations_found = 0

sub_adjacency, sub_vertices, sub_to_super_node_mapping, super_to_sub_node_mapping, super_coord_sub_vertices = remove_nodes(adjacency_mat, vertices, comb_to_remove[1])

sub_spanning_trees = find_all_spanning_trees(sub_adjacency, sub_vertices, do_print=0)
# This is just the nodes. Must transform to matrix. 
sub_spanning_adjacencies = []
for spanning_tree in sub_spanning_trees:
    sub_spanning_adjacencies.append(compute_adjacency_from_vertices(spanning_tree, sub_vertices))

#print(len(sub_spanning_trees))

for i_tree in range(1, len(comb_to_remove)):
    full_size_spanning = expand_to_full_size(sub_spanning_adjacencies[i_tree], comb_to_remove[i_tree])
    #print(full_size_spanning)

sys.exit()
omega = {0, 1, 2, 3, 4, 5, 6}
for nodes_to_remove in comb_to_remove:
    nodes_to_keep = get_complement(nodes_to_remove, omega)
    subgraph = get_sub_graph(adjacency_mat, nodes_to_keep)
    laplacian = compute_connections(subgraph)
    matrix=symp.Matrix(laplacian)
    n_spanning_trees = matrix.adjugate()[0,0]
    print("Nodes:")
    print(nodes_to_keep)
    print("No combinations:")
    print(n_spanning_trees)
    n_combinations_found += n_spanning_trees

print("Total combinations: ", n_combinations_found)

#print(subgraph)
#print(graph_mat)

#mat_mat = mat_mat[:-1]
#mat_mat = mat_mat[:,:-1]
#print(mat_mat)
#mat_det=np.linalg.det(mat_mat)
#print(mat_det)
