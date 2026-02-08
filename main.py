import function as f

if __name__ == "__main__":
    graph = f.build_graph_from_csv('graphe_villes.csv')
    graph_oriented = f.build_graph_from_csv('graphe_villes_for_pert.csv', directed=True)
    nodes = list(graph.keys())
    print(nodes)
    ville_reference = "Lille"
    
    # 2. Tests des Parcours
    print(f"\n[PARCOURS] au départ de {ville_reference}:")
    bfs_result = f.bfs(graph, ville_reference)
    dfs_result = f.dfs(graph, ville_reference)
    print(f"  BFS : {' --> '.join(bfs_result)}")
    print(f"  DFS : {' --> '.join(dfs_result)}")

    # 3. Arbres Couvrants Minimum (MST)
    print("\n[ARBRES COUVRANTS MINIMUM] :")
    print(f"  Prim (depuis {ville_reference}) : {f.prim(graph, ville_reference)}")
    print(f"  Kruskal : {f.kruskal(graph)}")

    # 4. Plus courts chemins (Dijkstra & Bellman-Ford)
    print(f"\n[PLUS COURTS CHEMINS] au départ de {ville_reference}:")
    
    d_dist, d_pred = f.dijkstra(graph, ville_reference,"Grenoble")
    print(f"  Dijkstra (Distances) : {d_dist}")
    print(f"  Dijkstra (Prédécesseurs) : {d_pred}")
    
    b_dist, b_pred = f.bellman_ford(graph, ville_reference, "Grenoble")
    print(f"  Bellman-Ford (Distances) : {b_dist}")
    print(f"  Bellman-Ford (Prédécesseurs) : {b_pred}")

    # 5. Floyd-Warshall (Toutes paires)
    print("\n[FLOYD-WARSHALL] (Matrice de distances entre toutes les villes) :")
    fw_matrix = f.floyd_warshall(graph)
    for ville_dep, destinations in fw_matrix.items():
        print(f"  De {ville_dep} : {destinations}")

    # 5. Analyse PERT (Gestion de projet / Ordonnancement)
    print("\n--- Analyse PERT (Ordonnancement) ---")
    tot, tard, critique, fin = f.calculer_pert(graph_oriented)
    print(f"\n--- RÉSULTATS PERT ---")
    print(f"Durée totale : {fin}")
    print(f"Dates au plus tôt : {tot}")
    print(f"Dates au plus tard : {tard}")
    print(f"Arêtes du chemin critique : {critique}")
