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
        question_idx = 1
        subj, pred, obj = self.triples[triple_idx]
        question = ''
        question_triple: tuple = (None, None, None)
        if question_idx == 0:
            pred1 = self.graph.qname(pred)
            obj1 = self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj
            pred1 = pred1 if ":" not in pred1 else pred1.split(":")[1]
            pred1 = pred1 if "#" not in pred1 else pred1.split("#")[1]
            obj1 = obj1 if ":" not in obj1 else obj1.split(":")[1]
            pred1 = self.get_a_synonym(pred1)
            obj1 = self.get_a_synonym(obj1)
            question = 'Cine este in relatia {} cu {} in partea dreapta: ' \
                .format(pred1, obj1)
            question_triple = (None, pred, obj)
        elif question_idx == 1:
            subj1 = self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj
            obj1 = self.graph.qname(obj) if type(obj) is rdflib.URIRef else obj
            subj1 = subj1 if ":" not in subj1 else subj1.split(":")[1]
            obj1 = obj1 if ":" not in obj1 else obj1.split(":")[1]
            subj1 = self.get_a_synonym(subj1)
            obj1 = self.get_a_synonym(obj1)
            question = 'Ce relatie este intre {} si {}: ' \
                .format(subj1, obj1)
            question_triple = (subj, None, obj)
        elif question_idx == 2:
            subj1 = self.graph.qname(subj) if type(subj) is rdflib.URIRef else subj
            pred1 = self.graph.qname(pred)
            subj1 = subj1 if ":" not in subj1 else subj1.split(":")[1]
            pred1 = pred1 if ":" not in pred1 else pred1.split(":")[1]
            pred1 = pred1 if "#" not in pred1 else pred1.split("#")[1]
            subj1 = self.get_a_synonym(subj1)
            pred1 = self.get_a_synonym(pred1)
            question = 'Cine este in relatia {} cu {} in partea stanga: ' \
                .format(pred1, subj1)
            question_triple = (subj, pred, None)
        return question, question_triple

    def is_same(self, answer, found):
        for synset in get_synset(found):
            if answer.lower() == synset.name().split(".")[0]:
                return True
            hypernyms = synset.hypernyms()
            for hypernym in hypernyms:
                if answer.lower() == hypernym.name().split(".")[0]:
                    print("Validated as hypernym")
                    return True
            meronyms = synset.part_meronyms()
            for meronym in meronyms:
                if answer.lower() == meronym.name().split(".")[0]:
                    print("Validated as meronym")
                    return True
        return False

    def validate_question_answer(self, question_triple, answer):
        found = None

        def find_answer(generator):
            wrong_answer = None
            for x in generator:
                y = self.graph.qname(x) if type(x) is rdflib.URIRef else x
                y = y if ":" not in y else y.split(":")[1]
                y = y if "#" not in y else y.split("#")[1]
                y_synset_arr = get_synset(y.lower())
                for synset in y_synset_arr:
                    name = synset.name()
                    print(answer.lower(), ' ---------- ', name.split(".")[0])
                    if answer.lower() == name.split(".")[0]:
                        return y
                wrong_answer = y
            return wrong_answer

        if question_triple[0] is None:
            subj_generator = self.graph.subjects(predicate=question_triple[1], object=question_triple[2])
            found = find_answer(subj_generator)
        elif question_triple[1] is None:
            pred_generator = self.graph.predicates(subject=question_triple[0], object=question_triple[2])
            found = find_answer(pred_generator)
            if found is not None:
                found = found if ":" not in found else found.split(":")[1]
        elif question_triple[2] is None:
            found = self.graph.value(subject=question_triple[0], predicate=question_triple[1], default=None, any=True)

        if type(found) is rdflib.URIRef:
            return self.is_same(answer, self.graph.qname(found)), found
        else:
            return self.is_same(answer, found), found
