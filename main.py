import function as f

if __name__ == "__main__":
    dico = f.build_graph_from_csv('graphe_villes.csv')
    for x in dico:
        print(f"{x} : {dico[x]}")
    print('\n-----------------Algo-----------\n')
    ville_reference = "Paris"
    bfs = f.bfs(dico,ville_reference)
    print(bfs)
    
    