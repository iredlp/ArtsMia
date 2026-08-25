import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph=nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMapAO={}
        for n in self._nodes:
            self._idMapAO[n.object_id]=n

    def getInfoCompConnessa(self, id_oggetto):
        #cercare la componente connessa che contiene id_oggetto

        #STRATEGIA 1
        if not self.hasNode(id_oggetto):
            return None #ho controllato se è nei nodi
        source=self._idMapAO[id_oggetto]

        dfsTree=nx.dfs_tree(self._graph,source)
        #la dimensione della componente connessa è uguale alla len (dfsTree)
        print(f"Size connesssa con dfs_tree {len(dfsTree.nodes())}")

        #STRATEGIA 2
        #esplorazione per successori o i predereccori
        dfsPred= nx.dfs_predecessors(self._graph,source)
        print(f"Size connesssa con dfs_predecessors {len(dfsPred.values())}") #uso values pk è un dizionario
        #ma questo non stampa il nodo source - quindi devo tenerlo in considerazione

        #STRATEGIA 3
        #METODO PIù FACILE- uso la libreria
        conn=nx.node_connected_component(self._graph, source)
        print(f"Size connesssa con node_connected_component{len(conn)}")

    def hasNode(self, id_oggetto):
        return id_oggetto in self._idMapAO #BOOLEANO



    def buildGraph(self):
        #AGGIUNGE I NODI

        self._graph.add_nodes_from(self._nodes)

        #AGGIUNGE GLI ARCHI
        self.addEdgesV2()

    def addEdges(self):
        #MOLTO POCO EFFICIENTE
        for u in self._nodes:
            for v in self._nodes:
                peso=DAO.getEdgePeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)
                    print(f"Aggiunto arco fra {u} e {v} con peso {peso}")

    def addEdgesV2(self):
        allEdges=DAO.getAllEdges(self._idMapAO)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getNumNodes(self):
        return len(self._nodes)

    def getNumEdges(self):
        return len(self._graph.edges())