

import spacy

nlp = spacy.load("en_core_web_lg")
for label in nlp.get_pipe("parser").labels:
    print(label, " -- ", spacy.explain(label))


for i in nlp.meta["sources"]:
    print(i)
