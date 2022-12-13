import random

import rdflib


class Questionaire:
    graph: rdflib.Graph
    triples: list

    def __init__(self, graph: rdflib.Graph):
        self.graph = graph
        self.triples = []
        for subj, pred, obj in graph.triples((None, None, None)):
            if type(subj) is rdflib.BNode or type(obj) is rdflib.BNode:
                continue
            self.triples.append((subj, pred, obj))

    def generate_question(self):
        triple_idx = random.randint(0, len(self.triples))
        question_idx = random.randint(0, 2)
        subj, pred, obj = self.triples[triple_idx]
        question = ''
        question_triple: tuple
        if question_idx == 0:
            question = 'Cine este in relatia {} cu {} in partea dreapta: ' \
                .format(self.graph.qname(pred), self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj)
            question_triple = (None, pred, obj)
        elif question_idx == 1:
            question = 'Ce relatie este intre {} si {}: ' \
                .format(self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj,
                        self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj)
            question_triple = (subj, None, obj)
        elif question_idx == 2:
            question = 'Cine este in relatia {} cu {} in partea stanga: ' \
                .format(self.graph.qname(pred), self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj)
            question_triple = (subj, pred, None)
        return question, question_triple

    def validate_question_answer(self, question_triple, answer):
        found = None

        def find_answer(generator):
            for x in generator:
                if answer == (self.graph.qname(x) if type(x) is rdflib.URIRef else x):
                    return x
            return None

        if question_triple[0] is None:
            subj_generator = self.graph.subjects(predicate=question_triple[1], object=question_triple[2])
            found = find_answer(subj_generator)
        elif question_triple[1] is None:
            pred_generator = self.graph.predicates(subject=question_triple[0], object=question_triple[2])
            found = find_answer(pred_generator)
        elif question_triple[2] is None:
            found = self.graph.value(subject=question_triple[0], predicate=question_triple[1], default=None, any=True)

        if type(found) is rdflib.URIRef:
            return answer == self.graph.qname(found), found
        else:
            return answer == found, found
