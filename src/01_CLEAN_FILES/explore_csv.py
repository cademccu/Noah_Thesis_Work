header = "Native Language,Speaker ID,Speaker gender,Role,File number_version,Task name,Task version,Time,Level,Pair,Length of file,PT_col_R1,PT_col_R2,PT_col_AVE,PT_TC_R1,PT_TC_R2,PT_TC_AVE,PT_sty_R1,PT_sty_R2,PT_sty_AVE,Total /12".split(",")

for i, var in enumerate(header):
    print("{} : {}".format(i, var)


import sys

if len(sys.argv) < 2:
    print("USAGE: index of field to print")
    sys.exit(0)


indexes = sys.argv[1:]
indexes = [int(x) for x in indexes]

with open("CCOT_files_and_scores_FIXED.csv", "rt") as f:
    
    # burn header
    f.readline()


    fstring = "|".join(["{}"] * len(indexes))
    



    
