import rdflib
import pprint
import nltk
from nltk.corpus import wordnet
import questionaire


if __name__ == '__main__':
    graph = rdflib.Graph()
    graph.parse(r"./data/food.rdf")
    questionaire = questionaire.Questionaire(graph)
    print("Length: ", len(graph))
    for subj, pred, obj in graph.triples((None, None, None)):
        if type(subj) is rdflib.BNode or type(obj) is rdflib.BNode:
            continue
        printable_subj = graph.qname(subj) if type(subj) is rdflib.URIRef else subj
        printable_pred = graph.qname(pred) if type(pred) is rdflib.URIRef else pred
        printable_obj = graph.qname(obj) if type(obj) is rdflib.URIRef else obj
        print('{} -- {} -- {}'.format(printable_subj, printable_pred, printable_obj))

    while True:
        question, question_triple = questionaire.generate_question()
        answer = input(question)
        correct, found = questionaire.validate_question_answer(question_triple, answer)
        if correct:
            print('Correct answer')
        else:
            print('Wrong answer, correct is ' + (found if type(found) is not rdflib.URIRef else questionaire.graph.qname(found)))
        should_terminate = input('Terminate program?(Y/n)')
        if should_terminate.lower() == 'y':
            break

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
