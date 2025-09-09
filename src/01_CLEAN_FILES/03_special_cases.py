


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

def r4(line):
    if line.strip().startswith("Teacher:"):
        return False
    return True

conditional_remove("07-532_201-A.txt", r4)

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

line_add("05-503_391-A.txt", "young uh and uh half of cla –her classes from 8:00a.m. until 7:00p.m. uh she she she didn't uh –she doesn't have time to enter –to attend –attended into university health care.")

line_add("21-373_434-S.txt", "make it at him the good advice or the help him in the future? … What what about you do you have an idea about that?")

line_add("21-477_502-S.txt", "NTA children uh the NTA children.  Uh I know that uh spank has uh consequences in the future but that is the best NTA for uh them.  The other the the you must make punishment it's very hard … you must make the p-uh-punishment it's very hard that's good for your uh son uh y-uh-he-your son he wanna make uh some bad he remind my father or my mother he uh spank me for this uh for this uh he cannot do this uh another time you know?  What about you uh you're uh father or mother he spank you already?")

line_add("22-431_268-S.txt", "Mexico food.  Uh for sure first thing it's there is a lot of Mexico people they live here in Flagstaff and most uh American people they like the Mexico food and uh the opportunity it's most the student most the people they live in Flagstaff they're students so they don't like to cook they just want eat.  Uh uh … outside … and uh yeah we have-I have uh two weakness-weaknesses.  Uh first is there is a lot many Mexico restaurant in Flagstaff.  Actually just one weakness .  So")





