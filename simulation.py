import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import statistics

def generate_topology(R, grid_size=18):
    if R == 1:
        G = nx.path_graph(grid_size ** 2)  # juste une ligne
    elif R == 2:
        G = nx.grid_2d_graph(grid_size, grid_size)  # Grille simple
    elif R == 3:
        G = nx.grid_2d_graph(grid_size, grid_size) #puis je fais en sorte qu'il y ait à chaque fois le bon nombre de liens par noeuds
        for node in list(G.nodes()):
            if 0 < node[0] <= grid_size - 1 and 0 < node[1] <= grid_size - 1:
                if (node[0] + 1, node[1] + 1) in G:
                    G.add_edge(node, (node[0] + 1, node[1] + 1))
                if (node[0] - 1, node[1] - 1) in G:
                    G.add_edge(node, (node[0] - 1, node[1] - 1))
    elif R == 4:
        G = nx.grid_2d_graph(grid_size, grid_size)
        for node in list(G.nodes()):
            if 0 < node[0] <= grid_size - 1 and 0 <= node[1] <= grid_size - 1:
                if (node[0] + 1, node[1] + 1) in G:
                    G.add_edge(node, (node[0] + 1, node[1] + 1))
                if (node[0] - 1, node[1] - 1) in G:
                    G.add_edge(node, (node[0] - 1, node[1] - 1))
                if (node[0] + 1, node[1] - 1) in G:
                    G.add_edge(node, (node[0] + 1, node[1] - 1))
                if (node[0] - 1, node[1] + 1) in G:
                    G.add_edge(node, (node[0] - 1, node[1] + 1))
    elif R == 5:
        G = nx.grid_2d_graph(grid_size, grid_size)

        # je refais R = 4 dans un premier temps
        for (x, y) in list(G.nodes()):
            if 0 < x <= grid_size - 1 and 0 <= y <= grid_size - 1:
                if (x + 1, y + 1) in G:
                    G.add_edge((x, y), (x + 1, y + 1))
                if (x - 1, y - 1) in G:
                    G.add_edge((x, y), (x - 1, y - 1))
                if (x + 1, y - 1) in G:
                    G.add_edge((x, y), (x + 1, y - 1))
                if (x - 1, y + 1) in G:
                    G.add_edge((x, y), (x - 1, y + 1))

        # diagonales supplémentaires
        for (x, y) in list(G.nodes()):
            #(i+1, j+2)
            if x + 1 < grid_size and y + 2 < grid_size:
                G.add_edge((x, y), (x + 1, y + 1))
            # (i-1, j-2)
            if x - 1 >= 0 and y - 2 >= 0:
                G.add_edge((x, y), (x - 1, y - 2))

    elif R == 6:
        G = nx.grid_2d_graph(grid_size, grid_size)

        # je refais R = 4 dans un premier temps
        for (x, y) in list(G.nodes()):
            if 0 < x <= grid_size - 1 and 0 <= y <= grid_size - 1:
                if (x + 1, y + 1) in G:
                    G.add_edge((x, y), (x + 1, y + 1))
                if (x - 1, y - 1) in G:
                    G.add_edge((x, y), (x - 1, y - 1))
                if (x + 1, y - 1) in G:
                    G.add_edge((x, y), (x + 1, y - 1))
                if (x - 1, y + 1) in G:
                    G.add_edge((x, y), (x - 1, y + 1))

        # diagonales de R = 5
        for (x, y) in list(G.nodes()):
            if x + 1 < grid_size and y + 2 < grid_size:
                G.add_edge((x, y), (x + 1, y + 2))
            if x - 1 >= 0 and y - 2 >= 0:
                G.add_edge((x, y), (x - 1, y - 2))

        # diagonales dans le sens opposé
        for (x, y) in list(G.nodes()):
            if x + 1 < grid_size and y - 2 >= 0:
                G.add_edge((x, y), (x + 1, y - 2))
            if x - 1 >= 0 and y + 2 < grid_size:
                G.add_edge((x, y), (x - 1, y + 2))

    else:
        raise ValueError("R doit être entre 1 et 6.")
    
    return nx.convert_node_labels_to_integers(G)

def simulate_failures(G, Pp, num_simulations=15):
    surviving_fractions = []
    for _ in range(num_simulations):
        G_copy = G.copy()
        nodes_to_remove = np.random.choice(G_copy.nodes(), int(Pp * len(G_copy)), replace=False)
        G_copy.remove_nodes_from(nodes_to_remove)
        largest_cc = max(nx.connected_components(G_copy), key=len, default=[])
        surviving_fractions.append(len(largest_cc) / len(G))
    
    mean_survival = np.mean(surviving_fractions)
    std_dev = statistics.stdev(surviving_fractions) if len(surviving_fractions) > 1 else 0
    return mean_survival, std_dev

def run_simulation():
    grid_size = 18
    probabilities = np.linspace(0, 1, 30)
    results = {R: [] for R in range(1, 7)}
    std_devs = {R: [] for R in range(1, 7)}
    
    for R in results.keys():
        G = generate_topology(R, grid_size)
        for Pp in probabilities:
            mean_survival, std_dev = simulate_failures(G, Pp)
            results[R].append(mean_survival)
            std_devs[R].append(std_dev)
    
    best_possible_line = [1 - Pp for Pp in probabilities]
    
    plt.figure(figsize=(10, 6))
    for R in results.keys():
        plt.errorbar(probabilities, results[R], yerr=std_devs[R], fmt='-o', label=f"R={R}", capsize=3)
    plt.plot(probabilities, best_possible_line, 'k--', label="Best possible line")
    plt.xlabel("Single node probability of destruction")
    plt.ylabel("Survivability: Largest fraction of stations in communication")
    plt.title("Sensitivity to node destruction - 100% of links operative")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    run_simulation()