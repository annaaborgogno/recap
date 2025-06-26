#CHIAMATA DAO PER LISTA SEMPLICE NO PARAMETRI

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

#CHIAMATA DAO PER NODI E CONNESSIONI
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

#CHIAMATA DAO PER PESO DA UTILIZZARE SE IL GRAFO è PESATO E NON SI RIESCE
#A INSERIRE IL PESO NELLE CONNESSIONI
  
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


    # per calcolare la distanza tra due circuiti
        """SELECT 
          c1.name AS circuito1,
          c2.name AS circuito2,
          6371 * ACOS(
            COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat)) *
            COS(RADIANS(c2.lng) - RADIANS(c1.lng)) +
            SIN(RADIANS(c1.lat)) * SIN(RADIANS(c2.lat))
          ) AS distanza_km
        FROM circuits c1
        JOIN circuits c2 ON c1.name = 'Monza' AND c2.name = 'Silverstone';"""

    # per calcolare i circuiti entro 1000 km da Monza
        """SELECT c2.name,
                  c2.country,
                  6371 * ACOS(
                    COS(RADIANS(c1.lat)) * COS(RADIANS(c2.lat)) *
                    COS(RADIANS(c2.lng) - RADIANS(c1.lng)) +
                    SIN(RADIANS(c1.lat)) * SIN(RADIANS(c2.lat))
                  ) AS distanza_km
                FROM circuits c1
                JOIN circuits c2 ON c1.name = 'Monza' AND c1.circuitId != c2.circuitId
                HAVING distanza_km < 1000
                ORDER BY distanza_km;"""

    #Arco team A → team B se A ha fatto più punti di B nella stessa gara
        """SELECT cr1.constructorId AS vincente,
                  cr2.constructorId AS sconfitto,
                  COUNT(*) AS volte_superato
                FROM constructorresults cr1
                JOIN constructorresults cr2 ON cr1.raceId = cr2.raceId 
                  AND cr1.constructorId != cr2.constructorId
                  AND cr1.points > cr2.points
                GROUP BY cr1.constructorId, cr2.constructorId;"""

    #Arco a → b se a ha finito una gara davanti a b
        """SELECT r1.driverId AS vincente,
              r2.driverId AS sconfitto,
              COUNT(*) AS volte_sorpassato
            FROM results r1
            JOIN results r2 ON r1.raceId = r2.raceId 
              AND r1.positionOrder < r2.positionOrder
              AND r1.driverId != r2.driverId
            GROUP BY r1.driverId, r2.driverId;"""

    #due team partecipano alla stessa gara
        """SELECT 
          LEAST(c1.constructorId, c2.constructorId) AS team1,
          GREATEST(c1.constructorId, c2.constructorId) AS team2,
          COUNT(DISTINCT c1.raceId) AS gare_insieme
        FROM constructorresults c1
        JOIN constructorresults c2 ON c1.raceId = c2.raceId AND c1.constructorId != c2.constructorId
        GROUP BY LEAST(c1.constructorId, c2.constructorId), GREATEST(c1.constructorId, c2.constructorId);"""

    #due piloti che hanno corso nella stessa gara
    """SELECT LEAST(r1.driverId, r2.driverId) AS driver1,
          GREATEST(r1.driverId, r2.driverId) AS driver2,
          COUNT(DISTINCT r1.raceId) AS gare_insieme
        FROM results r1
        JOIN results r2 ON r1.raceId = r2.raceId AND r1.driverId != r2.driverId
        GROUP BY LEAST(r1.driverId, r2.driverId), GREATEST(r1.driverId, r2.driverId);"""

    #in quale team corre un pilota
    """SELECT r.driverId, r.constructorId, c.name AS team_name
        FROM results r
        JOIN constructors c ON r.constructorId = c.constructorId
        WHERE r.driverId = 1;"""


#Alla pressione del bottone “Seleziona stagione”, creare un grafo con le seguenti caratteristiche: i vertici del grafo rappresentano le gare disputate
#nella stagione selezionata; gli archi del grafo sono non orientati e pesati, ed il peso rappresenta il numero di piloti che hanno corso in entrambe le gare adiacenti all’arco, e che so

@staticmethod
def getEdges(year):
    cnx = DBConnect.get_connection()
    cursor = cnx.cursor(dictionary=True)
    query = """select LEAST(ra1.raceId, ra2.raceId) as raceId1, GREATEST(ra1.raceId, ra2.raceId) as raceId2, COUNT(*) AS peso
                   from races ra1, results re1, races ra2, results re2
                   where ra1.`year` = %s 
                   and ra1.`year` = ra2.`year`
                   and ra1.raceId = re1.raceId 
                   and ra2.raceId = re2.raceId
                   and ra1.raceId != ra2.raceId
                   and re1.driverId = re2.driverId
                   and re1.statusId = 1
                   and re2.statusId = 1
                   group by LEAST(ra1.raceId, ra2.raceId), GREATEST(ra1.raceId, ra2.raceId)
                   order by peso desc"""
    cursor.execute(query, (year,))

    res = []
    for row in cursor:
        res.append(Edge(**row))
    cursor.close()
    cnx.close()
    return res