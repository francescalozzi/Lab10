from database.DB_connect import DBConnect
from model.hub import Hub


class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    """

    @staticmethod
    def recupera_tutti_gli_hub():
        "dizionario con tutti gli hub del database"

        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictonary=True)

        query = 'SELECT * FROM hub'
        cursore.execute(query)
        righe = cursore.fetchall()

        dizionario_hub = {}

        for riga in righe:
            hub = Hub(id = riga['id'], codice = riga['codice'], nome = riga['nome'],
                      citta = riga['citta'], stato=riga['stato'],
                      latitudine=riga['latitudine'], longitudine=riga['longitudine'])

            dizionario_hub[riga['id']] = hub

        cursore.close()
        conn.close()
        return dizionario_hub

    @staticmethod
    def recupera_tratte_aggregate():
        """ lista delle tratte aggregate nelle due direzioni,
        con somma di valori, numero di spedizioni e guadagno medio"""

        conn = DBConnect.get_connection()
        cursore = conn.cursor(dictonary=True)

        query = """SELECT 
                        LEAST(id_hub_origine, id_hub_destinazione) AS hub1,
                        GREATEST(id_hub_origine, id_hub_destinazione) AS hub2,
                        SUM(valore_merce) AS somma_valori,
                        COUNT(*) AS numero_spedizioni,
                        SUM(valore_merce)/COUNT(*) AS guadagno_medio
                    FROM spedizione
                    GROUP BY hub1, hub2"""


        cursore.execute(query)
        lista_tratte = cursore.fetchall()

        cursore.close()
        conn.close()
        return lista_tratte
