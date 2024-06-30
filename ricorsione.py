//RICORSIONE CON UN NODO DI PARTENZA CON MASSIMO PESO TOTALR E VINCOLO SUL NUMERO DI ELEMENTI

    def getBestPath(self, nodoInizialeString, limite):
        self._soluzione = []
        self._costoMigliore = 0
        nodoIniziale = self._idMap[int(nodoInizialeString.split("-")[0])]
        parziale = [nodoIniziale]
        self._ricorsione(parziale,limite)
        return self._costoMigliore,self._soluzione

    def _ricorsione(self, parziale, limite):
        if self.peso(parziale) <= limite:
            if len(parziale)>self._costoMigliore:
                self._soluzione=copy.deepcopy(parziale)
                self._costoMigliore=len(parziale)

            for n in self.grafo.neighbors(parziale[-1]):
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, limite)
                    parziale.pop()
    def peso(self, listaNodi):
        pesoTot = 0
        for i in range(0, len(listaNodi) - 1):
            pesoTot += self.grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]
        return pesoTot

//RICORSIONE CON NODO DI PARTENZA E NODO FINALE CON UN VINCOLO E MASSIMIZZAZIONE DIVERSA (NO PESO)

 def getBestPath(self, limite,nodoInizialeStringa, nodoFinaleStringa):
        self._soluzione = []
        self._costoMigliore = 0
        nodoIniziale = self._idMapNome[nodoInizialeStringa]
        nodoFinale=self._idMapNome[nodoFinaleStringa]
        parziale = [nodoIniziale]
        self._ricorsione(parziale, limite, nodoFinale)
        return self._costoMigliore, self._soluzione

    def _ricorsione(self, parziale, limite, nodoFinale):
        if self.pesoAmmissibile(parziale,limite) and parziale[-1] == nodoFinale:
            if self.count(parziale) > self._costoMigliore:
                self._soluzione = copy.deepcopy(parziale)
                self._costoMigliore = self.count(parziale)

        for n in self.grafo.neighbors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, limite,nodoFinale)
                parziale.pop()

    def pesoAmmissibile(self, listaNodi,limite):
        ammissibile=True
        for i in range(0, len(listaNodi) - 1):
            if self.grafo[listaNodi[i]][listaNodi[i + 1]]["weight"]<limite:
                ammissibile=False
        return ammissibile
    def count(self, listaNodi):
        bilancioRiferimento=self.bilancio(listaNodi[0])
        contatore=0
        for nodo in listaNodi:
            if self.bilancio(nodo)>bilancioRiferimento:
                contatore+=1
        return contatore
