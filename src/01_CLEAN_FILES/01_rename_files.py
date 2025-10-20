"""
This file is just renaming the files to a linux friendly format, and parsing the
'type of conversation' from the two participants and splitting their IDs from that
"""

import sys
sys.path.append("..")

import subprocess
import os
from CONFIGURATION import PATH_TO_CCOT



# another classic inconsistancy
# cross verified with spreadsheet it should be 515
try:
    # shouldnt have renamed this permanantly..
    os.rename(
        os.path.join(PATH_TO_CCOT, "CCOT_all_untagged", "05443&0515._B.txt"),
        os.path.join(PATH_TO_CCOT, "CCOT_all_untagged", "05443&05515_B.txt")
    )
except FileNotFoundError:
    print("[INFO]  05443&0515._B.txt already renamed to 05443&05515_B.txt")



# grab the untagged files from the directory
untagged_files = subprocess.check_output(["ls", "-1", os.path.join(PATH_TO_CCOT, "CCOT_all_untagged")])

# make a new directory for the processed data (if not exist)
new_dir = os.path.join(PATH_TO_CCOT, "WORK")
if not os.path.isdir(new_dir):
    subprocess.run(["mkdir", new_dir])

# iterate through all of them and rename to the format:
# <conversation_type>-<ID_A>_<ID_B>.txt
for untagged in untagged_files.decode("utf-8").split("\n"):
    if len(untagged) == 0:
        continue
    orig_name = untagged # need for copy command
    convo_type = untagged[0:2]
    untagged = untagged.split("&")
    id_a = untagged[0][2:]
    id_b = untagged[1].split("_")[0][2:]
    letter = untagged[1].split("_")[1][0]

    # build new name and path
    new_name = convo_type + "-" + id_a + "_" + id_b + "-" + letter + ".txt"
    new_name = os.path.join(new_dir, new_name)

    # since this is designed to be run in order, delete if exists already
    if os.path.isfile(new_name):
        subprocess.run(["rm", new_name])

    # copy file to new directory with new name
    subprocess.run(["cp", os.path.join(PATH_TO_CCOT, "CCOT_all_untagged", orig_name), new_name])
