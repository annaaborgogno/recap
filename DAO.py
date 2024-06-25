//CHIAMATA DAO PER LISTA SEMPLICE NO PARAMETRI

@staticmethod
    def getNazione():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct gr.Country as nazione
from go_retailers gr"""


        cursor.execute(query)

        for row in cursor:
            result.append(row["nazione"])

        cursor.close()
        conn.close()
        return result

//CHIAMATA DAO PER NODI E CONNESSIONI
 @staticmethod
    def getNodi():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct *
                    from state s """

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct n.state1 as v1, n.state2 as v2
                    from neighbor n """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(**row))

        cursor.close()
        conn.close()
        return result

//CHIAMATA DAO PER PESO DA UTILIZZARE SE IL GRAFO è PESATO E NON SI RIESCE
//A INSERIRE IL PESO NELLE CONNESSIONI
  
    @staticmethod
    def getPeso(forma,anno,stato1,stato2):
        conn = DBConnect.get_connection()

        result = 0

        cursor = conn.cursor(dictionary=True)
        query = """select count(*) as peso
                    from sighting s 
                    where s.shape=%s and year(s.`datetime`)=%s and (s.state=%s or s.state=%s)
                     """

        cursor.execute(query,(forma,anno,stato1,stato2,))

        for row in cursor:
            result=row["peso"]

        cursor.close()
        conn.close()
        return result

