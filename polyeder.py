import numpy as np
from scipy.spatial.transform import Rotation
from geometry import rotation_matrix_from_vectors as rot_mat
from copy import copy
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Polygon

class Polyeder():
    def __init__(self):
        self.facet_edges = [[0, 2, 1],
                            [0, 9, 10, 11, 3],
                            [2, 3, 4, 5, 6],
                            [1, 6, 7, 8, 9],
                            [12, 14, 7, 5],
                            [8, 14, 13, 10],
                            [11, 13, 12, 4]
                           ]
  
        self.facet_vertices = [[0, 1, 2],
                              [0, 5, 6, 7, 1],
                              [2, 1, 7, 8, 3],
                              [0, 2, 3, 4, 5],
                              [3, 8, 9, 4],
                              [5, 4, 9, 6],
                              [9, 8, 7, 6]]
        
        self.coordinates3d = [[102.92540117,  49.87062921,  34.09690239],
                              [ 64.57867716,  47.90858236,   0.0        ],
                              [102.58552237,  29.84274338,   0.0        ],
                              [103.46859197,   3.92782623,   0.0        ],
                              [105.91734603,  -0.22939487,  76.94551506],
                              [104.15211756,  51.30732998,  76.64277521],
                              [-26.72391577,  49.42631516, 105.5635993 ],
                              [ -1.69096739,  46.47077443,   0.0        ],
                              [  0.0        ,   0.0,           0.0        ],
                              [-24.75404573,  -6.78833432, 105.88401249]
                              ]
        """[[0, 1, 2],
                              [1, 0, 2],
                              [0, 0, 1],
                              [0, 0, 0],
                              [0, 2, 0],
                              [0, 2, 2],
                              [3, 2, 2],
                              [3, 0, 2],
                              [3, 0, 0],
                              [3, 2, 0]]
        """
        self.edge_vertices = [[0, 1],
                              [2, 0],
                              [1, 2],
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

        self.projected_coordinates = []

    def project(self, coordinates):
        #print("first rotation:")
        coordinates -= coordinates[0]
        l = np.linalg.norm(coordinates[1])
        target = [l, 0, 0]
        #print("Target and old coord: ", target, coordinates[1])
        r_mat = rot_mat(coordinates[1], target)#Rotation.align_vectors(target, [coordinates[2]]) #TODO: change for something nicer
        coordinates = np.matmul(r_mat, coordinates.transpose()).transpose()
        ##print("Transformed coordinates:")
        #print(coordinates)
        #print("Second rotation:")
        vect_to_rotate = copy(coordinates[2])
        vect_to_rotate[0] = 0 
        l = np.linalg.norm(vect_to_rotate)
        target = [0, l, 0]

        #target *= l / np.linalg.norm(target)
        #target[1] = l #np.sign(target[1]) * target[1]
        #print('target: ', target, vect_to_rotate)
        r_mat = rot_mat(vect_to_rotate, target, x=0)
        coordinates = np.matmul(r_mat, coordinates.transpose()).transpose()
    
        #print("Transformed coordinates:")
        #print(coordinates)
        #print("-------------------")
        return coordinates

    def project_facets(self):
        for facet_vertices in self.facet_vertices:
            projected_coordinates = []
            for vertex in facet_vertices:
                projected_coordinates.append(self.coordinates3d[vertex])
            
            self.projected_coordinates.append(self.project(np.array(projected_coordinates)))
        """
        for proj_coords in self.projected_coordinates:
            print(proj_coords)
        """

    def align_facet_edges(self, fixed_facet, facet, common_edge, fixed_facet_coords):
        #self.print_coordinates = []
        vertex1, vertex2 = self.edge_vertices[common_edge]
        #print(fixed_facet, facet, common_edge,vertex1, vertex2)
        fixed_facet_point1 = self.facet_vertices[fixed_facet].index(vertex1)
        fixed_facet_point2 = self.facet_vertices[fixed_facet].index(vertex2)
        facet_point1 = self.facet_vertices[facet].index(vertex1)
        facet_point2 = self.facet_vertices[facet].index(vertex2)

        fixed_coord1 = copy(fixed_facet_coords[fixed_facet_point1])
        fixed_coord2 = copy(fixed_facet_coords[fixed_facet_point2])
        coord1 = copy(self.projected_coordinates[facet][facet_point1])
        coord2 = copy(self.projected_coordinates[facet][facet_point2])
        
        diff_fixed_coord = fixed_coord2 - fixed_coord1
        diff_coord = coord2 - coord1

        r_mat = rot_mat(diff_coord, diff_fixed_coord)
        #print(r_mat)
        print_coordinates = self.projected_coordinates[facet] - coord1
        print_coordinates = np.matmul(r_mat, print_coordinates.transpose()).transpose() + fixed_coord1
        return print_coordinates

    def map_order(self, tree):
        n = tree.shape[0]
        connected = []
        mapped = []
        connections = []
        for i_node, node in enumerate(tree):
            if not np.sum(node):
                connected.append(i_node)
                mapped.append(i_node)
        for start_node in range(n):
            if start_node not in mapped:
                mapped.append(start_node)
                break
      
        while len(connected) < n:
            for i_map in range(n):
                if i_map in mapped and i_map not in connected:
                    break
            for i_connect in range(n):
                if tree[i_map, i_connect] and i_connect not in mapped:
                    mapped.append(i_connect)
                    connections.append([i_map, i_connect])
            connected.append(i_map)
        return connections

    def connecting_nodes(self, connected_nodes, tree):
        # TODO: Precompute this map.
        n_vertices = len(connected_nodes)
        connecting_edges = np.zeros(n_vertices, dtype=int)
        for i_vertex, vertex in enumerate(connected_nodes):
            for i_edge in self.facet_edges[vertex[0]]:
                if i_edge in self.facet_edges[vertex[1]]:
                    connecting_edges[i_vertex] = i_edge
                    break
        return connecting_edges

    def compute_print_coordinates(self, tree):
        print_coordinates = copy(self.projected_coordinates)
        map_order = self.map_order(tree)
        test_tree = self.connecting_nodes(map_order, tree)
        #test_tree = connection_vertices #[0, 3, 6, 7, 14, 13]
        #print_coordinates.append(self.projected_coordinates[map_order[0][0]])
        for i in range(len(test_tree)):
            print_coordinates[map_order[i][1]] = self.align_facet_edges(map_order[i][0], map_order[i][1],
                                                                        test_tree[i], print_coordinates[map_order[i][0]])

        return print_coordinates

    def get_tree_nodes(self, tree):
        nodes = []
        for i_node, node in enumerate(tree): 
            if np.sum(node): nodes.append(i_node)

        return nodes
    
    def print_tree(self, nodes,  print_coordinates,
                   colors='b', edgecolor='k',
                   alpha=.5, save_fig=False, show_fig=True, animate=False,
                   name_base="fig", name_rule="", file_type="pdf",
                   animation_filetype="mpeg"):
        fig, ax = plt.subplots()
        n_sides = len(nodes)
        if len(colors) == 1: colors = [colors for i in range(n_sides)]

        for i_color in range(len(nodes)):
            polygon = print_coordinates[nodes[i_color]]
            p = Polygon(polygon[:,:2], facecolor = colors[nodes[i_color]],
                        alpha=alpha, edgecolor=edgecolor)
        
            ax.add_patch(p)
    
        ax.set_xlim([-400, 400])
        ax.set_ylim([-400, 400])
        if save_fig:
            #print(name_base)
            #print(name_rule)
            #print(file_type)
            file_name = name_base + name_rule + "." + file_type
            #print(file_name)
            plt.savefig(file_name)

        if animate:
            ...


        if show_fig:
            plt.show()
        plt.close()

def animate():
    ...

def test_polyeder():
    poly = Polyeder()

    poly.project_facets()
    #print(poly.projected_coordinates[:2])
    tree = np.zeros((7,7))
    if False:
        for i in range(0, 3):
            tree[i, i + 1] = 1
            tree[i+1, i] = 1
    elif True:
        tree[0, 1] = 1
        tree[1, 0] = 1
        tree[1, 2] = 1 
        tree[2, 1] = 1
        tree[1, 3] = 1
        tree[3, 1] = 1 
        tree[3, 4] = 1
        tree[4, 3] = 1
        tree[4, 5] = 1
        tree[5, 4] = 1 
        tree[4, 6] = 1
        tree[6, 4] = 1
    print(tree)
    print_coordinates = poly.compute_print_coordinates(tree)
    nodes = poly.get_tree_nodes(tree)
    poly.print_tree(nodes, print_coordinates, colors=('b', 'b', 'y', 'y', 'c', 'm', 'r'))


