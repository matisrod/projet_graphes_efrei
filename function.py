from collections import defaultdict
from collections import deque
import csv

def build_graph_from_csv(path, directed: bool = False) -> dict:
    """
    Construit un dictionnaire d'adjacence pondéré à partir d'un CSV.
    - path: chemin du fichier CSV (colonnes: Ville1, Ville2, Distance)
    - directed: True pour un graphe orienté, False pour non orienté
    Retour: {noeud: {voisin: poids, ...}, ...}
    """
    adj = defaultdict(dict)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            u = row["Ville1"].strip()
            v = row["Ville2"].strip()
            w = float(row.get("Distance", 1))
            adj[u][v] = w
            if not directed:
                adj[v][u] = w
    # cast en dict "pur"
    return {node: dict(neigh) for node, neigh in adj.items()}


def bfs(graphe,sommet_depart):
    visited = set()
    queue = deque([sommet_depart])
    print("BFS : ")
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            print(node, end = ' ')
            bfs = queue.extend(voisin for voisin in graphe[node] if voisin not in visited)
    return bfs
#def dfs(graphe,sommet_depart):
    
    