import nltk
from nltk.corpus import wordnet

if __name__ == '__main__':
    word = input('Introduceti un cuvant pentru a fi cautat in wordnet: ')
    syn_arr = wordnet.synsets(word)
    # print(wordnet.synonyms(word))
    print('Cuvantul apartine urmatoarelor synseturi:')
    for synset in syn_arr:
        print(synset.name())
        # print([str(lemma.name()) for lemma in synset.lemmas()])


def get_synset(word):
    syn_arr = wordnet.synsets(word)
    return syn_arr

