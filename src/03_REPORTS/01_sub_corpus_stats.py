
import sys  
sys.path.append("..") # add the correct path

import subprocess
import os
import re
from math import ceil
from CONFIGURATION import PATH_TO_CCOT, PATH_TO_DATA


path_to_work_output = os.path.join(PATH_TO_DATA, "WORK_OUTPUT")
#path_to_excel_csv   = "../01_CLEAN_FILES/CCOT_files_and_scores.csv"
path_to_excel_csv   = "../01_CLEAN_FILES/CCOT_files_and_scores_FIXED.csv"


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
            "col_average": str(ceil(float(line[13]))),
            "PT_col_R1": line[11],
            "PT_col_R2": line[12],
            "id_original_file": line[4]
        })

        line = f.readline()

#for val in values:
#    print(val)

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

def find_both_speakers(filename):
    """
    another horrific addition after the fact! ah i wish i was a trustfund kid

    get the entry in values directory of the spreadsheet for A and B speakers in the file
    """
    #25-580_577-S_OUTFILE.txt
    # {'id': '543', 'convo_type': '24', 'level': '3', 'col_average': '3', 'PT_col_R1': '3', 'PT_col_R2': '3', 'id_original_file': '24417&24543_S.txt'}
    type_ = filename[:2]
    first = filename[3:6]
    second = filename[7:10]
    both = []

    for val in values:
        if type_ == val["id_original_file"][0:2] and val["id_original_file"][2:5] in [first, second] and val["id_original_file"][8:11] in [first, second]:
            both.append(val)


    if len(both) != 2:
        print(len(both))
        for x in both:
            print("    ", x)
        id_match = "null"
        multiple = ""
        if len(both) > 1:
            id_match = both[0]["id_original_file"]
        if len(both) > 2:
            multiple = "MULTIPLE_MATCHES_FOUND"
        print("First: {}, second: {}, type: {}, filename: {}, id_match: {}   {}".format(first, second, type_, filename, id_match, multiple))
        #sys.exit(0)

    return both



def stats_file(outfile_name):
    #r"FORMULAIC\sCOUNT\s[AB]{1}[0-9]{3}"

    # vestigial organs of late nights??? not sure but i will not be refactoring at this time
    stats = {}
    matching_files = []
    frags_and_formuliacs = []

    outfile_stats = open(outfile_name, "wt")

    first_line = ",".join((["{}"] * 15)) + "\n"
    outfile_stats.write(first_line.format(
        "original_file_name",
        "id_A",
        "id_B",
        "sentence_count_A",
        "sentence_count_B",
        "level_A",
        "level_B",
        "collab_score_avg_A",
        "collab_score_avg_B",
        "fragment_count_A",
        "fragment_count_B",
        "fragment_count_all",
        "fragments_A",
        "fragments_B",
        "fragments_all"))
        

    for file_ in files:
        if len(file_.strip()) == 0:
            continue
        #print(file_)
        #for criteria in criteria_list:
        #if file_[:2] == criteria["convo_type"] and criteria["id"] in file_:


        # data that needs to be collected AHHH
        fragments_all = []
        fragments_A   = []
        fragments_B   = []
        fragments_all_count = 0
        fragments_A_count   = 0
        fragments_B_count   = 0
        collab_A = None
        collab_B = None
        level_A = None
        level_B = None
        sentence_count_A = 0
        sentence_count_B = 0
        id_A = None
        id_B = None
        id_ = None

        both_speakers = find_both_speakers(file_)


        # we should only need one of the files to match
        # the below section opens the file and deals with it
        criteria = both_speakers[0] 

        #if file_[:2] == criteria["convo_type"] and criteria["id"] in file_: # matches file with item in values


        f = open(os.path.join(PATH_TO_DATA, "WORK_OUTPUT", file_), "rt")
        line = f.readline()
        while not line.startswith("=== "):
            # just burn        
            line = f.readline()
        # now we are in the metadata section, handle 3*= fields
        while line.startswith("=== "):
            line = line[4:].split("|")

            # just using line count for id here...
            if line[0].strip().startswith("LINE COUNT A"):
                id_A = line[0].split(" ")[2]
            if line[0].strip().startswith("LINE COUNT B"):
                id_B = line[0].split(" ")[2]

                

            if re.match(r"CHUNK\/SENTENCE\sCOUNT\s[AB]{1}" + criteria["id"], line[0].strip()):
                if re.match(r"CHUNK\/SENTENCE\sCOUNT\s[A]{1}" + criteria["id"], line[0].strip()):
                    sentence_count_A += int(line[1].strip())
                    num_A = line[0].strip().split(" ")[2]
                elif re.match(r"CHUNK\/SENTENCE\sCOUNT\s[B]{1}" + criteria["id"], line[0].strip()):
                    sentence_count_B += int(line[1].strip())
                    num_B = line[0].strip().split(" ")[2]

            line = f.readline()

        # now we are in  5*=
        while line.startswith("===== "):

            line = line[6:].split("|")
            #if criteria["id"] in line[0]:
            #    print(criteria["id"])
            line = f.readline()

        while line.startswith("#####"):
            line = line.strip().split("|")
            assert len(line) == 2

            fragments = []
            if len(line[1].strip()) > 0:
                fragments = line[1].split("$")
            

            if line[0].strip() == "##### FRAGMENTS_ALL":
                fragments_all = fragments
                fragments_all_count = len(fragments)
            elif line[0].startswith("##### FRAGMENTS_ALL A"):
                fragments_A = fragments
                fragments_A_count = len(fragments)
            elif line[0].startswith("##### FRAGMENTS_ALL B"):
                fragments_B = fragments
                fragments_B_count = len(fragments)


            line = f.readline()

        # here, decide specific speakers
        speaker_A = None
        speaker_B = None
        if both_speakers[0]["id"] == id_A[1:4]:
            speaker_A = both_speakers[0]
            speaker_B = both_speakers[1]
        elif both_speakers[0]["id"] == id_B[1:4]:
            speaker_A = both_speakers[1]
            speaker_B = both_speakers[0]
        else:
            print("something is definitley wrong with your ids......")
            print(both_speakers)
            print(id_A, id_B)
            sys.exit(255)

        
        # {'id': '543', 'convo_type': '24', 'level': '3', 'col_average': '3', 'PT_col_R1': '3', 'PT_col_R2': '3', 'id_original_file': '24417&24543_S.txt'}
        collab_A = speaker_A["col_average"]
        collab_B = speaker_B["col_average"]
        level_A = speaker_A["level"]
        level_B = speaker_B["level"]
        id_ = speaker_A["id_original_file"]
        if speaker_A["id_original_file"] != speaker_B["id_original_file"]:
            # another few in the fix file.......
            print(speaker_A["id_original_file"], speaker_B["id_original_file"])
        
        # actually write to the output file

        # get ready for some format strings from GOD
        first_line = ",".join((["{}"] * 15)) + "\n"
        second_line = ("," * 12) + "{}" + ",,\n"
        third_line = ("," * 13) + "{}" + ",\n"
        fourth_line = ("," * 14) + "{}" + "\n"

        outfile_stats.write(first_line.format(
            id_,
            id_A,
            id_B,
            sentence_count_A,
            sentence_count_B,
            level_A,
            level_B,
            collab_A,
            collab_B,
            fragments_A_count,
            fragments_B_count,
            fragments_all_count,
            "",
            "",
            ""))

        for frag in fragments_A:
            outfile_stats.write(second_line.format(frag))
        for frag in fragments_B:
            outfile_stats.write(third_line.format(frag))
        for frag in fragments_all:
            outfile_stats.write(fourth_line.format(frag))




def searcher(criteria_list, outfile_name):
    #r"FORMULAIC\sCOUNT\s[AB]{1}[0-9]{3}"

    stats = {}
    matching_files = []
    frags_and_formuliacs = []
        

    for file_ in files:
        for criteria in criteria_list:
            if file_[:2] == criteria["convo_type"] and criteria["id"] in file_:
                matching_files.append((file_, criteria["id"]))
                f = open(os.path.join(PATH_TO_DATA, "WORK_OUTPUT", file_), "rt")
                line = f.readline()
                while not line.startswith("=== "):
                    if re.match(r"[AB]{1}" + criteria["id"], line):
                        line = f.readline() # burn the full un-chunked line
                        temp_list = []
                        while len(line.strip()) != 0:
                            line = line.strip()
                            if not (line.startswith("*ISFRAG") or
                                line.startswith("---NO_FRAGMENTS") or 
                                line == ">>>FORMULAIC_CHUNKS:"):
                                temp_list.append(line)
                            line = f.readline()
                        frags_and_formuliacs = frags_and_formuliacs + list(set(temp_list))
                            
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

    outfile.write("ALL FRAGMENTS AND FORMULAICS:\n")
    outfile.write("total count: " + str(len(frags_and_formuliacs)) + "\n")
    outfile.write("-----------------------------\n")
    for frag in frags_and_formuliacs:
        outfile.write(frag + "\n")
    outfile.write("\n\n")
    outfile.close()

    print("\nstats outfile created: " + outfile_name)

stats_file("INDIVIDUAL_FILE_STATS.csv")            


# slice it up by criteria 
searcher(slice_by("level", "1"), "LEVEL_1_STATS.txt")
searcher(slice_by("level", "2"), "LEVEL_2_STATS.txt")
searcher(slice_by("level", "3"), "LEVEL_3_STATS.txt")

searcher(slice_by("col_average", "1"), "COLLAB_SCORE_1_STATS.txt")
searcher(slice_by("col_average", "2"), "COLLAB_SCORE_2_STATS.txt")
searcher(slice_by("col_average", "3"), "COLLAB_SCORE_3_STATS.txt")
searcher(slice_by("col_average", "4"), "COLLAB_SCORE_4_STATS.txt")
searcher(slice_by("col_average", "5"), "COLLAB_SCORE_5_STATS.txt")


    
