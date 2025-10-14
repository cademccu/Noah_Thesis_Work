
# testing individual sentence dependancies

import spacy

nlp = spacy.load("en_core_web_lg")




lines = [
    "for his arrival",
    "drinking too much milk",
    "to climb really hard",
    "if he knows the answer",
    "What this mean, Because you know, culture, that's mean you have to see your manager"
]

for line in lines:
    print("---> " + line)
    doc = nlp(line)
    for sent in doc.sents:
        for word in sent:
            #print("   " + word + " | " + word.dep_)
            print("    ", word, "[", word.dep_, "]")
            #print(word, word.dep_, word.tag_, word.pos_, word.morph)
    print("====================================================")




