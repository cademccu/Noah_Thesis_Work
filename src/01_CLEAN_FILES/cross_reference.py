
# this doesn't need to be run. this was written and run to produce suplemental correction
# material for all the transcription errors. preserving in case it comes up.


import subprocess


pre = []
with open("id_errors_precursor.txt") as f:
    line = f.readline()
    while line:
        pre.append(line)
        line = f.readline()

# XXXXX|25-438_542-S.txt|542|438|<Student A: 25438 and Student B: 25360>

outfile = open("id_errors.txt", "wt")

# doing this the slow way 
scores = open("CCOT_files_and_scores.csv", "rt")
scores_l = []
line = scores.readline()
while line:
    scores_l.append(line)
    line = scores.readline()


for data_row in pre:
    matches = [] 
    data_row = data_row.split("|")
    for line in scores_l:
        if len(line.strip()) == 0:
            continue
        line = line.split(",")
        if data_row[2] in line[4] and data_row[3] in line[4] and data_row[1][:2] == line[4][:2]:
            matches.append(line)
    
    if len(matches) != 2:
        print(len(matches))
        print(data_row)

    A, B = None, None
    # you wouldnt believe it but even their data speadsheet isnt right sometimes.. oh yes you would
    if matches[0][3] == "A":
        A = matches[0][1]
        if len(A) == 2:
            A = "0" + A
        elif len(A) == 1:
            A = "00" + A
        B = matches[1][1]
        if len(B) == 2:
            B = "0" + B
        elif len(B) == 1:
            B = "00" + A
    elif matches[0][3] == "B":
        B = matches[0][1]
        if len(B) == 2:
            B = "0" + B
        A = matches[1][1]
        if len(A) == 2:
            A = "0" + A
        elif len(A) == 1:
            A = "00" + A
        elif len(B) == 1:
            B = "00" + A

    # Arabic,58,M,B,02162&02058_A.txt,
    # matches
    print('fix_metadata_id("{}", "{}", "<A is {}; B is {}>")'.format(
        data_row[1].strip(), 
        data_row[4].strip(), 
        data_row[1].strip()[-16:-14] + A, 
        data_row[1].strip()[-16:-14] + B
   ))


