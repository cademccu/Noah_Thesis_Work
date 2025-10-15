#!/bin/bash

# this script runs ever bit of processing, in order. 


# NOTE: yeah, this script probably isnt compatable with vanilla windows.. 
# you might have to run each step manually


# if this dir already exists... CLEAN IT UP 
PATH_TO_CCOT=`python3 -c "import CONFIGURATION; print(CONFIGURATION.PATH_TO_CCOT)"`
echo `pwd`
PATH_TO_CCOT+="/WORK"

    

cd 01_CLEAN_FILES

# path should be relative to the script folders, or absolute, either way this works
if [ -e $PATH_TO_CCOT ]; then
    rm ${PATH_TO_CCOT}/*-*_*-?.txt
fi

echo "Running: 01_CLEAN_FILES/01_rename_files.py"
python3 01_rename_files.py
echo "Done!"

echo "Running: 01_CLEAN_FILES/02_replace_special_chars.py"
python3 02_replace_special_chars.py
echo "Done!"

echo "Running: 01_CLEAN_FILES/03_special_cases.py"
python3 03_special_cases.py
echo "Done!"

cd ..

cd 02_RUN_SPACY

echo "Running: 01_split_by_sentence.py"
python3 01_split_by_sentence.py	
echo "Done!"

echo "Running: 02_get_counts.py"
python3 02_get_counts.py	
echo "Done!"

cd ..


echo "Finished running all code."
