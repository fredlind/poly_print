import numpy as np
import polyeder
import kjetil_det
from kjetils_graph import get_verbose_graph_description
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

poly = polyeder.Polyeder()
poly.project_facets()

for projected_side in poly.projected_coordinates:
    fig, ax = plt.subplots()
    p = Polygon(projected_side[:,:2], facecolor = 'b',
                alpha=.25, edgecolor='k')
        
    ax.add_patch(p)
    ax.set_xlim([-200, 200])
    ax.set_ylim([-200, 200])
    plt.show()