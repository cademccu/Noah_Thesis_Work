
import sys
sys.path.append("..")

import subprocess
import os
import spacy
import re

from corpus_file_reader import CorpusFileReader
from CONFIGURATION import PATH_TO_CCOT, PATH_TO_DATA


# making this global because it deserves it
nlp = spacy.load("en_core_web_lg")

def _get_func_name(_func):
    """
    gets the same of a function from a function. For file and naming
    reasons.

    Args:
        _func (function)

    Returns:
        (str): name of the function
    """
    return str(_func).split()[1]

def _parse_file(infile, outfile, chunker, criteria_list):
    """
    this function takes a file, and reads it with the 'chunker' method, and then
    writes the relvant data and metadata to 'outfile'

    Args:
        infile (str): the input processed file from step one
        outfile (str): the path and name of the output file
        chunker (func): a function that splits the line from the CorpusFileReader into logical
                        segments, be it sentence, comma, or something else.
                        (must return a plain text chunk, no nlp() docs)
        criteria (list<func>): a function that determines whether the sentence is a 'fragment' or not
    """

    # open outfile 
    out = open(outfile, "wt")

    # these variables will be for saving metadata
    line_count = 0
    chunk_count = 0

    fragment_count = {}
    fragment_chunks = {}
    func_names = []

    for crit in criteria_list:
        name = _get_func_name(crit)
        fragment_count[name] = 0
        fragment_chunks[name] = []
        func_names.append(name)

    # init the filereader 
    cfp = CorpusFileReader(infile)
    line = cfp.next_line()

    while line:
        line_count += 1

        # split into the chunks desired (some discourse present about what constitutes a clause or sentence)
        chunks = chunker(line.strip())
        chunk_count += len(chunks)

        # reset the list
        for func_name in func_names:
            fragment_chunks[func_name] = []

        for chunk in chunks:
            if len(chunk.strip()) == 0:
                continue
            doc = nlp(chunk)
            for crit_func in criteria_list:
                if crit_func(doc):
                    name = _get_func_name(crit_func)
                    fragment_count[name] += 1
                    fragment_chunks[name].append(chunk)

        # write the initial line
        out.write(line + "\n")
        
        # if none of the values have _any_ values, just write no fragments
        has_any_fragments = False
        for v_frag_list in fragment_chunks.values():
            if len(v_frag_list) > 0:
                has_any_fragments = True
        
        if has_any_fragments:
            for key, values in fragment_chunks.items():
                out.write(" " * 4 + "*" + key + "\n")
                if len(values) == 0:
                    out.write(" " * 8 + "---NO_FRAGMENTS\n")
                else:
                    for fragment in values:
                        out.write(" " * 8 + fragment + "\n")
        else:
            out.write(" " * 4 + "---NO_FRAGMENTS_ANY\n")
            
        out.write("\n")
        line = cfp.next_line()


    out.write("\n\n")

    longest_name = 20
    for _name in func_names:
        if len(_name) + 11 > longest_name:
            longest_name = len(_name) + 11
    longest_name += 2 # to account for brackets in the dynamic method names

    f_string = "=== {:<" + str(longest_name) + "} | "
    out.write(f_string.format("FILE") + infile + "\n")
    out.write(f_string.format("LINE COUNT") + str(line_count) + "\n")
    out.write(f_string.format("CHUNK/SENTENCE COUNT") + str(chunk_count) + "\n")
    
    for key, value in fragment_count.items():
        out.write(("=== FRAG COUNT {:<" + str(longest_name-11) + "} | ").format("[" + key + "]") + str(value) + "\n")


def _by_sentence_period(line):
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

def _by_comma(line):
    pass


def ISFRAG_hasFiniteVerb_HasSubject(sent):
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



def main():
    # paths
    path_to_work =        os.path.join(PATH_TO_CCOT, "WORK")
    path_to_work_output = os.path.join(PATH_TO_DATA, "WORK_OUTPUT")

    # list of functions to determine fragements -- every single on of these is a test on a 
    # chunk/sentence to determine if they are a fragment or not. the method name just needs
    # to be in this list, and it will be run on every file.
    is_fragment_list = [
        ISFRAG_hasFiniteVerb_HasSubject,
        ISFRAG_MissingFiniteVerb,
        ISFRAG_MissingSubject
    ]

    # need to make this dir if doesnt exist
    if not os.path.isdir (path_to_work_output):
        subprocess.run(["mkdir", path_to_work_output])
    else:
        # it exists! clear it -- no globbing and also im lazy so -
        for to_rm in subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK_OUTPUT")]).decode("utf-8").split("\n"):
            if to_rm.endswith("_OUTFILE.txt"):
                subprocess.run(["rm", os.path.join(path_to_work_output, to_rm)])
        
    # list working files
    #files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK")]).decode("utf-8").split("\n")
    files = ["22-232_231-S.txt", "15-038_270-S.txt", "24-360_438-S.txt"] # selected at random

    for _file in files:
        infile = os.path.join(path_to_work, _file)
        outfile_stem = os.path.join(path_to_work_output, _file[:-4])

        # by sentence
        _parse_file(infile, outfile_stem + "_OUTFILE.txt", _by_sentence_period, is_fragment_list)


if __name__ == "__main__":
    main()
