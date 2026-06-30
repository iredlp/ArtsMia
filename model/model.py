import networkx as nx
from database.DAO import DAO

class Model():
    def __init__(self):
        self._graph=nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO={ } #DIZIONARIO
        for n in self._nodes:
            self._idMapAO[n.object_id]=n

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

