import rdflib
import nltk
from nltk.corpus import wordnet


if __name__ == '__main__':
    print("Hello world!")
    #nltk.download('wordnet')
    #nltk.download('omw-1.4')
    syn_arr = wordnet.synsets('room')
    print(syn_arr[2].definition())