
## PROGRAM OUTPUT

The output files for this program will be creating in your \'data\' directory, which should be correct by default in the CONSTANTS.py file.

Output files contain the parsed data, and have one of two states. Both states contain the line, but if none of the fragment testing methods returned a fragment for any sentence in the line, the sentence will only contain a message indicating that nothing at all was found in the line. If _any_ of the fragment methods used in the file found a fragment sentence in the line, they will all be listed beneath the line. Each function will either have a message indicating that no fragments were found with that function, or it will list every sentence in the line that the given function returned \'True\' for being a fragment.

Example with no fragments found for any fragment functions:
``` 
Yeah but I agree with you.
    ---NO_FRAGMENTS_ANY
```

Example with the first and last function of three having returned the sentence as being a fragment.
```
Okay thank you.
    *ISFRAG_hasFiniteVerb_HasSubject
        Okay thank you 
    *ISFRAG_MissingFiniteVerb
        ---NO_FRAGMENTS
    *ISFRAG_MissingSubject
        Okay thank you 
```

As stated in other section \"Cleaning the Data\", the data is read line\-wise, and thus there may be multiple sentences from a single speaker on a given line. This is done so that if needed in the future, individual speakers can be isolated and checked for fragmentary speech, as well as keeping each burst of speech together.

Another feature of the output data involves \'formulaic chunks\'. These are chunks of text that by many fragment definition would be considered fragments, but are not interesting for this study because they are reoccuring patterns of speech instead of shortered versions of fully grammatically correct speech, such as \'Thank you\' or \'No\'. A chunk will not be considered for fragment checks if it meets this critera, and will be added at the end of the printout of the speaker:

```
Uh-huh.
    ---NO_FRAGMENTS_ANY
    >>>FORMULIAC_CHUNKS:
        Uh-huh
```

In addition, each file contains metadata at the bottom:

```
=== FILE                                         | ../../data/CCOT/WORK/22-232_231-S.txt
=== LINE COUNT                                   | 48
=== CHUNK/SENTENCE COUNT                         | 95
=== FRAG COUNT [ISFRAG_hasFiniteVerb_HasSubject] | 29
=== FRAG COUNT [ISFRAG_MissingFiniteVerb]        | 25
=== FRAG COUNT [ISFRAG_MissingSubject]           | 28
```

The original file, number of _valid_ lines read from the file, the number of chunks or sentences that were created from those lines, and finally the count of fragments returned by each method which is denoted in brackets.



## Running the project

You will have to set up a python3 enviroment. One should be able to run it with just a modern version of python3 and an enviorment with spacy, but you can also use my enviroment specs exactly to set it up.

To run the project, simply clone this repository and unzip the copy of CCOT data to a directory of your choosing. I chose to place it in the \'data\' dir of this, and if you do so the gitignore will not allow it to be uploaded. Once this is complete, please update the path to this data in CONFIGURATION.py with either a relative or absolute path to the data. If doing relative path, the path should be relative from INSIDE one of the code directorys such as 01\_CLEAN\_DATA, not relative to the CONFIGURATION.py file. This is because all code is run in a subdirectory from src, not at the top level.

Once these paths are correct, run bash script in src. If you are on windows or can only run python3, you can run each script in 01\_CLEAN\_DATA individually with the python3 executable, and then all numbered scripts in 02\_RUN\_SPACY.

```
# give execution priviledge to script
chmod +x 00_RUN_ALL.sh
# run script
./00_RUN_ALL.sh
```

Once the script complete, all data will be located in your data directory. The parsed data will be in data/WORK\_OUTPUT and the \'cleaned\' data files will be in CCOT/WORK, renamed to be linux friendly while retaining all the filename metadata.


## Cleaning the data

TODO

## Overview

The data is split into files containing conversations between subjects, with metadata \(usually denoted by a \'\<\' opener, but not always \). The data is messy for our uses, including transcriber notes, stuttering, and some inconsistancies with transcription. The following section decribes what is done to \'clean\' the data, though more information can be found in the code itself on the exact process and this description is just a plaintext description.

TODO 


## Useful links

Token docs:

https://spacy.io/api/token

Some info on the universal dependencies, specifically finite verbs for our use:

https://universaldependencies.org/u/feat/VerbForm.html

Token Dependency defintions:

https://github.com/clir/clearnlp-guidelines/blob/master/md/specifications/dependency\_labels.md

Spacy glossary:

https://github.com/explosion/spaCy/blob/master/spacy/glossary.py



### Notes on authorship

'burnt' is cademccu's new laptop that he forgot to set his global user.email and user.name ... so consider all commits by burnt to be cademccu


### Notes on cross-platform compatability

* This was written on MacOS (unix). It should run on other linux systems, though this is untested. It should also be able to run on Windows, with the caveots that:
1. You will need to swap/change the subprocess commands to the windows equivalent
2. I will not be testing on windows because I do not have a windows computer and also don't want/need to. All hail Linus Torvalds or something.


### TODO

special case for NTA: https://spacy.io/usage/linguistic-features#special-cases


