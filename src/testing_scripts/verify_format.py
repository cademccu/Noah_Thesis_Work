import sys
import subprocess 
import re

files = subprocess.check_output(["ls" , "-1", "/Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK"]).decode("utf-8").strip().split("\n")
files = [e for e in files if e.endswith(".txt")]

total_len = 0

for name in files:
    has_ireg = False
    ireg_data = []
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
                fline = line
                line = line.split() 
                try:
                    if line[1] not in ["A:", "B:", "S?:", "S:", "A;"]:
                        # some skip line numbers
                        if line[0] not in ["A:", "B:", "S?:"]:
                            # some combine num and speaker
                            if not re.search(r"[0-9]{1,3}[AB]{1}\:{1}", line[0]): # or  re.search(r"^[0-9]{1,3}\s[S]{1}\??\:{1}", fline):
                                if not re.search(r"[0-9]{1,3}\s{1,2}[ABS]{1}\s{1}", fline):
                                    # arnt linguists supposed to care about format?
                                    if not line[0].strip().lower() in ["verified", "verfied"]:
                                        has_ireg = True
                                        #print(name + ": " + " ".join(line))
                                        ireg_data.append(" ".join(line))
                except IndexError as ind:
                    print("\u001b[31m" "ERROR: " + name + " : " + " ".join(line) + "\u001b[0m")
            line = f.readline()
    if has_ireg:
        print("\u001b[31m" + name + "\u001b[0m")
        total_len += len(ireg_data)
        for i in ireg_data:
            print(i)

print("\u001b[31m" + "TOTAL COUNT: " + str(total_len) +  "\u001b[0m")
        

    



