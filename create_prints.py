import numpy as np
import polyeder
import kjetil_det
from kjetils_graph import get_verbose_graph_description
import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon
import matplotlib.colors as mcolors


poly = polyeder.Polyeder()
poly.project_facets()
"""
adjacency_mat, vertices = get_verbose_graph_description(0)
print(vertices)
print(adjacency_mat)
"""
def animate_prints(prints, nodes):
    images = []
    fig, ax = plt.subplots()
    plt.axis('off')
    n_prints = len(prints)
    ax_lim = 500
    xlim = [-ax_lim, ax_lim]
    ylim = xlim
    def poly_animate(i):
    #for print in prints:
        ax.clear()
        for i_poly in nodes[i]: #prints[i]:
            polygon = prints[i][i_poly]
            p = Polygon(polygon[:,:2], facecolor = 'b',
                        alpha=.2, edgecolor='k')
            ax.add_patch(p)

        ax.axis('equal')
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        ax.set_axis_off()
        #im = ax.set_animated(True)
        #images.append([im])

    ani = animation.FuncAnimation(fig, poly_animate,
                                    frames=n_prints,
                                    interval=10,
                                    repeat=False)
                                    #blit=True,
                                    #repeat_delay=1000)
    ani.save('kjetil_art.gif', writer='imagemagick')
    plt.show()

#spanning_trees = kjetil_det.find_all_spanning_trees(adjacency_mat, vertices, do_print=0)
def zero_one_name_rule(adjacency, full_adjacency):
    rule=""
    for i_row, row in enumerate(adjacency):
        for i_col in range(i_row + 1, len(row)):
            if full_adjacency[i_row, i_col]:
                rule += str(row[i_col])
    return rule

do_animate = True #False #
do_plot = True #False
if do_animate:
    all_print_coordinates = []
    all_nodes = []

all_adjacency_matrices, full_adj = kjetil_det.test_kjetil()
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
            if do_animate:
                all_print_coordinates.append(copy.copy(print_coordinates))
                all_nodes.append(nodes)
            name = zero_one_name_rule(spanning_matrix, full_adj)
            #name = str(int(name, 2))
            if do_plot:
                poly.print_tree(nodes, print_coordinates,
                            colors=('lightsteelblue', 'purple', 'navy', 'blue', 'mediumslateblue', 'darkorchid', 'thistle'), # 'y', 'y', 'c', 'c', 'r'),
                                    save_fig=True, show_fig=False,
                                    name_base="Images/vertices",
                                    name_rule=name + "_" + str(n_printed + 1), fig_title="Image " + str(n_printed + 1) + ", Nodes: " + name)
            n_printed += 1
            print(n_printed, " prints produced.", end="\r")

if  do_animate:
    animate_prints(all_print_coordinates, all_nodes)


#print(found_zeros, variants_found, empty_what)