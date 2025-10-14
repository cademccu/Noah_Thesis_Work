
"""
This is a file containing all the chunking and fragmentation checks for 01_split_by_sentence.py
"""



def CHUNK_by_sentence_period(line):
    """
    splits up a line by period. if EOL is reached, that counts as the end of the
    sentence.

    Args:
        line (str): a line from a step 1 processed file

    Returns:
        (list<str>): the sentences from the line
    """
    if "." in line:
        return line.split(".")
    else:
        return [line]


def ISFRAG_MissingVerb_FromDep(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria
    must not have any verb in from token.dep_

    Args:
        sent (spacy nlp doc): the nlp parsed doc object of a sentence or chunk

    Returns:
        (boolean): True if the doc is a fragment, False if not
    """

    has_dep_verb = False

    for token in sent:
        if "VERB" == token.dep_:
            has_dep_verb = True
    
    return not has_dep_verb


def ISFRAG_MissingVerb_FromMorph(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria
    must not have any verb in from token.morph

    Args:
        sent (spacy nlp doc): the nlp parsed doc object of a sentence or chunk

    Returns:
        (boolean): True if the doc is a fragment, False if not
    """

    has_morph_verb = False

    for token in sent:
        if "Verb" in token.morph:
            has_morph_verb = True
    
    return not has_morph_verb


def ISFRAG_MissingFiniteVerb_or_MissingSubject(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria
    must have neither subject or fitinite verb to return true

    Args:
        sent (spacy nlp doc): the nlp parsed doc object of a sentence or chunk

    Returns:
        (boolean): True if the doc is a fragment, False if not
    """

    # found some info on finite verbs, seems they live in the morph seg of the token
    # found this by brute force and grep --!
    # https://universaldependencies.org/u/feat/VerbForm.html
    has_finite_verb = False
    # Okay, for subject, it appears there are several types of subject. In spacy, if it contains 'subj' in the .doc_
    # str it is a subject of _some_ kind -- therefore what we are looking for in the moment. 
    # https://stackoverflow.com/questions/66181946/identify-subject-in-sentences-using-spacy-in-advanced-cases
    # seems to 
    has_subject = False

    for token in sent:
        if "VerbForm=Fin" in token.morph:
            has_finite_verb = True
        if "subj" in token.dep_:
            has_subject = True

    # okay, check this:
    # i think if there is a finite verb, and a subject, then we are _not_ considering this a fragment
    # therefore:
    # this has the same truth table as (not has_subject or not has_finite_verb)
    return not (has_subject and has_finite_verb)



def ISFRAG_MissingFiniteVerb(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria
    if sentence is missing a finite verb, return True

    Args:
        sent (spacy nlp doc): the nlp parsed doc object of a sentence or chunk

    Returns:
        (boolean): True if the doc is a fragment, False if not
    """

    # found some info on finite verbs, seems they live in the morph seg of the token
    # found this by brute force and grep --!
    # https://universaldependencies.org/u/feat/VerbForm.html
    has_finite_verb = False

    for token in sent:
        if "VerbForm=Fin" in token.morph:
            has_finite_verb = True

    return not has_finite_verb


def ISFRAG_MissingSubject(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria
    if senetence is missing a subject, return true

    Args:
        sent (spacy nlp doc): the nlp parsed doc object of a sentence or chunk

    Returns:
        (boolean): True if the doc is a fragment, False if not
    """
    # Okay, for subject, it appears there are several types of subject. In spacy, if it contains 'subj' in the .doc_
    # str it is a subject of _some_ kind -- therefore what we are looking for in the moment. 
    # https://stackoverflow.com/questions/66181946/identify-subject-in-sentences-using-spacy-in-advanced-cases
    # seems to 
    has_subject = False

    for token in sent:
        if "subj" in token.dep_:
            has_subject = True

    # okay, check this:
    # i think if there is a finite verb, and a subject, then we are _not_ considering this a fragment
    # therefore:
    return not has_subject

