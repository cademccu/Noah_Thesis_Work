


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
    swaps temp file to regular file, deletes old file

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





# turns out we need the individual statistic for each person which include their ID and wether they
# are A or B speaker so we (me) can grap sub corpora for analysis... 
# these 10 files (in the supplimental text file) all are missing or have poorly formatted 
# metadata on the speakers. I manually/programmatically compiled the list from the excel spreadsheet
# and several hacky scripts.
no_metadata_files = {}

with open("03A_missing_metadata.txt", "rt") as f:
    line = f.readline()
    while line:
        if len(line.strip()) == 0:
            continue
        line = line.split("|")
        no_metadata_files[line[0].strip()] = {
            "A":line[1].strip().split()[0],
            "B":line[1].strip().split()[2]
        }
        line = f.readline()

            
for key, value in no_metadata_files.items():
    tmp_file = open(os.path.join(PATH_TO_CCOT, "WORK", key + ".TMP"), "wt")
    curr_file = open(os.path.join(PATH_TO_CCOT, "WORK", key), "rt")

    # just add it to the top of the file, faster reads anyways
    tmp_file.write("<Student A: " + key[0:2] + value["A"] + "; Student B: " + key[0:2] + value["B"] + ">\n")

    line = curr_file.readline()
    while line:
        tmp_file.write(line)
        line = curr_file.readline()

    tmp_file.close()
    curr_file.close()
    _swapper(os.path.join(PATH_TO_CCOT, "WORK", key))


def fix_metadata_id(metadata_file, oldstr, newstr):
    # more transcription errors, this time in the etadata
    fm1 = open(os.path.join(PATH_TO_CCOT, "WORK", metadata_file), "rt")
    fm1_tmp = open(os.path.join(PATH_TO_CCOT, "WORK", metadata_file + ".TMP"), "wt")
    line = fm1.readline()
    while line:
        if line.strip() == oldstr:
            fm1_tmp.write(newstr + "\n")
        else:
            fm1_tmp.write(line)
        line = fm1.readline()
    _swapper(os.path.join(PATH_TO_CCOT, "WORK", metadata_file))

fix_metadata_id("15-038_270-S.txt", "<A is 15028; B is 15270>", "<A is 15038; B is 15270>")
fix_metadata_id("02-261_326-B.txt", "<A is 02122; B is B02326>", "<A is 02261; B is 02326>")
fix_metadata_id("02-328_324-A.txt", "<A is S?; B is S?>", "<A is 02324; B is 02328>")
fix_metadata_id("02-371_256-A.txt", "<A is 02334; B is 02256>", "<A is 02371; B is 02256>")
fix_metadata_id("02-523_458-C.txt", "<A is 02523; B is 02461>", "<A is 02523; B is 02458>")
fix_metadata_id("03-577_580-S.txt", "<Student A: 03581 and Student B: 03577>", "<A is 03580; B is 03577>")
fix_metadata_id("04-014_172-A.txt", "<Student A is 04010; Student B is 04172>", "<A is 04014; B is 04172>")
# these arnt in the spreadsheet correctly and thus must be manually conjured
fix_metadata_id("16-103_137-S.txt", "<Student A is 16103; Student B is 16044>", "<A is 16103; B is 16137>")
fix_metadata_id("04-594_228-A.txt", "<A is 04594; B is 04087>", "<A is 04594; B is 04228>")
fix_metadata_id("05-499_079-C.txt", "<A is 05596; B is 05079>", "<A is 05499; B is 05079>")
fix_metadata_id("20-573_399-A.txt", "<A is 20571; B is 20399>", "<A is 20573; B is 20399>")

# turns out about 10% of the files have an error like this... pulled the data via much
# trickery and wrote all necessary info to a file in this directory. Programmatic time.
# output of cross reference code:
fix_metadata_id("04-050_505-A.txt", "<A is 04050; B is 04476>", "<A is 04050; B is 04505>")
fix_metadata_id("04-143_286-C.txt", "<Student A is 04286; Student B is 04140>", "<A is 04286; B is 04143>")
fix_metadata_id("04-268_015-B.txt", "<Student A is 04066; Student B is 04268>", "<A is 04015; B is 04268>")
fix_metadata_id("04-455_523-A.txt", "<Student A is 04461; Student B is 04523>", "<A is 04455; B is 04523>")
fix_metadata_id("05-102_474-A.txt", "<A is 05102; B is 05482>", "<A is 05102; B is 05474>")
fix_metadata_id("05-109_057-A.txt", "<A is 05109; B is 05058>", "<A is 05109; B is 05057>")
fix_metadata_id("05-124_412-C.txt", "<A is 05124; B is 05012>", "<A is 05124; B is 05412>")
fix_metadata_id("05-181_186-A.txt", "<A is 05187; B is 05186>", "<A is 05181; B is 05186>")
fix_metadata_id("05-188_361-C.txt", "<A is 05188; B is 05348>", "<A is 05188; B is 05361>")
fix_metadata_id("05-224_153-B.txt", "<A is 05224; B is 05513>", "<A is 05224; B is 05153>")
fix_metadata_id("05-329_336-D.txt", "<Student A is 05319; Student B is 05329>", "<A is 05336; B is 05329>")
fix_metadata_id("05-382_510-A.txt", "<Student A is 05510; Student B is 05033>", "<A is 05510; B is 05382>")
fix_metadata_id("06-427_469-A.txt", "<Student A is 06527; Student B is 06442>", "<A is 06427; B is 06469>")
fix_metadata_id("07-161_396-B.txt", "<Student A is 07131; Student B is 07161>", "<A is 07396; B is 07161>")
fix_metadata_id("07-258_020-B.txt", "<Student A is 07258; Student B is 07048>", "<A is 07258; B is 07020>")
fix_metadata_id("07-429_596-B.txt", "<Student A is 07351; Student B is 07429>", "<A is 07596; B is 07429>")
fix_metadata_id("08-164_133-S.txt", "<Student A: 08166; Student B: 08133>", "<A is 08164; B is 08133>")
fix_metadata_id("08-449_524-S.txt", "<A is 08449; B is 08516>", "<A is 08449; B is 08524>")
fix_metadata_id("09-153_591-S.txt", "<Student A is 09153; Student B is 09163>", "<A is 09153; B is 09591>")
fix_metadata_id("09-452_424-S.txt", "<Student A is 09452; Student B is 09420>", "<A is 09452; B is 09424>")
fix_metadata_id("10-517_303-S.txt", "<Student A: 08303; Student B: 08483>", "<A is 10303; B is 10517>")
fix_metadata_id("11-554_489-S.txt", "<Student A is 11552; Student B is 11489>", "<A is 11554; B is 11489>")
fix_metadata_id("12-162_058-B.txt", "<A is 12057; B is 12162>", "<A is 12058; B is 12162>")
fix_metadata_id("12-223_029-A.txt", "<Student A is 12029; Student B is 12222>", "<A is 12029; B is 12223>")
fix_metadata_id("12-564_177-B.txt", "<A is 12177; B is 12538>", "<A is 12177; B is 12564>")
fix_metadata_id("13-068_309-S.txt", "<A is 13218; B is 13068>", "<A is 13309; B is 13068>")
fix_metadata_id("16-064_113-S.txt", "<Student A is 16059; Student B is 16113>", "<A is 16064; B is 16113>")
fix_metadata_id("16-522_551-S.txt", "<Student A is 16315; Student B is 16551>", "<A is 16522; B is 16551>")
fix_metadata_id("17-148_159-S.txt", "<Student A is 17148; Student B is 17590>", "<A is 17148; B is 17159>")
fix_metadata_id("17-354_573-S.txt", "<Student A is 17571; Student B is 17354>", "<A is 17354; B is 17573>")
fix_metadata_id("17-441_588-S.txt", "<Student A is 17444; Student B is 17588>", "<A is 17441; B is 17588>")
fix_metadata_id("18-049_162-S.txt", "<Student A is 18162; Student B is 18058>", "<A is 18162; B is 18049>")
fix_metadata_id("18-381_296-S.txt", "<Student A is 18271; Student B is 18381>", "<A is 18296; B is 18381>")
fix_metadata_id("18-510_033-S.txt", "<Student A is 18510; Student B is 18382>", "<A is 18510; B is 18033>")
fix_metadata_id("18-573_435-S.txt", "<Student A is 18573; Student B is 18026>", "<A is 18573; B is 18435>")
fix_metadata_id("19-305_349-p.txt", "<A is 19341; B is 19305>", "<A is 19349; B is 19305>")
fix_metadata_id("19-360_588-p.txt", "<A is 19588; B is 19542>", "<A is 19588; B is 19360>")
fix_metadata_id("19-462_407-p.txt", "<A is 19438; B is 19407>", "<A is 19462; B is 19407>")
fix_metadata_id("20-159_444-A.txt", "<A is 20154; B is 20444>", "<A is 20159; B is 20444>")
fix_metadata_id("20-524_590-B.txt", "<Student A is 20154; Student B is 20524>", "<A is 20590; B is 20524>")
fix_metadata_id("21-163_516-S.txt", "<Student A is 21163; Student B is 21524>", "<A is 21163; B is 21516>")
fix_metadata_id("21-360_437-S.txt", "<Student A is 21542; Student B is 21437>", "<A is 21360; B is 21437>")
fix_metadata_id("21-361_152-S.txt", "<Student A is 21348; Student B is 21152>", "<A is 21361; B is 21152>")
fix_metadata_id("21-371_094-S.txt", "<Student A is 21334; Student B is 21094>", "<A is 21371; B is 21094>")
fix_metadata_id("21-477_502-S.txt", "<Student A is 21582; Student B is 21037>", "<A is 21502; B is 21477>")
fix_metadata_id("21-538_507-S.txt", "<Student A is 21357; Student B is 21538>", "<A is 21507; B is 21538>")
fix_metadata_id("22-095_511-S.txt", "<A is 22094; B is 22511>", "<A is 22095; B is 22511>")
fix_metadata_id("22-096_364-S.txt", "<A is A22041; B is 22096>", "<A is 22364; B is 22096>")
fix_metadata_id("22-389_228-S.txt", "<A is 22387; B is 22228>", "<A is 22389; B is 22228>")
fix_metadata_id("22-415_466-S.txt", "<A is 22414; B is 22466>", "<A is 22415; B is 22466>")
fix_metadata_id("22-527_153-S.txt", "<A is 22242; B is 22153>", "<A is 22527; B is 22153>")
fix_metadata_id("23-032_082-B.txt", "<Student A: 23032 and Student B: 23024>", "<A is 23032; B is 23082>")
fix_metadata_id("23-144_008-A.txt", "<A is 23346; B is 23144>", "<A is 23008; B is 23144>")
fix_metadata_id("23-158_166-A.txt", "<Student A: 23164 and Student B: 23158>", "<A is 23166; B is 23158>")
fix_metadata_id("23-201_007-B.txt", "<A is 23034; B is 23201>", "<A is 23007; B is 23201>")
fix_metadata_id("23-322_403-A.txt", "<Student A: 23322 and Student B: 23556>", "<A is 23322; B is 23403>")
fix_metadata_id("23-334_539-A.txt", "<A is 05539; B is 05371>", "<A is 23539; B is 23334>")
fix_metadata_id("23-349_305-A.txt", "<Student A: 23341 and Student B: 23305>", "<A is 23349; B is 23305>")
fix_metadata_id("23-498_282-B.txt", "<Student A: 23350 and Student B: 23282>", "<A is 23498; B is 23282>")
fix_metadata_id("24-234_297-S.txt", "<Student A is 24297; Student B is 24090>", "<A is 24297; B is 24234>")
fix_metadata_id("24-565_148-S.txt", "<Student A is 24565; Student B is 24184>", "<A is 24565; B is 24148>")
fix_metadata_id("25-028_027-S.txt", "<Student A: 25028 and Student B: 25022>", "<A is 25028; B is 25027>")
fix_metadata_id("25-297_234-S.txt", "<Student A: 25297 and Student B: 25090>", "<A is 25297; B is 25234>")
fix_metadata_id("25-413_054-S.txt", "<Student A: 25486 and Student B: 25054>", "<A is 25413; B is 25054>")
fix_metadata_id("25-438_542-S.txt", "<Student A: 25438 and Student B: 25360>", "<A is 25438; B is 25542>")

#fix_metadata_id("02-261_326-B.txt", 

