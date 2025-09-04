


# These are some special cases that can't (really) be programatically cleaned and
# dealt with without some serious code that isnt necessary for the situation. They
# just need to be clean and reproducable.
import sys
sys.path.append("..")
from CONFIGURATION import PATH_TO_CCOT
import os
import subprocess

# in this particular file, the transcriber used a '[' instead of a '('
with open(os.path.join(PATH_TO_CCOT, "WORK/18-313_141-S.txt"), "rt") as infile:
    outfile = open(os.path.join(PATH_TO_CCOT, "WORK/18-313_141-S.txt.TMP"), "wt")
    line = infile.readline()
    while line:
        if line.startswith("3  A:"):
            outfile.write(line[:line.index("[")] + line[line.index(")") + 1:])
        else:
            outfile.write(line)
        line = infile.readline()

subprocess.run(["rm", os.path.join(PATH_TO_CCOT, "WORK/18-313_141-S.txt")])
subprocess.run(["mv", os.path.join(PATH_TO_CCOT, "WORK/18-313_141-S.txt.TMP"), os.path.join(PATH_TO_CCOT, "WORK/18-313_141-S.txt")])
