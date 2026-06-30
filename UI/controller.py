import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafp correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(
            f"Il grafo contiene {self._model.getNumNodes()} nodi e{self._model.getNumEdges()} archi."))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False

        self._view.update_page()

    def handleCompConnessa(self,e):
        txtIdOggetto=self._view.txtIdOggetto.value

        try:
            idOggetto=int(txtIdOggetto)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore nel campo id", color= "red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idOggetto):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, l'id inserito non è presente nel grafo", color="orange"))
            self._view.update_page()
            return

        sizeComConn=self._model.getInfoCompConnessa(idOggetto)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa contenente l'oggetto con  id {idOggetto} è composta di{sizeComConn} NODI", color="verde"))
        self._view.update_page()




