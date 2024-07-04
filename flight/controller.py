from datetime import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None
        self._choiceAeroportoA = None
        self.grafo=None

    def handelAnalizza(self, e):
        minimoCompagnie=self._view._txtInNumC.value
        if minimoCompagnie=="":
            self._view.create_alert("Inserire il numero minimo di compagnie")
            return
        try:
            minimoCompagnieInt=int(minimoCompagnie)
        except ValueError:
            self._view.create_alert("Il minimo numero di compagnie deve essere un intero")
            return
        self.grafo = self._model.creaGrafo(minimoCompagnieInt)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view._txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        self._view._ddAeroportoP.disabled=False
        self._view._ddAeroportoA.disabled=False
        self._view._btnConnessi.disabled=False
        self._view._btnPercorso.disabled = False
        self.fillDD()
        self._view._txtInNumTratte.disabled=False
        self._view._btnCercaItinerario.disabled=False
        self._view.update_page()


    def handleConnessi(self, e):
        if self._choiceAeroportoP is None:
            self._view.create_alert("Attenzione aeroporto di partenza non selezionato")
            return
        self._view._txt_result.controls.append(ft.Text(f"Raggiungibili da {self._choiceAeroportoP}"))
        listaNodi = self._model.getTuttiConnessi(self._choiceAeroportoP)
        for nodo in listaNodi:
            self._view._txt_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()

    def handleTestConnessione(self, e):
        if self._choiceAeroportoP is None:
            self._view.create_alert("Attenzione aeroporto di partenza non selezionato")
            return
        if self._choiceAeroportoA is None:
            self._view.create_alert("Attenzione aeroporto di arrivo non selezionato")
            return
        percorso = self._model.getConnessi(self._choiceAeroportoP,self._choiceAeroportoA)
        if percorso==[]:
            self._view._txt_result.controls.append(ft.Text(f"Percorso non presente"))
        else:
            for i in range(0, len(percorso)-1):
                self._view._txt_result.controls.append(ft.Text(f"DA {percorso[i]} a {percorso[i+1]}"))
        self._view.update_page()



    def handleCercaItinerario(self,e):
        massimoTratte = self._view._txtInNumTratte.value
        if massimoTratte == "":
            self._view.create_alert("Inserire il numero massimo di tratte")
            return
        try:
            massimoTratteInt = int(massimoTratte)
        except ValueError:
            self._view.create_alert("Il massimo numero di tratte deve essere un intero")
            return
        costo, listaNodi = self._model.getBestPath(massimoTratteInt,self._choiceAeroportoP,self._choiceAeroportoA)
        self._view._txt_result.controls.append(ft.Text(f"La soluzione migliore è costituita da {costo} voli totali disponibili sul percorso"))
        for nodo in listaNodi:
            self._view._txt_result.controls.append(ft.Text(f"{nodo}"))
        self._view.update_page()


    def fillDD(self):
        for n in self.grafo.nodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=n,
                                                                       text=n, on_click=self.readDDAeroportoP
                                                                       ))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=n,
                                                                       text=n, on_click=self.readDDAeroportoA
                                                                       ))

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        else:
            self._choiceAeroportoP = e.control.data

    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choiceAeroportoA = None
        else:
            self._choiceAeroportoA = e.control.data
