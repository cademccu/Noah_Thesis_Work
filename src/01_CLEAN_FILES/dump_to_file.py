
# this is if you have the exported CSV of the spreadsheet -- this will process it into 
# the file you need to rename the files correctly. I do not know if any of that is 
# proprietary, so i am only including what it needed here.

# 1. export mv 'CCOT_files and scores.xlsx' to 'CCOT_files and scores.csv'
# 2. mv CCOT_files\ and\ scores.csv CCOT_files_and_scores.csv 
# 3. mv to this directory

from math import ceil

_infile  = "CCOT_files_and_scores.csv"
_outfile = "01A_corpus_metadata.csv"

infile  = open("CCOT_files_and_scores.csv", "rt")
outfile = open("01A_corpus_metadata.csv", "wt")


# Native Language,Speaker ID,Speaker gender,Role,File number_version,Task name,Task version,Time,Level,Pair,Length of file,PT_col_R1,PT_col_R2,PT_col_AVE,PT_TC_R1,PT_TC_R2,PT_TC_AVE,PT_sty_R1,PT_sty_R2,PT_sty_AVE,Total /12
"""
Native Language 0
Speaker ID 1
Speaker gender 2
Role 3
File number_version 4
Task name 5
Task version 6
Time 7
Level 8
Pair 9
Length of file 10
PT_col_R1 11
PT_col_R2 12
PT_col_AVE 13
PT_TC_R1 14
PT_TC_R2 15
PT_TC_AVE 16
PT_sty_R1 17
PT_sty_R2 18
PT_sty_AVE 19
Total /12
"""

# i COULD use csv for this, but i also could not and be speedy

header = infile.readline().split(",")
line = infile.readline()

outfile.write("id,level,collaboration_score\n")

while line:
    line = line.split(",")
    collab = str(ceil(float(line[13])))
    outfile.write(line[1].strip() + "," + line[8].strip() + "," + collab + "\n")
    
    line = infile.readline()







