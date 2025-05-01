from simulation import generate_topology, simulate_failures

G = generate_topology(R=4)
Pp = 0.3  # si x% des noeuds tombent en panne

survie = simulate_failures(G, Pp)
print(f"Niveau de survie après panne : {survie*100:.2f}%")
