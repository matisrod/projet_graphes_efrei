from collections import defaultdict
from collections import deque
import csv
import heapq



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


def bfs(graph, start):
    visited = []
    queue = deque([start])
    seen = {start}
    
    while queue:
        vertex = queue.popleft()
        visited.append(vertex)
        for neighbor in graph.get(vertex, {}):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    return visited


def dfs(graph, start_node, visited=None):
    if visited is None:
        visited = []
    if start_node not in visited:
        visited.append(start_node)
        for neighbor in graph.get(start_node, {}):
            dfs(graph, neighbor, visited)
    return visited


def prim(graph, start_node):
    mst_edges = []
    visited = {start_node}
    all_nodes = set(graph.keys())

    while len(visited) < len(all_nodes):
        min_edge = None
        min_weight = float('inf')
        for u in visited:
            for v, weight in graph.get(u, {}).items():
                if v not in visited and weight < min_weight:
                    min_weight = weight
                    min_edge = (u, v, weight)
        if min_edge:
            visited.add(min_edge[1])
            mst_edges.append(min_edge)
        else: break
    return mst_edges


def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)

        if u == end: break  # Optimisation : on s'arrête si on a atteint la destination
        if d > distances[u]: continue

        for v, weight in graph.get(u, {}).items():
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                heapq.heappush(pq, (distances[v], v))

    # Reconstruction du chemin de la fin vers le début
    path = []
    current = end
    if distances[end] != float('inf'):  # Si un chemin existe
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()  # On remet dans l'ordre Départ -> Arrivée

    return path, distances[end]

def get_path(predecessors, target):
    """recré le path de dijkstra à partir des prédécesseurs."""
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = predecessors[curr]
    return path[::-1]


def kruskal(graph):
    mst_edges = []
    edges = []
    seen_edges = set()
    for u in graph:
        for v, w in graph[u].items():
            edge_id = tuple(sorted((u, v)))
            if edge_id not in seen_edges:
                edges.append((w, u, v))
                seen_edges.add(edge_id)
    edges.sort() 
    
    parent = {n: n for n in graph}
    def find(i):
        if parent[i] == i: return i
        return find(parent[i])

    for w, u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u != root_v:
            mst_edges.append((u, v, w))
            parent[root_u] = root_v
    return mst_edges


def bellman_ford(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    nodes = list(graph.keys())

    # Relaxation des arêtes n-1 fois
    for _ in range(len(nodes) - 1):
        for u in nodes:
            for v, weight in graph.get(u, {}).items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u

    # Vérification des cycles négatifs
    for u in nodes:
        for v, weight in graph.get(u, {}).items():
            if distances[u] + weight < distances[v]:
                return None, "Cycle négatif détecté"

    # Reconstruction du chemin
    path = []
    if distances[end] != float('inf'):
        curr = end
        while curr is not None:
            path.append(curr)
            curr = predecessors[curr]
        path.reverse()

    return path, distances[end]


def floyd_warshall(graph):
    nodes = list(graph.keys())
    # Initialisation de la matrice
    dist = {u: {v: float('inf') for v in nodes} for u in nodes}

    for u in nodes:
        dist[u][u] = 0
        for v, weight in graph.get(u, {}).items():
            dist[u][v] = weight

    # Algorithme principal
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def calculer_pert(graph_pert):
    # 1. Calcul des dates au plus tôt (Early start)
    nodes = list(graph_pert.keys())
    # On s'assure d'avoir tous les noeuds même ceux sans successeurs
    all_nodes = set(nodes)
    for neighbors in graph_pert.values():
        all_nodes.update(neighbors.keys())
    all_nodes = sorted(list(all_nodes))  # Simplification, un tri topo serait mieux

    au_plus_tot = {node: 0 for node in all_nodes}

    # On parcourt plusieurs fois pour propager les durées (méthode simplifiée)
    for _ in range(len(all_nodes)):
        for u in graph_pert:
            for v, weight in graph_pert[u].items():
                if au_plus_tot[v] < au_plus_tot[u] + weight:
                    au_plus_tot[v] = au_plus_tot[u] + weight

    # 2. Calcul des dates au plus tard (Late start)
    fin_projet = max(au_plus_tot.values())
    au_plus_tard = {node: fin_projet for node in all_nodes}

    for _ in range(len(all_nodes)):
        for u in graph_pert:
            for v, weight in graph_pert[u].items():
                # date au plus tard de u = min(tard de v - durée u->v)
                if au_plus_tard[u] > au_plus_tard[v] - weight:
                    au_plus_tard[u] = au_plus_tard[v] - weight

    # 3. Identification du chemin critique (marge = 0)
    chemin_critique = []
    for u in graph_pert:
        for v, weight in graph_pert[u].items():
            if au_plus_tot[u] == au_plus_tard[u] and au_plus_tot[v] == au_plus_tard[v] and (
                    au_plus_tot[v] - au_plus_tot[u] == weight):
                chemin_critique.append((u, v))

    return au_plus_tot, au_plus_tard, chemin_critique, fin_projet