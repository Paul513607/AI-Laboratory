import random

import rdflib
from wordnet_tasks import get_synset


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

    def get_a_synonym(self, word):
        syn_arr = get_synset(word)
        prob = random.randint(0, 100)
        if prob < 50 or len(syn_arr) == 0:
            return word
        else:
            for synset in syn_arr:
                if synset.name().split(".")[0] != word.lower():
                    return synset.name().split(".")[0]
            return word

    def generate_question(self):
        triple_idx = random.randint(0, len(self.triples))
        question_idx = random.randint(0, 2)
        subj, pred, obj = self.triples[triple_idx]
        question = ''
        question_triple: tuple = (None, None, None)
        if question_idx == 0:
            pred = self.graph.qname(pred)
            obj = self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj
            #pred1 = pred if ":" not in pred else pred.split(":")[1]
            #obj1 = obj if ":" not in obj else obj.split(":")[1]
            #pred1 = self.get_a_synonym(pred1)
            #obj1 = self.get_a_synonym(obj1)
            question = 'Cine este in relatia {} cu {} in partea dreapta: ' \
                .format(pred, obj)
            question_triple = (None, pred, obj)
        elif question_idx == 1:
            subj = self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj
            obj = self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj
            #subj1 = subj if ":" not in subj else subj.split(":")[1]
            #obj1 = obj if ":" not in obj else obj.split(":")[1]
            #subj1 = self.get_a_synonym(subj1)
            #obj1 = self.get_a_synonym(obj1)
            question = 'Ce relatie este intre {} si {}: ' \
                .format(subj, obj)
            question_triple = (subj, None, obj)
        elif question_idx == 2:
            subj = self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj
            pred = self.graph.qname(pred)
            #subj1 = subj if ":" not in subj else subj.split(":")[1]
            #pred1 = pred if ":" not in pred else pred.split(":")[1]
            #subj1 = self.get_a_synonym(subj1)
            #pred1 = self.get_a_synonym(pred1)
            question = 'Cine este in relatia {} cu {} in partea stanga: ' \
                .format(pred, subj)
            question_triple = (subj, pred, None)
        return question, question_triple

    def validate_question_answer(self, question_triple, answer):
        found = None

        def find_answer(generator):
            wrong_answer = None
            for x in generator:
                if answer == (self.graph.qname(x) if type(x) is rdflib.URIRef else x):
                    return x
                wrong_answer = x
            return wrong_answer

        if question_triple[0] is None:
            subj_generator = self.graph.subjects(predicate=question_triple[1], object=question_triple[2])
            for x in subj_generator:
                print("AAAAAAAA: ", x)
            found = find_answer(subj_generator)
        elif question_triple[1] is None:
            pred_generator = self.graph.predicates(subject=question_triple[0], object=question_triple[2])
            found = find_answer(pred_generator)
            if found is not None:
                found = found.split(":")[1]
        elif question_triple[2] is None:
            found = self.graph.value(subject=question_triple[0], predicate=question_triple[1], default=None, any=True)

        if found is None:
            found = 'None'
        if type(found) is rdflib.URIRef:
            return answer == self.graph.qname(found), found
        else:
            return answer == found, found
