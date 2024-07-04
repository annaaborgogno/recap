import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.aeroporti=DAO.getAllAirports()
        self._idMap = {}
        for v in self.aeroporti:
            self._idMap[v.ID] = v

    def creaGrafo(self, numeroCompagnie):
        self.nodi = DAO.getNodi(numeroCompagnie)
        self.grafo.add_nodes_from(self.nodi)
        self.addEdges()
        return self.grafo

    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def addEdges(self):
        self.grafo.clear_edges()
        allEdges = DAO.getConnessioni()
        for connessione in allEdges:
            nodo1 = self._idMap[connessione.v1]
            nodo2 = self._idMap[connessione.v2]
            if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                if self.grafo.has_edge(nodo1, nodo2) == False:
                    self.grafo.add_edge(nodo1, nodo2, weight=connessione.peso)

    def getConnessi(self, v0, v1):
        percorso=[]
        connessa = nx.node_connected_component(self.grafo, v0)
        if v1 in connessa:
            percorso=nx.dijkstra_path(self.grafo, v0, v1)
        return percorso
    def getTuttiConnessi(self,v0):
        raggiungibili=[]
        for nodi in nx.dfs_tree(self.grafo,v0):
            raggiungibili.append(nodi)
        return raggiungibili

    def getBestPath(self, limite, nodoIniziale, nodoFinale):
        self._soluzione = []
        self._costoMigliore = 0
        parziale = [nodoIniziale]
        self._ricorsione(parziale, limite, nodoFinale)
        return self._costoMigliore, self._soluzione

    def _ricorsione(self, parziale, limite, nodoFinale):
        if len(parziale)-1 <=limite and parziale[-1]==nodoFinale:
            if self.peso(parziale)>self._costoMigliore:
                self._soluzione = copy.deepcopy(parziale)
                self._costoMigliore = self.peso(parziale)

        if len(parziale) -1< limite and nodoFinale not in parziale:
            for n in self.grafo.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, limite, nodoFinale)
                    parziale.pop()



    def peso(self, listaNodi):
        pesoTot = 0
        for i in range(0, len(listaNodi) - 1):
            pesoTot += self.grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]
        return pesoTot
