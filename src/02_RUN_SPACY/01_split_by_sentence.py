
import sys
sys.path.append("..")

import subprocess
import os
import spacy
import re

from corpus_file_reader import CorpusFileReader
from CONFIGURATION import PATH_TO_CCOT


# making this global because it deserves it
nlp = spacy.load("en_core_web_lg")



def _parse_file(infile, outfile, chunker, criteria):
    """
    this function takes a file, and reads it with the 'chunker' method, and then
    writes the relvant data and metadata to 'outfile'

    Args:
        infile (str): the input processed file from step one
        outfile (str): the path and name of the output file
        chunker (func): a function that splits the line from the CorpusFileReader into logical
                        segments, be it sentence, comma, or something else.
                        (must return a plain text chunk, no nlp() docs)
        criteria (func): a function that determines whether the sentence is a 'fragment' or not
    """


    # open outfile 
    out = open(outfile, "wt")

    # these variables will be for saving metadata
    line_count = 0
    chunk_count = 0
    fragment_count = 0

    # init the filereader 
    cfp = CorpusFileReader(os.path.join(PATH_TO_CCOT, "WORK", infile))
    line = cfp.next_line()

    while line:
        line_count += 1

        # split into the chunks desired (some discourse present about what consituteus clause or sentence)
        chunks = chunker(line.strip())
        chunk_count += len(chunks)
       
        frag_chunks = []

        for chunk in chunks:
            if len(chunk.strip()) == 0:
                continue
            doc = nlp(chunk)
            if criteria(doc):
                fragment_count += 1
                frag_chunks.append(chunk)
        out.write(line + "\n")
        if len(frag_chunks) > 0:
            for frag_chunk in frag_chunks:
                out.write("    " + frag_chunk + "\n")
        else:
            # this is subject to change:
            out.write("    NO_FRAGMENTS\n")
            
        line = cfp.next_line()


    out.write("\n\n")
    out.write("=== " + "FILE:        " + infile + "\n")
    out.write("=== " + "LINE COUNT:  " + str(line_count) + "\n")
    out.write("=== " + "CHUNK COUNT: " + str(chunk_count) + "\n")
    out.write("=== " + "FRAG COUNT:  " + str(fragment_count) + "\n")


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


def _is_fragment(sent):
    """ 
    checks if the spacy processed document is a fragment based on custom criteria

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




def main():
    # paths
    path_to_work =        os.path.join(PATH_TO_CCOT, "WORK")
    path_to_work_output = os.path.join(PATH_TO_CCOT, "WORK_OUTPUT")

    # need to make this dir if doesnt exist
    if not os.path.isdir (path_to_work_output):
        subprocess.run(["mkdir", path_to_work_output])
    else:
        # it exists! clear it -- no globbing and also im lazy so -
        for to_rm in subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK_OUTPUT")]).decode("utf-8").split("\n"):
            if to_rm.endswith("_FRAGMENTS.txt"):
                subprocess.run(["rm", os.path.join(PATH_TO_CCOT, "WORK_OUTPUT", to_rm)])
        
    # list working files
    #files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK")]).decode("utf-8").split("\n")
    files = ["22-232_231-S.txt", "15-038_270-S.txt", "24-360_438-S.txt"] # selected at random

    for _file in files:
        infile = os.path.join(PATH_TO_CCOT, "WORK", _file)
        outfile_stem = os.path.join(PATH_TO_CCOT, "WORK_OUTPUT", _file[:-4])

        # by sentence
        _parse_file(_file, outfile_stem + "_BY_PERIOD_FRAGMENTS.txt", _by_sentence_period, _is_fragment)


if __name__ == "__main__":
    main()
