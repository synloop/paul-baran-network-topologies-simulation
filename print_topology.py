import networkx as nx
import matplotlib.pyplot as plt
from simulation import generate_topology

G = generate_topology(R=2, grid_size=4)

nx.draw(G, with_labels=False, node_size=30)
plt.show()
