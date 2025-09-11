

from corpus_file_reader import CorpusFileReader

_file = "/Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK/22-232_231-S.txt"
cfp = CorpusFileReader(_file)

print("FILE: " + _file)

line = cfp.next_line()

import spacy

nlp = spacy.load("en_core_web_lg")

while line:
    print("---> " + line)
    doc = nlp(line)
    for sent in doc.sents:
        for word in sent:
            #print("   " + word + " | " + word.dep_)
            print(word, word.dep_, word.tag_, word.pos_, word.morph)
    line = cfp.next_line()




