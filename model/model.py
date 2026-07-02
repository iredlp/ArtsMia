import copy

import networkx as nx
from database.DAO import DAO

class Model():
    def __init__(self):
        self._graph=nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO={ } #DIZIONARIO
        for n in self._nodes:
            self._idMapAO[n.object_id]=n

        self._optPath = []  # che dopo la ricorsione conterrà la lista di nodi ottima
        self._optCost = 0  # valore che stiamo massimizzando, lo inizializzo a zero


    def getOptPath(self, source, lun):  # gestisce la RICORSIONE
        parziale = [source]

        for n in self._graph.neighbors(source):  # o parziale -1
            if n.classification == parziale[-1].classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)  # CHIAMO IL METODO RICORSIVO
                parziale.pop()  # Backtracking
        return self._optPath, self._optCost


    def _ricorsione(self, parziale, lun):
        # verificarre la condizione di terminazione
        if len(parziale) == lun:  # allora parziale è lunga esattamente lun
            # per cui verifico che questa parziale sia me
            # condizione di terminazionglio del mio best(condizione di ottimalità)
            # ed in ogni caso esco
            if self._costoPath(parziale) > self._optCost:
                self._optCost = self._costoPath(parziale)
                self._optPath = copy.deepcopy(
                    parziale)  # DEVO SALVARE NELLA COPIA PROFONDAAA (perchè parziale è un oggetto)
            return

        # se arrivo qui posso ancora aggiungere nodi
        #print(len(parziale))
        for n in self._graph.neighbors(parziale[-1]):  # così prendo l'ultimo
            if parziale[
                -1].classification == n.classification:  # se la class è = alla class dell'ulimo nodo aggiunto in prziale
                parziale.append(n)
                self._ricorsione(parziale, lun)  # CHIAMO IL METODO RICORSIVO
                parziale.pop()  # Backtracking


    def _costoPath(self, path):
        costo = 0
        for i in range(0, len(path) - 1):
            costo += self._graph[path[i]][path[i + 1]]["weoght"]  # nodo partrnza, nodo arrivo, peso
        return costo


    def getInfoCompConnessa(self, id_oggetto):
            #cercare la componente connessa che contine l'id_oggetto

            #controllo se ha senso cercare la componenete connessa
            if not self.hasNode(id_oggetto):
                return None

            #1) RICERCA DFS cercare poi i nodi
            source=self._idMapAO[id_oggetto]
            dfsTree=nx.dfs_tree(self._graph,source) #source è il nodo associato all'ID oggetto
            print("size connessa con dfs_tree=",len(dfsTree.nodes()))

            #2) PRENDO I PREDECESSORI traminte dfs
            dfsPred=nx.dfs_predecessors(self._graph,source)
            print("size connessa con dfs predecessor",len(dfsPred.values()))

            #3) UTILIZZO I METODI DELLA LIBRERIA- DA USARE
            conn=nx.node_connected_component(self._graph,source)
            print("size connessa con node connected component", len(conn))

            return len(conn)

    def hasNode(self,id_oggetto): #mi va a verificare se l'id è contenuto nel grafo
        return id_oggetto in self._idMapAO

    def buildGraph(self):
        #aggiunge i nodi
        self._nodes=DAO.getAllNodes()
        self._graph.add_nodes_from(self._nodes)
        #aggiunge gli archi
        self.addEdgesV2(self._nodes)

    def getNumNodes(self):
        return len(self._graph.nodes)

    def addEdges(self):
        for u in self._nodes:
            for v in self._nodes:
                peso=DAO.getEdgePeso(u,v)
                if peso is None:
                    self._graph.add_edge(u, v, weight=peso)
                    print(f"Aggiunto arco fra {u}e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges=DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1,e.o2,weight=e.peso)
    def getNumEdges(self):
        return len(self._graph.edges)

