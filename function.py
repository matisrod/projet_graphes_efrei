from collections import defaultdict
from collections import deque
import csv

def build_graph_from_csv(path, directed: bool = False) -> dict:
    """
    Construit un dictionnaire d'adjacence pondéré à partir d'un CSV.
    Retour: {noeud: {voisin: poids, ...}, ...}
    """
    adj = defaultdict(dict)
    # Encodage utf-8-sig pour gérer les BOM (caractères bizarres) parfois présents au début des CSV Excel
    with open(path, newline="", encoding="utf-8-sig") as f: 
        reader = csv.DictReader(f, delimiter=',') # Assurez-vous que le délimiteur correspond à votre CSV
        for row in reader:
            # Sécurisation si des lignes vides traînent
            if not row or not row.get("Ville1"): continue
            
            u = row["Ville1"].strip()
            v = row["Ville2"].strip()
            w = float(row.get("Distance", 1))
            adj[u][v] = w
            if not directed:
                adj[v][u] = w
    return {node: dict(neigh) for node, neigh in adj.items()}



def bfs(graphe,sommet_depart):
    visited = set()
    queue = deque([sommet_depart])
    print("BFS : ")
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            print(node, end = ' -> ')
            bfs = queue.extend(voisin for voisin in graphe[node] if voisin not in visited)
    return bfs

def dfs(graphe,sommet,visited):
    if sommet not in visited:
        print(sommet)
        visited.add(sommet)
        for voisin in graphe[sommet]:
            dfs(graphe,sommet,visited)
    