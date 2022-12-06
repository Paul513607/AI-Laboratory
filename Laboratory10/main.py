import rdflib
import pprint


if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(r"./data/food.rdf")
    print("Length: ", len(graph))
    for stmt in graph:
        pprint.pprint(stmt)
