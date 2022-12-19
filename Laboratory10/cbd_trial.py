import rdflib

if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(r"./data/food.rdf")
    recursive_terms = []
    for subj, pred, obj in graph.triples((None, None, None)):
        if graph.qname(pred) == 'owl:hasValue' or graph.qname(pred) == 'owl:onProperty':
            if type(obj) is not rdflib.BNode:
                term = [subj, graph.qname(pred), graph.qname(obj)]
                generator = graph.subject_predicates(subj)
                for subj, pred in generator:
                    while type(subj) is rdflib.BNode:
                        term.insert(0, graph.qname(pred))
                        term.insert(0, subj)
                        for subj1, pred1 in graph.subject_predicates(subj):
                            subj, pred = subj1, pred1
                            break
                    term.insert(0, graph.qname(pred))
                    term.insert(0, graph.qname(subj))
                recursive_terms += [term]
    for term in recursive_terms:
        print(term)
