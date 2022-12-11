import rdflib
import pprint
import nltk
from nltk.corpus import wordnet


if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(r"./data/food.rdf")
    print("Length: ", len(graph))
    for subj, pred, obj in graph:
        printable_subj = graph.qname(subj) if type(subj) is rdflib.URIRef else subj
        printable_pred = graph.qname(pred) if type(pred) is rdflib.URIRef else pred
        printable_obj = graph.qname(obj) if type(obj) is rdflib.URIRef else obj
        print('{} -- {} -- {}'.format(printable_subj, printable_pred, printable_obj))

    # print(graph.serialize(format='turtle'))

    # graph.print()
    # for subject, predicate, other in graph.triples((None, None, None)):
    #     print(subject, '--', predicate, '--', other)
    # for stmt in graph:
    #     pprint.pprint(stmt)

    # nltk.download('wordnet')
    # nltk.download('omw-1.4')
    # syn_arr = wordnet.synsets('room')
    # print(syn_arr[0].definition())
