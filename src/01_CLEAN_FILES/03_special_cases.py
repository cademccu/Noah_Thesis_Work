


# These are some special cases that can't (really) be programatically cleaned and
# dealt with without some serious code that isnt necessary for the situation. They
# just need to be clean and reproducable.
import sys
sys.path.append("..")
from CONFIGURATION import PATH_TO_CCOT
import os
import subprocess

def _swapper(filename):
    """
    swaps temp file to regualr file, deletes old file

    Args:
        filename(str): the root file path (without '.TMP' at the end)
    """
    subprocess.run(["rm", filename])
    subprocess.run(["mv", filename + ".TMP", filename])

# in this particular file, the transcriber used a '[' instead of a '('
with open(os.path.join(PATH_TO_CCOT, "WORK", "18-313_141-S.txt"), "rt") as infile:
    outfile = open(os.path.join(PATH_TO_CCOT, "WORK", "18-313_141-S.txt.TMP"), "wt")
    line = infile.readline()
    while line:
        if line.startswith("3  A:"):
            outfile.write(line[:line.index("[")] + line[line.index(")") + 1:])
        else:
            outfile.write(line)
        line = infile.readline()

_swapper(os.path.join(PATH_TO_CCOT, "WORK", "18-313_141-S.txt"))

def conditional_remove(filename, criteria):
    """
    removes a line from a file if it doesn't meet the criteria

    Args:
        filename (str): the name of the file
        criteria (func): a function that takes the line as an arg and returns True if line
                         should be included, False if it should be removed
    """
    filename = os.path.join(PATH_TO_CCOT, "WORK", filename)
    with open(filename, "rt") as f:
        fout = open(filename + ".TMP", "wt")
        for line in f:
            if criteria(line):
                fout.write(line)

    _swapper(filename)


def r1(line):
    if line.strip() == "1" or line.strip() == "F10wk15_Investing_12187 & 12186":
        return False
    return True
    
conditional_remove("12-187_186-B.txt", r1)



def r2(line):
    if line.strip() == "…":
        return False
    return True

conditional_remove("20-159_444-A.txt", r2)


def r3(line):
    if line.strip() == ".":
        return False
    return True

conditional_remove("21-537_460-S.txt", r3)


def line_add(filename, sent):
    """
    a few instances of a file having an arrant newline 
    this function adds those lines together based on the line

    Args:
        filename (str): the name of the file
        sent (str): the line to be added to the line before it
    """

    # if anyone reads this, this is dirty and not stream editing. But im 
    # doing this for free so whatever, lists

    filename = os.path.join(PATH_TO_CCOT, "WORK", filename)
    with open(filename, "rt") as f:
        f_list = []
        fout = open(filename + ".TMP", "wt")
        for line in f:
            if line.strip() == sent:
                f_list[-1] = f_list[-1].strip() + line
            else:
                f_list.append(line)
        for line in f_list:
            fout.write(line)

    _swapper(filename)



# someone clicked enter huh
line_add("22-182_340-S.txt", "will")

line_add("22-095_511-S.txt", "type?")
