import numpy as np
from scipy.spatial.transform import Rotation
from geometry import rotation_matrix_from_vectors as rot_mat
from copy import copy
import matplotlib.pyplot as plt
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
        
        self.coordinates3d = [[0, 1, 2],
                              [1, 0, 2],
                              [0, 0, 1],
                              [0, 0, 0],
                              [0, 2, 0],
                              [0, 2, 2],
                              [3, 2, 2],
                              [3, 0, 2],
                              [3, 0, 0],
                              [3, 2, 0]]
        
        self.edge_vertices = [[0, 1],
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
        r_mat = rot_mat(vect_to_rotate, target)
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

    def align_facet_edges(self, fixed_facet, facet, common_edge):
        # 
        vertex1, vertex2 = self.edge_vertices[common_edge]
        print(fixed_facet, facet, common_edge,vertex1, vertex2)
        fixed_facet_point1 = self.facet_vertices[fixed_facet].index(vertex1)
        fixed_facet_point2 = self.facet_vertices[fixed_facet].index(vertex2)
        facet_point1 = self.facet_vertices[facet].index(vertex1)
        facet_point2 = self.facet_vertices[facet].index(vertex2)

        fixed_coord1 = copy(self.projected_coordinates[fixed_facet][fixed_facet_point1])
        fixed_coord2 = copy(self.projected_coordinates[fixed_facet][fixed_facet_point2])
        coord1 = copy(self.projected_coordinates[facet][facet_point1])
        coord2 = copy(self.projected_coordinates[facet][facet_point2])
        
        diff_fixed_coord = fixed_coord2 - fixed_coord1
        diff_coord = coord2 - coord1

        r_mat = rot_mat(diff_coord, diff_fixed_coord)
        self.projected_coordinates[facet] -= coord1 - fixed_coord1
        self.projected_coordinates[facet] = np.matmul(r_mat, self.projected_coordinates[facet].transpose()).transpose()


        
poly = Polyeder()

poly.project_facets()
#print(poly.projected_coordinates[:2])
test_tree = [0, 3, 6, 7, 14, 13]
for i in range(6):
    poly.align_facet_edges(i, i + 1, test_tree[i])

#print(poly.projected_coordinates[:2])
fig,ax = plt.subplots()
for polygon in poly.projected_coordinates:
    p = Polygon(polygon[:,:2], facecolor = 'b', alpha=0.1, edgecolor='k')


    ax.add_patch(p)
    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])

plt.show()