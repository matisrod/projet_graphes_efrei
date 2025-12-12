import function as f

if __name__ == "__main__":
    dico = f.build_graph_from_csv('graphe_villes.csv')
    for x in dico:
        print(f"{x} : {dico[x]}")
    print('\n-----------------Algo-----------\n')
    
    bfs = f.bfs(dico,"Paris")
    print(bfs)
    
    