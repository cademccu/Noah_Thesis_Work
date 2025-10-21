
import sys  
sys.path.append("..") # add the correct path

import subprocess
import os
import re
from math import ceil
from CONFIGURATION import PATH_TO_CCOT, PATH_TO_DATA


path_to_work_output = os.path.join(PATH_TO_DATA, "WORK_OUTPUT")
path_to_excel_csv   = "../01_CLEAN_FILES/CCOT_files_and_scores.csv"


# first, lets generate the datastructure populated with the values 
# we want

values = []
with open(path_to_excel_csv, "rt") as f:
    headers = f.readline()

    line = f.readline()
    while line:
        if len(line.strip()) == 0:
            line = f.readline()
            continue

        line = line.split(",")

        id_ = line[1]
        if len(id_) < 3:
            id_ = ("0" * (3-len(id_))) + id_

        type_id = line[4].strip()
        t1 = type_id.split("&")[0][:2]
        t2 = type_id.split("&")[1][:2]
        if (t1 == t2):
            type_id = t1
        # more errors in the docs, more errors in the docs
        elif type_id == "05441&04284_A.txt":
            type_id = "05"
        elif type_id == "20355&30560_A.txt":
            type_id = "20" # probably

        values.append({
            "id": id_,
            "convo_type" : type_id,
            "level": line[8],
            "col_average": str(ceil(float(line[13])))
        })

        line = f.readline()


files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_DATA, "WORK_OUTPUT")]).decode("utf-8").split("\n")    


def slice_by(key, match):
    matches = []
    for val in values:
        if val[key] == match:
            matches.append({
                "convo_type": val["convo_type"],
                "id": val["id"]
            })
    return matches


def searcher(criteria_list, outfile_name):
    #r"FORMULAIC\sCOUNT\s[AB]{1}[0-9]{3}"

    stats = {}
    matching_files = []
        

    for file_ in files:
        for criteria in criteria_list:
            if file_[:2] == criteria["convo_type"] and criteria["id"] in file_:
                matching_files.append((file_, criteria["id"]))
                f = open(os.path.join(PATH_TO_DATA, "WORK_OUTPUT", file_), "rt")
                line = f.readline()
                while not line.startswith("=== "):
                    line = f.readline()
                # now we are in the metadata section, handle 3*= fields
                while line.startswith("=== "):
                    line = line[4:].split("|")

                    if re.match(r"FORMULAIC\sCOUNT\s[AB]{1}" + criteria["id"], line[0].strip()):
                        if not "FORMULAIC COUNT" in stats:
                            stats["FORMULAIC COUNT"] = 0
                        stats["FORMULAIC COUNT"] += int(line[1].strip())

                    elif re.match(r"LINE\sCOUNT\s[AB]{1}" + criteria["id"], line[0].strip()):
                        if not "LINE COUNT" in stats:
                            stats["LINE COUNT"] = 0
                        stats["LINE COUNT"] += int(line[1].strip())

                    elif re.match(r"CHUNK\/SENTENCE\sCOUNT\s[AB]{1}" + criteria["id"], line[0].strip()):
                        if not r"CHUNK/SENTENCE" in stats:
                            stats[r"CHUNK/SENTENCE"] = 0
                        stats[r"CHUNK/SENTENCE"] += int(line[1].strip())

                    line = f.readline()
                # now we are in  5*=
                while line.startswith("===== "):
                    line = line[6:].split("|")
                    if criteria["id"] in line[0]:
                        if not ("FRAG COUNT " + line[0].split()[3]) in stats:
                            stats["FRAG COUNT " + line[0].split()[3]] = 0
                        stats["FRAG COUNT " + line[0].split()[3]] += int(line[1].strip())
                    line = f.readline()
    
    # write to file section
    outfile = open(outfile_name, "wt")

    longest = 0
    for key in stats.keys():
        longest = longest if len(key) <= longest else len(key)

    for key, value in stats.items():
        outfile.write(("{:<" + str(longest) + "}  {}\n").format(key, value))

    outfile.write("\n\n")
    outfile.write("MATCHING FILES & MATCHING ID:\n")
    outfile.write("num files: " + str(len(matching_files)) + "\n")
    outfile.write("-----------------------------\n")
    for match in matching_files:
        outfile.write(match[0] + " | " + match[1] + "\n")
    outfile.write("\n\n")
    outfile.close()

    print("\nstats outfile created: " + outfile_name)

            
            
# slice it up by criteria 
searcher(slice_by("level", "1"), "LEVEL_1_STATS.txt")
searcher(slice_by("level", "2"), "LEVEL_2_STATS.txt")
searcher(slice_by("level", "3"), "LEVEL_3_STATS.txt")

searcher(slice_by("col_average", "1"), "COLLAB_SCORE_1_STATS.txt")
searcher(slice_by("col_average", "2"), "COLLAB_SCORE_2_STATS.txt")
searcher(slice_by("col_average", "3"), "COLLAB_SCORE_3_STATS.txt")
searcher(slice_by("col_average", "4"), "COLLAB_SCORE_4_STATS.txt")
searcher(slice_by("col_average", "5"), "COLLAB_SCORE_5_STATS.txt")


    
