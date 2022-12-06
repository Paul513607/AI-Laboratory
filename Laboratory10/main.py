import rdflib
import pprint
import nltk
from nltk.corpus import wordnet


if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(r"./data/food.rdf")
    print("Length: ", len(graph))
    for stmt in graph:
        pprint.pprint(stmt)

    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    syn_arr = wordnet.synsets('room')
    print(syn_arr[0].definition())
