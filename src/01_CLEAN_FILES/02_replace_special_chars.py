"""
This file is just renaming the files to a linux friendly format, and parsing the
'type of conversation' from the two participants and splitting their IDs from that
"""

import sys
sys.path.append("..")

import subprocess
import os
import time
import re
from CONFIGURATION import PATH_TO_CCOT


# keeps trying to open .TMP files, which leads me to believe there is some overlap
# between copying on the previous script and the ls -1 on this script. Hopefully a 
# light pause will let the OS catch up...
time.sleep(2)

# list working files
files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "WORK")])

for _file in files.decode("utf-8").split("\n"): 
    if len(_file) == 0:
        continue

    # NOTE: Intended to just use 'sed -i s//g' but apparently sed is goofy on mac:
    # https://stackoverflow.com/questions/7573368/in-place-edits-with-sed-on-os-x
    # Instead going to stream the files and replace/modify -- same thing.

    # make full path to file
    _file = os.path.join(PATH_TO_CCOT, "WORK", _file)

    with open(_file, "rt") as orig_file:
        out_file = open(_file + ".TMP", "wt")
        line = orig_file.readline()
       
        while line:

            # preserve whitespace? sure
            if len(line.strip()) == 0:
                out_file.write(line)
                line = orig_file.readline()
                continue

            # not sure what this special character is but i dont like it
            line = line.replace("	", " ") # you can see this char with :set list in vim

            # Metadata & transcription author section
            if line[0] == "<":
                # Nothing specific here yet. Might want to delete at some point.
                out_file.write(line)
                line = orig_file.readline()
                continue
           
            # search/replace any '%' char -- can be changed later if they have transcription importance
            line = line.replace("%", "") # currently replacing with nothing

            # replace '/---/' with placeholder. '/---/'' appears to represent a word that cannot in good
            # faith be transcribed. I am remapping to 'NTA' -- 'No Transcription Available' to avoid spacy
            # doing something funky with the punctuation. I will create a special rule for the tokenizer
            # to handle these.
            # NOTE: the trasnscribers appear to just randomly use different versions of the missing word
            # thus the below regex which handles most everything
            regex_str = r'\/\s?\-{2,6}\s?\/?'
            line = re.subn(regex_str, "NTA", line, count=1000)[0] # hacky

            # need to remove all the em dashes '--' and replace them with nothing.
            line = line.replace("--", "")

            # Transcribers notes are written sometimes inside of the file in parenthesis. i want to delete
            # these as they are not a part of the conversation, rather a clarifying point or guess, which
            # while interesting isnt useful in parsing (for now).
            while "(" in line and ")" in line:
                # do until all parenthesis are gone -- extra whitespace handled by spacy
                # there are nested parentheis. This doesnt delete the inner and then the outer,
                # it just deletes the largest outer since everything enclosed must go.
                p_start = line.index("(") 
                depth = 0 
                for i in range(p_start + 1, len(line)):
                    if line[i] == ")" and depth == 0:
                        line = line[:p_start] + line[i + 1:] 
                        break # only for loop, while still checks again
                    elif line[i] == ")" and depth > 0:
                        depth -= 1
                    elif line[i] == "(":
                        depth += 1
           
            # write to newfile 
            out_file.write(line)
            line = orig_file.readline()
                

    # now we can swap the files.
    subprocess.run(["rm", _file])
    subprocess.run(["mv", _file + ".TMP", _file])
    
