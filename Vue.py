import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import function as f
import matplotlib.colors as mcolors


class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Graphes Complet - Projet EFREI")

        # Chargement des données
        self.graph_data = f.build_graph_from_csv('graphe_villes.csv')
        self.villes = sorted(list(self.graph_data.keys()))

        # --- Panneau Latéral (Menu) ---
        self.frame_sidebar = tk.Frame(root, width=280, bg="#f1f3f5")
        self.frame_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Label(self.frame_sidebar, text="Menu Algorithmes", font=('Arial', 14, 'bold'), bg="#f1f3f5").pack(pady=10)

        # Sélection Villes
        tk.Label(self.frame_sidebar, text="Départ :", bg="#f1f3f5").pack(anchor="w")
        self.combo_start = ttk.Combobox(self.frame_sidebar, values=self.villes, state="readonly")
        self.combo_start.pack(fill=tk.X, pady=2)
        self.combo_start.set("Paris")

        tk.Label(self.frame_sidebar, text="Arrivée (Dijkstra/BF) :", bg="#f1f3f5").pack(anchor="w")
        self.combo_end = ttk.Combobox(self.frame_sidebar, values=self.villes, state="readonly")
        self.combo_end.pack(fill=tk.X, pady=2)
        self.combo_end.set("Grenoble")

        # --- Section Boutons ---
        buttons = [
            ("Réinitialiser", self.draw_graph, "#6c757d"),
            ("BFS (Largeur)", lambda: self.run_traversal("BFS"), "#fd7e14"),
            ("DFS (Profondeur)", lambda: self.run_traversal("DFS"), "#6f42c1"),
            ("Dijkstra", self.run_dijkstra, "#28a745"),
            ("Bellman-Ford", self.run_bellman, "#dc3545"),
            ("Floyd-Warshall", self.run_floyd, "#007bff"),
            ("Prim (MST)", self.run_prim, "#17a2b8"),
            ("Kruskal (MST)", self.run_kruskal, "#20c997"),
            ("PERT (Graphe de tâches)", self.run_pert, "#343a40")
        ]

        for text, cmd, color in buttons:
            tk.Button(self.frame_sidebar, text=text, command=cmd, bg=color, fg="white", font=('Arial', 9, 'bold')).pack(
                fill=tk.X, pady=3)

        # --- Console de texte pour les résultats ---
        tk.Label(self.frame_sidebar, text="Résultats détaillés :", bg="#f1f3f5").pack(anchor="w", pady=(15, 0))
        self.console = tk.Text(self.frame_sidebar, height=10, width=30, font=('Consolas', 9))
        self.console.pack(fill=tk.X, pady=5)

        # --- Zone Graphique ---
        self.fig, self.ax = plt.subplots(figsize=(7, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.draw_graph()

    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

    def draw_graph(self, highlight_edges=None, node_colors=None):
        self.ax.clear()
        G = nx.Graph()
        for u, neighbors in self.graph_data.items():
            for v, weight in neighbors.items():
                G.add_edge(u, v, weight=weight)
        pos = nx.spring_layout(G, seed=42)

        color_map = [node_colors.get(node, 'skyblue') if node_colors else 'skyblue' for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=1000, ax=self.ax, font_size=8)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), ax=self.ax, font_size=7)
        if highlight_edges:
            nx.draw_networkx_edges(G, pos, edgelist=highlight_edges, edge_color='red', width=3, ax=self.ax)
        self.canvas.draw()

    #Algorithmes

    def run_traversal(self, mode):
        start = self.combo_start.get()
        order = f.bfs(self.graph_data, start) if mode == "BFS" else f.dfs(self.graph_data, start)
        self.log(f"[{mode}] Départ {start}: {' -> '.join(order)}")
        colors = {node: list(mcolors.TABLEAU_COLORS.values())[i % 10] for i, node in enumerate(order)}
        self.draw_graph(node_colors=colors)

    def run_dijkstra(self):
        start, end = self.combo_start.get(), self.combo_end.get()
        path, dist = f.dijkstra(self.graph_data, start, end)

        if not path or dist == float('inf'):
            self.log(f"[Dijkstra] Aucun chemin trouvé entre {start} et {end}")
            messagebox.showwarning("Erreur", f"Aucun chemin possible entre {start} et {end}")
            return

        self.log(f"[Dijkstra] {start} -> {end}: {dist} km")

        #Création de la liste des arêtes pour l'affichage graphique
        edges_to_highlight = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        self.draw_graph(highlight_edges=edges_to_highlight)


    def run_prim(self):
        mst = f.prim(self.graph_data, self.combo_start.get())
        self.draw_graph(highlight_edges=[(u, v) for u, v, w in mst])
        self.log(f"[Prim] MST calculé.")

    def run_kruskal(self):
        mst = f.kruskal(self.graph_data)
        self.draw_graph(highlight_edges=[(u, v) for u, v, w in mst])
        self.log(f"[Kruskal] MST global calculé.")

    def run_bellman(self):
        start, end = self.combo_start.get(), self.combo_end.get()
        path, dist = f.bellman_ford(self.graph_data, start, end)
        if path is None and dist == "Cycle négatif détecté":
            self.log("[Bellman-Ford] Erreur : Cycle négatif !")
            messagebox.showerror("Erreur", "Un cycle négatif a été détecté.")
            return
        if not path:
            self.log(f"[Bellman-Ford] Aucun chemin entre {start} et {end}")
            return
        self.log(f"[Bellman-Ford] {start} -> {end}: {dist} km")
        edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        self.draw_graph(highlight_edges=edges)

    def run_floyd(self):
        start, end = self.combo_start.get(), self.combo_end.get()
        self.log("[Floyd-Warshall] Calcul de toutes les distances en cours...")

        matrix = f.floyd_warshall(self.graph_data)
        dist_finale = matrix[start][end]

        if dist_finale == float('inf'):
            self.log(f"[Floyd-Warshall] Pas de connexion entre {start} et {end}")
        else:
            self.log(f"[Floyd-Warshall] Distance {start} vers {end} : {dist_finale} km")
            messagebox.showinfo("Floyd-Warshall",
                                f"La distance la plus courte entre {start} et {end} est de {dist_finale} km.")

    def run_pert(self):
        self.log("\n" + "=" * 30)
        self.log(" ANALYSE DU PROJET (PERT)")
        self.log("=" * 30)
        try:

            graph_pert = f.build_graph_from_csv('graphe_villes_for_pert.csv', directed=True)
            tot, tard, critique, fin = f.calculer_pert(graph_pert)


            self.log(f"Durée totale estimée : {fin} jours")
            self.log(f"{'Tâche':<12} | {'Tôt':<4} | {'Tard':<5} | {'Marge'}")
            for n in tot:
                m = tard[n] - tot[n]
                self.log(f"{n:<12} | {tot[n]:<4} | {tard[n]:<5} | {m}")

            self.ax.clear()
            G = nx.DiGraph()
            for u, neighbors in graph_pert.items():
                for v, w in neighbors.items():
                    G.add_edge(u, v, weight=w)

            pos = nx.spring_layout(G, k=2, seed=42)


            nx.draw_networkx_edges(G, pos, ax=self.ax, edge_color='#BDC3C7', arrows=True, arrowsize=15)
            nx.draw_networkx_edges(G, pos, edgelist=critique, ax=self.ax, edge_color='#E74C3C', width=3, arrows=True,
                                   arrowsize=20)


            node_colors = ['#F39C12' if tot[n] == tard[n] else '#3498DB' for n in G.nodes()]
            nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=node_colors, node_shape='s', node_size=2000)


            labels = {n: f"{n}\n{tot[n]} | {tard[n]}" for n in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels=labels, ax=self.ax, font_size=7, font_weight='bold',
                                    font_color='white')


            edge_labels = nx.get_edge_attributes(G, 'weight')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=self.ax, font_size=7)

            self.ax.set_title(f"Diagramme PERT - Fin du projet : {fin} jours", fontsize=10, fontweight='bold',
                              color='#2C3E50')
            self.canvas.draw()

            messagebox.showinfo("PERT", f"Analyse terminée.\nChemin critique en rouge.\nDurée totale : {fin}")

        except Exception as e:
            self.log(f"Erreur : {e}")
            messagebox.showerror("Erreur PERT", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x700")
    app = GraphApp(root)
    root.mainloop()