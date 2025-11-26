import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """

        "PRIMO PASSAGGIO: CONTROLLARE CHE L'INPUT SIA CORRETTO"
        valore = self._view.guadagno_medio_minimo.value.strip()
        if valore == "":
            self._view.show_alert('inserire un valore numerico per la soglia!')
            return


        try:
            threshold = float(valore)
        except ValueError:
            self._view.show_alert('il valore inserito non è un valore numero!')
            return


        "SECONDO PASSAGGIO: COSTRUZIONE DEL GRAFO E AGGIORNAMENTO DELL'UI"
        self._model.costruisci_grafo(threshold)

        self._view.lista_visualizzazione.controls.clear()

        #numero nodi e tratte
        n_nodi = self._model.get_num_nodes()
        n_tratte = self._model.get_num_edges()

        self._view.lista_visualizzazione.controls.append(ft.Text(f'Numero di Hub: {n_nodi}',size = 18,
                                                                 weight=ft.FontWeight.BOLD))
        self._view.lista_visualizzazione.controls.append(ft.Text(f'Numero di Tratte: {n_tratte}',size = 18,
                                                                 weight=ft.FontWeight.BOLD))


        #creo una riga vuota per maggior chiarezza nella stampa del risultato
        self._view.lista_visualizzazione.controls.append(ft.Text(""))


        #lista delle tratte

        for h1,h2,valore in self._model.get_all_edges():
            riga = ft.Text(f'{h1.nome} ({h1.stato} --> {h2.nome} ({h2.stato})'
                           f'guadagno medio per spedizione: {valore:.2f} euro')

            self._view.lista_visualizzazione.controls.append(riga)

        self._view.update()
