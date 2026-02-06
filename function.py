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


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > distances[u]: continue
        
        for v, weight in graph.get(u, {}).items():
            if distances[u] + weight < distances[v]:
                distances[v] = distances[u] + weight
                predecessors[v] = u
                heapq.heappush(pq, (distances[v], v))
    
    return distances, predecessors


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


def bellman_ford(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    predecessors = {node: None for node in graph}
    
    nodes = list(graph.keys())
    for _ in range(len(nodes) - 1):
        for u in nodes:
            for v, w in graph[u].items():
                if distances[u] + w < distances[v]:
                    distances[v] = distances[u] + w
                    predecessors[v] = u
                    
    for u in nodes:
        for v, w in graph[u].items():
            if distances[u] + w < distances[v]:
                return "Cycle négatif détecté", None

    return distances, predecessors


def floyd_warshall(graph):
    nodes = list(graph.keys())
    dist = {n1: {n2: float('inf') for n2 in nodes} for n1 in nodes}
    
    for n in nodes:
        dist[n][n] = 0
        for neighbor, weight in graph[n].items():
            dist[n][neighbor] = weight
            
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def pert_analysis(graph):
    # 1. Calcul des degrés entrants
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            # Initialiser v s'il n'est pas clé du graphe (destination sans départ)
            if v not in in_degree: in_degree[v] = 0
            in_degree[v] += 1
    
    # 2. Files des noeuds sans dépendance
    queue = deque([u for u in in_degree if in_degree[u] == 0])
    topo_order = []
    
    while queue:
        u = queue.popleft()
        topo_order.append(u)
        
        if u in graph: # Vérifier si u a des voisins
            for v in graph[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

    # --- DETECTION DE CYCLE ---
    # Si on n'a pas pu ordonner tous les noeuds, c'est qu'il y a un cycle
    if len(topo_order) < len(in_degree):
        print("ERREUR : Le graphe contient un cycle (boucle) ! PERT impossible.")
        return {}, []

    # 3. Calcul des dates au plus tôt
    earliest_start = {u: 0 for u in in_degree}
    for u in topo_order:
        if u in graph:
            for v, duration in graph[u].items():
                if earliest_start[v] < earliest_start[u] + duration:
                    earliest_start[v] = earliest_start[u] + duration
                
    return earliest_start, topo_order