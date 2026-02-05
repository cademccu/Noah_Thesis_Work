

"""
0  :  Native Language
1  :  Speaker ID
2  :  Speaker gender
3  :  Role
4  :  File number_version
5  :  Task name
6  :  Task version
7  :  Time
8  :  Level
9  :  Pair
10  :  Length of file
11  :  PT_col_R1
12  :  PT_col_R2
13  :  PT_col_AVE
14  :  PT_TC_R1
15  :  PT_TC_R2
16  :  PT_TC_AVE
17  :  PT_sty_R1
18  :  PT_sty_R2
19  :  PT_sty_AVE
20  :  Total /12
"""


with open("CCOT_files_and_scores.csv", "rt") as f:
    headers = f.readline()

    line = f.readline()

    count = 0

    while line:

        line = line.split(",")
        print(line[4], " : ", line[8], " : ", line[13], " : ", line[11], " : ", line[12])

        line = f.readline()
        count += 1
        if count % 2 == 0:
            print()
            print("filename           : lvl : avg :  R1 : R2")
            
