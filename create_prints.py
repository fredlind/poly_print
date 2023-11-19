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
def animate_prints(prints, nodes, facecolors='b', alpha=.2, edgecolor='k'):
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
            if hasattr(facecolors, "__len__"):
                if len(facecolors) == 1: facecolor = facecolors
                else:
                    print(facecolors, i_poly)
                    facecolor = facecolors[i_poly]
            else: facecolor = facecolors

            p = Polygon(polygon[:,:2], facecolor = facecolor,
                        alpha=alpha, edgecolor=edgecolor)
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

from settings import *

if do_animate:
    all_print_coordinates = []
    all_nodes = []

all_adjacency_matrices, full_adj = kjetil_det.test_kjetil()
variants_found = 0
#print(len(all_adjacency_matrices))
found_zeros = 0
empty_what = 0
n_printed = 0

n_prints_per_page = n_rows * n_cols
#n_to_print = len(all_adjacency_matrices)
#print(n_to_print)
page_number = 0
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
                n_printed_on_page = n_printed % n_prints_per_page
                #print(n_printed, n_prints_per_page, n_printed_on_page)
                if n_printed_on_page == 0:
                    fig, axes = plt.subplots(n_rows, n_cols)
                
                col_num = n_printed_on_page % n_cols
                row_num = n_printed_on_page // n_cols
                text_zeros = '0000'
                n_zeros = len(text_zeros)
                text_num_short = str(n_printed +1)
                n_digits = len(text_num_short)
                text_num_long = text_zeros[:n_zeros - n_digits] + text_num_short
                fig_title= text_num_long#"Image " + str(n_printed + 1) + ", Nodes: " + name
                poly.print_tree(nodes, print_coordinates,
                                colors=colors,
                                save_fig=True, show_fig=show_fig,
                                name_base="Images/vertices",
                                name_rule=name + "_" + str(n_printed + 1),
                                fig_title=fig_title,
                                fig=fig, ax=axes[row_num, col_num],
                                text_position=text_position)
            
                n_printed += 1
                n_printed_on_page = n_printed % n_prints_per_page
                if n_printed_on_page == 0:
                    page_number += 1
                    fig.suptitle("Page " + str(page_number))
                    start_string = str(n_printed - n_prints_per_page + 1)
                    n_start_string = len(start_string)
                    long_start_string = text_zeros[:n_zeros - n_start_string] + start_string
                    end_string = str(n_printed)
                    n_end_string =len(end_string)
                    long_end_string = text_zeros[:n_zeros - n_end_string] + end_string
                    fig.savefig("MultiImages/" + "fig_" + long_start_string + "to" + long_end_string + "_page" + str(page_number) + "_rc" + str(n_rows) + "x" + str(n_cols) + "." + filetype)
                    plt.close()
                elif n_printed == N_TO_PRINT:
                    for col in range(col_num + 1, n_cols):
                        axes[row_num, col].set_axis_off()
                    for row in range(row_num + 1, n_rows):
                        for col in range(n_cols):
                            axes[row, col].set_axis_off()
                    page_number += 1
                    fig.suptitle("Page " + str(page_number))
                    start_string = str(n_printed - n_printed_on_page + 1)
                    n_start_string = len(start_string)
                    long_start_string = text_zeros[:n_zeros - n_start_string] + start_string
                    end_string = str(n_printed)
                    n_end_string =len(end_string)
                    long_end_string = text_zeros [:n_zeros - n_end_string] + end_string
                    fig.savefig("MultiImages/" + "fig_" + long_start_string + "to" + long_end_string + "_page" + str(page_number) + "_rc" + str(n_rows) + "x" + str(n_cols) + "." + filetype)
                    plt.close()

            
            if verbose:
                print(n_printed, " prints produced.", end="\r")
print(n_printed, " in total printed.")

if  do_animate:
    animate_prints(all_print_coordinates, all_nodes)


#print(found_zeros, variants_found, empty_what)