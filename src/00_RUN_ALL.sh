#!/bin/bash

# this script runs ever bit of processing, in order. 


# NOTE: yeah, this script probably isnt compatable with vanilla windows.. 
# you might have to run each step manually

cd 01_CLEAN_FILES

echo "Running: 01_CLEAN_FILES/01_rename_files.py"
python3 01_rename_files.py
echo "Done!"

echo "Running: 01_CLEAN_FILES/02_replace_special_chars.py"
python3 02_replace_special_chars.py
echo "Done!"

cd ..
