import numpy as np
import polyeder
import kjetil_det
from kjetils_graph import get_verbose_graph_description

poly = polyeder.Polyeder()
poly.project_facets()
"""
adjacency_mat, vertices = get_verbose_graph_description(0)
print(vertices)
print(adjacency_mat)
"""
#spanning_trees = kjetil_det.find_all_spanning_trees(adjacency_mat, vertices, do_print=0)
def zero_one_name_rule(adjacency):
    rule=""
    for row in adjacency:
        for num in row:
            rule += str(num)
    return rule

all_adjacency_matrices = kjetil_det.test_kjetil()
variants_found = 0
#print(len(all_adjacency_matrices))
found_zeros = 0
empty_what = 0
n_printed = 0
for span_with_nodes_removed in all_adjacency_matrices:
    if len(span_with_nodes_removed)!=0:
        empty_what += 1
        for spanning_matrix in span_with_nodes_removed:
            print_coordinates = poly.compute_print_coordinates(spanning_matrix)

            nodes = poly.get_tree_nodes(spanning_matrix)
            name = zero_one_name_rule(spanning_matrix)
            poly.print_tree(nodes, print_coordinates,
                            colors=('b', 'b', 'y', 'y', 'c', 'c', 'r'),
                                    save_fig=True, show_fig=False,
                                    name_base="Images/vertices",
                                    name_rule=name)
            n_printed += 1
            print(n_printed, " prints produced.", end="\r")

#print(found_zeros, variants_found, empty_what)