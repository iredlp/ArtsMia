from model.model import Model

mdl=Model()
mdl.buildGraph()
print(f" Il Grafo creato contiene {mdl.getNumNodes()}nodi e"
      f"{mdl.getNumEdges()}archi.")

mdl.getInfoCompConnessa(1224)
