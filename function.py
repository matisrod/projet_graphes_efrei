from collections import defaultdict
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


def prim(graph, start_node):
    """
    Algorithme de Prim.
    Retourne une liste de tuples (u, v, poids).
    """
    mst_edges = []
    visited = {start_node}
    all_nodes = set(graph.keys())

    while len(visited) < len(all_nodes):
        min_edge = None
        min_weight = float('inf')

        for u in visited:
            # --- CORRECTION ICI : ajout de .items() ---
            for v, weight in graph[u].items():
                if v not in visited:
                    if weight < min_weight:
                        min_weight = weight
                        min_edge = (u, v, weight)
        
        if min_edge:
            u, v, w = min_edge
            visited.add(v)
            mst_edges.append(min_edge)
        else:
            break
            
    return mst_edges


class UnionFind:
    def __init__(self, elements):
        self.parent = {e: e for e in elements}

    def find(self, item):
        if self.parent[item] != item:
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a != root_b:
            self.parent[root_b] = root_a
            return True
        return False

def kruskal(graph):
    """
    Algorithme de Kruskal.
    Retourne une liste de tuples (u, v, poids).
    """
    mst_edges = []
    edges = []
    seen_edges = set()

    for u in graph:
        # --- CORRECTION ICI : ajout de .items() ---
        for v, w in graph[u].items():
            edge_id = tuple(sorted((u, v)))
            if edge_id not in seen_edges:
                edges.append((w, u, v))
                seen_edges.add(edge_id)
    
    edges.sort() 

    uf = UnionFind(graph.keys())
    
    for w, u, v in edges:
        if uf.union(u, v):
            mst_edges.append((u, v, w))
            
    return mst_edges
