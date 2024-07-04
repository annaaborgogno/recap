
//stato
from dataclasses import dataclass

@dataclass
class Stato:
    id:str
    Name:str
    Capital:str
    Lat:float
    Lng:float
    Area:int
    Population:int
    Neighbors:str


    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.Name}"


//avvistamenti 
from dataclasses import dataclass

@dataclass
class Avvistamento:
    id: int
  datetime:str
  city:str
  state:str
  country:str
  shape:str
  duration:int
  duration_hm:str
  comments:str
  date_posted:str
  latitude:float
  longitude:float


    def __hash__(self):
        return hash(self.id)
        
//I vertici del grafo saranno gli stati americani (o meglio, il sottoinsieme di stati
in cui vi è stato almeno un avvistamento nell'anno)

        select distinct s.state as stato
        from sighting s 
        where s.country ='us' and year(s.`datetime`) =%s
        group by s.state 
        having count(s.id)>0

//Gli archi del grafo rappresentano l'ordine temporale degli avvistamenti.
In particolare, ci dovrà essere un arco tra lo stato A e lo stato B se almeno un
avvistamento in B è temporalmente successivo ad almeno un avvistamento in A
(sempre nell'anno di riferimento).

         select count(*) as peso
        from (select s.`datetime` as d1
        from sighting s 
        where s.country ='us' and s.state =%s
        and year(s.`datetime`)=%s) as t1,
        (select s.`datetime` as d2
        from sighting s 
        where s.country ='us' and s.state =%s
        and year(s.`datetime`)=%s) as t2
        where d1<d2

//Facendo click sul bottone CREA GRAFO, creare un grafo semplice, pesato e non orientato, i cui vertici siano
tutti gli stati presenti nella tabella “state”. Un arco collega due stati solo se sono confinanti, come indicato
nella tabella “neighbor”.

        select distinct *
         from state s

        select distinct n.state1 as v1, n.state2 as v2
        from neighbor n 
        where n.state1<n.state2

//Il peso dell’arco viene calcolato come il numero di avvistamenti che hanno la stessa forma (colonna “shape”)
selezionata dal menù a tendina Forma, e che si sono verificati nello stesso anno selezionato (da estrarre dalla
colonna “datetime”), nei due stati considerati.

        select count(*) as peso
        from sighting s 
        where s.shape=%s and year(s.`datetime`)=%s and (s.state=%s or s.state=%s)

