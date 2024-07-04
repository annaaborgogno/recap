
//VALIDAZIONE CAMPI:

//dropdown
porzione=self._view.ddporzione.value
        if porzione is None:
            self._view.create_alert("Selezionare un tipo di porzione")
            return
        dizio=self._model.analisi(porzione)

//textfield:
calorie=self._view.txtcalorie.value
if calorie=="":
    self._view.create_alert("Inserire un valore numerico per le calorie")
    return
grafo = self._model.creaGrafo( int(calorie)) 

//NB: in entrambi i casi il cast del valore (se necessario) va fatto dopo altrimenti da errore


/RIMPIRE IL DROPDOWN -> ricordati di chiamare self._controller.fillDD() NELLA VIEW DOPO 
//DOPO LA CREAZIONE DEL DD

    def fillDD(self):
        ann="201"
        for i in range(5,9):
            anno=ann+str(i)
            self._view.dd_anno.options.append(ft.dropdown.Option(
                               text=anno))

//RIEMPIRE IL IL DD DA UNA COLONNA/TABELLA DEL DATABASE
//NB se nazioni fosse costituita da Oggetti bisogna accertarsi che il metodo
/str stampa ciò che desideriamo inserire nel DD

nazioni=self._model.getNazioni
for nazione in nazioni:
    self._view.dd_nazione.options.append(ft.dropdown.Option(
        text=nazione))


//CREA GRAFO -> Ricordarsi la validazione dei campi se necessario

    def handle_grafo(self, e):
        nazione = self._view.dd_nazione.value
        if nazione is None:
            self._view.create_alert("Selezionare una Nazione")
            return
        anno = self._view.dd_anno.value
        if anno is None:
            self._view.create_alert("Selezionare un Anno")
            return
        nProdotti= self._view.txt_prodotti.value
        if nProdotti == "":
            self._view.create_alert("Inserire un valore numerico per il numero di prodotti in comune")
            return
        grafo = self._model.creaGrafo(nazione, int(anno), int(nProdotti))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        self._view.update_page()


  
  //CREATE ALERT:
    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

//UN DD CHE SI POPOLA AL CLICK SULL ALTRO
    def fillDDanno(self):
        anni=self._model.getAnni
        for anno in anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(
                text=anno))

    def fillDDforme(self,e):
        self._view.dd_shape.options=[]
        forme=self._model.getForme(int(self._view.dd_anno.value))
        for forma in forme:
            self._view.dd_shape.options.append(ft.dropdown.Option(
                text=forma))
        self._view.update_page()

SU VIEW:
 self.dd_anno=ft.Dropdown(label="Anno", on_change=self._controller.fillDDforme)
        self.dd_shape=ft.Dropdown(label="Shape")
        self._controller.fillDDanno()


//GESTIONE INPUT:
 def fillDD(self):
        allNodes = self._model.getAllNodes()
        for n in allNodes:
            self._view._ddAeroportoP.options.append(
                ft.dropdown.Option(
                    data= n,
                    on_click=self.readDDAeroportoP,
                    text=n.AIRPORT
                ))
            self._view._ddAeroportoA.options.append(
                ft.dropdown.Option(
                    data=n,
                    on_click=self.readDDAeroportoA,
                    text=n.AIRPORT
                ))

    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        else:
            self._choiceAeroportoP = e.control.data
        print(f"readDDAeroportoP called -- {self._choiceAeroportoP}")

//GESTIONE ERRORI:
        soglia = self._view._txtInDistanza.value
        if soglia == "":
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Distanza non inserita."))    //oppure create alert
            self._view.update_page()
            return

        try:
            sogliaFloat = float(soglia)
        except ValueError:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Attenzione, soglia inserita non numerica."))
            self._view.update_page()
            return
//CONTROLLER CON GESTIONE ERRORI
  import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        d=self._view._txtInDurata.value
        if d=="":
            self._view.create_alert("Inserire una durata in minuti")
            return
        try:
            dInt=int(d)
        except ValueError:
            self._view.create_alert("INSERIRE UN INTERO")
            return
        grafo = self._model.creaGrafo(dInt)
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        for n in grafo:
            self._view._ddAlbum.options.append(ft.dropdown.Option(data=n,
                            text = n.Title, on_click=self.getSelectedAlbum
                          ))

        self._view.update_page()

    def getSelectedAlbum(self, e):
        if e.control.data is None:
            self._choiceAlbum = None
        else:
            self._choiceAlbum = e.control.data



    def handleAnalisiComp(self, e):
        if self._choiceAlbum is None:
            self._view.create_alert("Attenzione album non selezionato")
            return
        dimensione,durata=self._model.getAnalisi(self._choiceAlbum)
        self._view.txt_result.controls.append(ft.Text(f"Componente conenssa -  {self._choiceAlbum} "
                                                      f"di dimensione {dimensione} e durata complessiva"
                                                      f"pari a "
                                                      f"{durata}"))

        self._view.update_page()

//NB IN QUESTO MODO L'ALBUM SELEZIONATO GIA' E' L'OGGETTO INTERO E NON SERVE L'IDMAP
//NEL MODEL

//disabilitare e attivare bottoni:
        self._txtInNumTratte = ft.TextField(label="Num Tratte Max", width=200,
                                                     disabled=True)
//PER ATTIVARE:
        self._view._txtInNumTratte.disabled = False
//pul54
    self._view.txt_result.controls.clear()
