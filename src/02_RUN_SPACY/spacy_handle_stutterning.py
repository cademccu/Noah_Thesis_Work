


import spacy
# https://github.com/explosion/spaCy/blob/master/spacy/glossary.py#L49

nlp = spacy.load("en_core_web_lg")

# this is good for em dashes
# /Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK/22-230_229-S.txt


def formatted_output(s):
    print()
    print(s)
    doc = nlp(s)

    f_string = "{:<20}|" * 8

    print("-" * (20 * 8 + 8))
    print(f_string.format("text", "lemma", "pos", "tag", "dep", "shape", "is_alpha", "is_stop"))
    print("-" * (20 * 8 + 8))

    for token in doc:
        print(f_string.format(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop))

    print("-" * (20 * 8 + 8))
    print()

formatted_output("Also in uh my uh Arabic uh market uh it's uh very expensive because we should bring the--")

formatted_output("Yes if they ha-have some mistake you can uh you can punishment uh the children but it will hurt your relationship with the children and i-if you can't if you can't control your action spanking will hurt children body uh I think they need to use other ways to teach children uh but not only to span-spanik-spanking the children.")
