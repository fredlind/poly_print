"""
Maybe have polygons that has both a local and global node numberings. 
Maybe define a way to traverse the graph and add nodes and polygons
"""

class CollapsedPolyeder():
    def __init__(self, polyeder):
        self.polyeder = polyeder
        self.polygons = "hej"

class Polyeder():
    def __init__(self):
        self.facet_edges = [[0, 2, 1],
                            [0, 9, 10, 11, 4],
                            [2, 3, 4, 5, 6],
                            [1, 6, 7, 8, 9],
                            [12, 14, 7, 5],
                            [8, 14, 13, 10],
                            [11, 13, 12, 4]
                           ]

        
        self.facet_vertices = [[0, 1, 2],
                              [0, 5, 6, 7],
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
                    