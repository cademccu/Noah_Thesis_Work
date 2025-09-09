import sys
import subprocess 

files = subprocess.check_output(["ls" , "-1", "/Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK"]).decode("utf-8").strip().split("\n")
files = [e for e in files if e.endswith(".txt")]


for name in files:
    with open( "/Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK/" + name, "rt") as f:
        line = f.readline()
        while line:
            if len(line.strip()) == 0:
                line = f.readline()
                continue
            elif line.strip()[0] == "<":
                line = f.readline()
                continue
            else:
                line = line.split()
                try:
                    if line[1] not in ["A:", "B:"]:
                        print(name + ": " + " ".join(line))
                except IndexError as ind:
                    print("ERROR: " + name + " : " + " ".join(line))
            line = f.readline()

    
