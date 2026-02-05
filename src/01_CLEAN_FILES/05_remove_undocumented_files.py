


# these are files that are valid BUT are not at all in the documentation.... 
# so we are REMOVING the processed versions of them so they do not muddle
# or otherwise confuse the processing process


# NOTES: 04-282-275 has an 02 version in the docs... which I originally corrected to 
# here. turns out, both files exist, but only 02 has 'Advertisement' documentation
# same with 05-212-206 ---> 07 is the only documented one
# 24-485_555-S.txt --- literally no mention of this convo from either participant
# in the csv file
files = ["04-282_275-B.txt", "05-212_206-C.txt", "24-485_555-S.txt"]

import sys
sys.path.append("..")
from CONFIGURATION import PATH_TO_CCOT
import os

for f in files:
    os.remove(os.path.join(PATH_TO_CCOT, "WORK", f))
