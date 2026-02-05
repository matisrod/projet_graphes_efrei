import function as f

if __name__ == "__main__":
    graph = f.build_graph_from_csv('graphe_villes.csv')
    for x in graph:
        print(f"{x} : {graph[x]}")

    print("\n--- 2. Arbres Couvrant Minimum (MST) ---")
    prim_mst = f.prim(graph, 'Rennes')
    print(f"Prim (départ Rennes) - {len(prim_mst)} arêtes :")
    total_prim = 0
    for u, v, w in prim_mst:
        print(f"  - {u} -- {v} ({w} km)")
        total_prim += w
    print(f"  Coût Total Prim: {total_prim} km")

    kruskal_mst = f.kruskal(graph)
    print(f"\nKruskal (Global) - {len(kruskal_mst)} arêtes :")
    total_kruskal = 0
    for u, v, w in kruskal_mst:
        print(f"  - {u} -- {v} ({w} km)")
        total_kruskal += w
    print(f"  Coût Total Kruskal: {total_kruskal} km")