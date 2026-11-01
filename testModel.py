from model.model import Model

mymodel=Model()
mymodel.buildGraph('pop')
print(f"Ci sono {mymodel.getNumNodes()} nodi e {mymodel.getNumEdges()} archi")