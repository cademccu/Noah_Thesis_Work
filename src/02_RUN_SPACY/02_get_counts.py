
import sys  
sys.path.append("..") # add the correct path

import subprocess
import os
from CONFIGURATION import PATH_TO_CCOT, PATH_TO_DATA


output_file_path    = "../03_REPORTS/TOTAL_COUNTS.txt"
path_to_work_output = os.path.join(PATH_TO_DATA, "WORK_OUTPUT")

fout = open(output_file_path, "wt") 
fout.write("""
This is a file that returns the total counts of the processed files
from the WORK_OUTPUT directory in data/
""")
fout.write("\n\n\n")



files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_DATA, "WORK_OUTPUT")]).decode("utf-8").split("\n")    

# just going to hold all the information in this here dictionary
total_counts = {}


for fname in files:
    if len(fname.strip()) == 0:
        continue

    with open(os.path.join(PATH_TO_DATA, "WORK_OUTPUT", fname), "rt") as f:
        line = f.readline()
        while not line.startswith("=== FILENAME"):
            # better ways of doing this but there isnt much data so
            line = f.readline()
        line = f.readline() # burn the filename value
        while line.startswith("=== "):
            line = line[4:].split("|")
            if line[0].strip() not in total_counts.keys():
                total_counts[line[0].strip()] = 0
            total_counts[line[0].strip()] += int(line[1].strip())

            line = f.readline()

longest = 0
for key in total_counts.keys():
    longest = longest if len(key) <= longest else len(key)
   
print("\n")

for key, value in total_counts.items():
    print(("{:<" + str(longest) + "}  {}").format(key, value))
    fout.write(("{:<" + str(longest) + "}  {}\n").format(key, value))

fout.write("\n\n\n")
fout.close()
print("\nWRITTEN TO OUTFILE: " + output_file_path + "\n\n")





    
