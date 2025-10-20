
import sys
sys.path.append("..") # add the correct path

import subprocess
import os
import spacy
import re

from CONFIGURATION import PATH_TO_CCOT, PATH_TO_DATA
from A01_chunking_and_frag_checks import *
from B01_formulaic_checks import is_formulaic
from C01_corpus_file_reader import CorpusFileReader

#CHUNK_by_sentence_period, ISFRAG_MissingFiniteVerb_or_MissingSubject, ISFRAG_MissingFiniteVerb, ISFRAG_MissingSubject, ISFRAG_MissingVerb_FromMorph, ISFRAG_MissingVerb_FromDep, is_formulaic



# making this global because it deserves it
nlp = spacy.load("en_core_web_lg")
# making this global too because it also deserves it
a_to_z_regex = re.compile(r'[^a-zA-Z\s]')

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

       

def _parse_file(infile, outfile, chunker, criteria_list, formulaic_chunks_dict):
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
        formulaic_chunks (dict): the dictionary to store unique formulaic chunks and their counts
    """

    # open outfile 
    out = open(outfile, "wt")

    # these variables will be for saving metadata
    line_count = 0
    chunk_count = 0
    formulaic_count = 0

    formulaic_count_A = 0
    formulaic_count_B = 0

    fragment_count = {}
    fragment_chunks = {}

    fragment_count_A = {}
    fragment_count_B = {}
    fragment_chunks_A = {}
    fragment_chunks_B = {}
    
    func_names = []

    for crit in criteria_list:
        name = _get_func_name(crit)
        fragment_count[name] = 0
        fragment_count_A[name] = 0
        fragment_count_B[name] = 0
        fragment_chunks[name] = []
        func_names.append(name)

    # init the filereader 
    cfp = CorpusFileReader(infile)
    line = cfp.next_line()

    while line[0]:
        line_count += 1

        # split into the chunks desired (some discourse present about what constitutes a clause or sentence)
        chunks = chunker(line[1].strip())
        chunk_count += len(chunks)

        # reset the list
        for func_name in func_names:
            fragment_chunks[func_name] = []
            fragment_chunks_A[func_name] = []
            fragment_chunks_B[func_name] = []
        
        formulaic_chunks = [] 
        formulaic_chunks_A = [] 
        formulaic_chunks_B = [] 

        for chunk in chunks:
            if len(chunk.strip()) == 0:
                continue

            # if the chunk is 'formulaic', we don't even want to check.
            if is_formulaic(chunk):
                formulaic_chunks.append(chunk)
                if line[0] == "A":
                    formulaic_chunks_A.append(chunk)
                else: # B
                    formulaic_chunks_B.append(chunk)
                continue

            doc = nlp(chunk)
            for crit_func in criteria_list:
                if crit_func(doc):
                    name = _get_func_name(crit_func)
                    fragment_count[name] += 1
                    fragment_chunks[name].append(chunk)
                    if line[0] == "A":
                        fragment_count_A[name] += 1
                        fragment_chunks_A[name].append(chunk)
                    else: # B
                        fragment_count_B[name] += 1
                        fragment_chunks_B[name].append(chunk)
                        

        # write the initial line
        out.write(line[0] + ":  " + line[1] + "\n")
        
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

        if len(formulaic_chunks) > 0:
            formulaic_count += len(formulaic_chunks)
            out.write(" " * 4 + ">>>FORMULAIC_CHUNKS:\n")
            for f_chunk in formulaic_chunks:
                out.write(" " * 8 + f_chunk + "\n")
                # add to dict
                f_chunk = f_chunk.strip().lower()
                f_chunk = a_to_z_regex.sub('', f_chunk)
                if f_chunk not in formulaic_chunks_dict:
                    formulaic_chunks_dict[f_chunk] = 0
                formulaic_chunks_dict[f_chunk] += 1

        # we dont need to print these out specifically
        formulaic_count_A += len(formulaic_chunks_A)
        formulaic_count_B += len(formulaic_chunks_B)

            
        out.write("\n")
        line = cfp.next_line()

    # get the info
    speakers = cfp.get_speakers()

    out.write("\n\n")

    longest_name = 20
    for _name in func_names:
        if len(_name) + 11 > longest_name:
            longest_name = len(_name) + 11
    longest_name += 2 # to account for brackets in the dynamic method names

    f_string = "=== {:<" + str(longest_name) + "} | "
    out.write(f_string.format("FILENAME") + infile + "\n")
    out.write(f_string.format("LINE COUNT") + str(line_count) + "\n")
    out.write(f_string.format("CHUNK/SENTENCE COUNT") + str(chunk_count) + "\n")

    out.write(f_string.format("FORMULAIC COUNT") + str(formulaic_count) + "\n")
    out.write(f_string.format("FORMULAIC COUNT A" + speakers["A"]) + str(formulaic_count_A) + "\n")
    out.write(f_string.format("FORMULAIC COUNT B" + speakers["B"]) + str(formulaic_count_B) + "\n")
    
    for key, value in fragment_count.items():
        out.write(("=== FRAG COUNT {:<" + str(longest_name-11) + "} | ").format("[" + key + "]") + str(value) + "\n")

    for key, value in fragment_count_A.items():
        out.write(("===== FRAG COUNT A" + speakers["A"] + " {:<" + str(longest_name-11) + "} | ").format("[" + key + "]") + str(value) + "\n")
    for key, value in fragment_count_B.items():
        out.write(("===== FRAG COUNT B" + speakers["B"] + " {:<" + str(longest_name-11) + "} | ").format("[" + key + "]") + str(value) + "\n")

def main():
    # paths
    path_to_work =        os.path.join(PATH_TO_CCOT, "WORK")
    path_to_work_output = os.path.join(PATH_TO_DATA, "WORK_OUTPUT")

    # this is to store the unique formuliac chunks and their counts
    formulaic_chunks = {}

    # list of functions to determine fragements -- every single on of these is a test on a 
    # chunk/sentence to determine if they are a fragment or not. the method name just needs
    # to be in this list, and it will be run on every file.
    is_fragment_list = [
        ISFRAG_MissingFiniteVerb_or_MissingSubject,
        ISFRAG_MissingFiniteVerb,
        ISFRAG_MissingSubject,
        ISFRAG_MissingVerb_FromMorph,
        ISFRAG_MissingVerb_FromDep
    ]

    # need to make this dir if doesnt exist
    if not os.path.isdir (path_to_work_output):
        subprocess.run(["mkdir", path_to_work_output])
    else:
        # it exists! clear it -- no globbing and also im lazy so -
        for to_rm in subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_DATA, "WORK_OUTPUT")]).decode("utf-8").split("\n"):
            if to_rm.endswith("_OUTFILE.txt"):
                subprocess.run(["rm", os.path.join(path_to_work_output, to_rm)])
        
    # list working files
    files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK")]).decode("utf-8").split("\n")
    #files = ["22-232_231-S.txt", "15-038_270-S.txt", "24-360_438-S.txt"] # selected at random

    for _file in files:
        if len(_file.strip()) == 0:
            continue
        infile = os.path.join(path_to_work, _file)
        outfile_stem = os.path.join(path_to_work_output, _file[:-4])

        # by sentence
        _parse_file(infile, outfile_stem + "_OUTFILE.txt", CHUNK_by_sentence_period, is_fragment_list, formulaic_chunks)
    # sort the formulaic chunks
    formulaic_chunks = {k: v for k, v in sorted(formulaic_chunks.items(), key=lambda item: item[1], reverse=True)}

    formulaic_outfile = open("../03_REPORTS/FORMULAIC_LIST_UNIQUE.txt", "wt")

    for key, value in formulaic_chunks.items():
        formulaic_outfile.write(key + "   [" + str(value) + "]\n")

    formulaic_outfile.close()

if __name__ == "__main__":
    main()




