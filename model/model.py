from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()
        self.hub_dictonary = None
        self.tratte_valide = None

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        self.G.clear()

        "carico tutti hub da database"
        self.hub_dictonary = DAO.recupera_tutti_gli_hub()

        "aggiungo i nodi al grafo"
        for hub in self.hub_dictonary.values():
            self.G.add_node(hub)

        """recuperare tutte le tratte aggregate"""
        tratte_aggregate = DAO.recupera_tratte_aggregate()
        self.tratte_valide = []

        "bisogna aggiungere al grafo solo le tratte che rispettano la condizione"

        for tratta in tratte_aggregate:
            guadagno_medio = tratta['guadagno_medio']

            if guadagno_medio >= threshold:
                hub_1 = self.hub_dictonary[tratta['hub1']]
                hub_2 = self.hub_dictonary[tratta['hub2']]

                self.G.add_edge(hub_1, hub_2, weight = guadagno_medio)
                self.tratte_valide.append((hub_1,hub_2, guadagno_medio))


    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return self.G.edges()

