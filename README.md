
## Overview

This project utilizies custom code and spacy to parse an existing corpus, tokenize it, and search for fragmentary language. It is done on behalf of, and in collaboration with Noah Larson for his Master's Thesis. All code here is written with the direction and collaboration of Noah Larson, by Cade McCumber.

I will upload some additional documents with explanation/outcomes/research should they become available and be worth uploading.


## RUNNING THE PROJECT

You will have to set up a python3 enviroment. One should be able to run it with just a modern version of python3 and an enviorment with spacy, but you can also use my enviroment specs exactly to set it up.

To run the project, simply clone this repository and unzip the copy of CCOT data to a directory of your choosing. I chose to place it in the \'data\' dir of this, and if you do so the gitignore will not allow it to be uploaded. Once this is complete, please update the path to this data in src/CONFIGURATION.py with either a relative or absolute path to the data. If doing relative path, the path should be relative from INSIDE one of the code directorys such as 01\_CLEAN\_DATA, not relative to the CONFIGURATION.py file. This is because all code is run in a subdirectory from src, not at the top level.

Once these paths are correct, run bash script in src. If you are on windows or can only run python3, you can run each script in 01\_CLEAN\_DATA individually with the python3 executable, and then all numbered scripts in 02\_RUN\_SPACY.

```
# give execution priviledge to script
chmod +x 00_RUN_ALL.sh
# run script
./00_RUN_ALL.sh
```

Once the script complete, all data will be located in your data directory. The parsed data will be in data/WORK\_OUTPUT and the \'cleaned\' data files will be in CCOT/WORK, renamed to be linux friendly while retaining all the filename metadata.


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

Currently, formulaic speech is just determined by length. The heuristics for determining types of formulaic speech are outside of the scope of this study, and since this data will mostly be combed through by Noah by hand, further distinction was not deemed necessary. For a list of all chunks and sentence fragments deemed formulaic, see src/03\_REPORTS/FORMULAIC\_LIST\_UNIQUE.txt

In addition, each file contains metadata at the bottom:

```
=== FILENAME                                                | ../../data/CCOT/WORK/20-452_585-B.txt
=== LINE COUNT                                              | 16
=== CHUNK/SENTENCE COUNT                                    | 32
=== FORMULAIC COUNT                                         | 5
=== FRAG COUNT [ISFRAG_MissingFiniteVerb_or_MissingSubject] | 5
=== FRAG COUNT [ISFRAG_MissingFiniteVerb]                   | 3
=== FRAG COUNT [ISFRAG_MissingSubject]                      | 4
=== FRAG COUNT [ISFRAG_MissingVerb_FromMorph]               | 18
=== FRAG COUNT [ISFRAG_MissingVerb_FromDep]                 | 18
```

The original file, number of _valid_ lines read from the file, the number of chunks or sentences that were created from those lines, the number of chunks deemed formulaic, and finally the count of fragments returned by each method which is located after the pipe on each line.

Some additional statistics are generated from the data, and can be foound in textfile form at src/03\_REPORTS. These include all unique formulaic chunks and their counts, and the summary of the total metadata counts above.


## Cleaning the data

The data is split into files containing conversations between subjects, with metadata \(usually denoted by a \'\<\' opener, but not always \). The data is messy for our uses, including transcriber notes, stuttering, and some inconsistancies with transcription. This section decribes what is done to \'clean\' the data, though more information can be found in the code itself on the exact process and this description is just a plaintext description.

All code related to cleaning/preparing the data is in src/01\_CLEAN\_FILES

#### Step 1

First, the files had to be renamed, mostly so they could be worked with in linux without having to escape everything. All information in filename is retained, the prefix is pulled for the start (denotes the conversation type), the 3 number ID is preserved in order, and the letter of the conversation.

```
# pre rename (note the & char.... linguists!!!)
02010&02172_C.txt

# after the rename
02-010_172-C.txt
```

#### Step 2 

This step involves a lot of character removal, replacing, etc. For a full understanding of the processing, please refer to src/01\_CLEAN\_FILES/02\_replace\_special\_chars.py 

A brief summary, but not an exhaustive list:

+ remove whitespace, along with OS specific whitespace chars
+ replace any special chars from transcription that may denote emphasis, but are not important to our use case
+ replace the various Missing Values used by transcribers with a set 'NTA' string to allow for better parsing by spacy.
+ remove em dashes
+ remap unicode dashes to utf-8 dashes
+ remove transcriptions of stuttered speech which would confuse spacy and replace it with the intended word when possible
+ remove all transcribers notes that are not apart of the corpus that are in parensthesis or brackets


#### Step 3

Step 3 mostly involves removing step 2 instances that don't quite follow the patterns to be programmatically removed.

+ instances where transcribers notes use a mismatch of parentheis and brackets
+ lines are not numbered and labeled and are likely just the accidental press of the ENTER key
+ fusing together lines that were split

## PARSING THE DATA

I wrote a custom filereader class for the cleaned files C01\_corpus\_file\_reader.py that ignores existing metadata, and parses out the annotations for the speaker as they are not needed for this analysis. The speaker annotations are by the loosest definitions "consistant" so the function \_get\_generator() shows many different options for removing the speaker (and other) annotations still left in the file after cleaning.

This acts as a reader for all files. All files are read, chunked and tokenized with spacy, and the tokens are then checked for specific tests present in A01\_chunking\_and\_frag\_checks.py and B01\_formulaic\_checks.py which check for sentence fragments and formulaic speech repectively. 

All files are output containing all the matches for these fragment and formulaic checks with their own special annotation, described above for review. In addition, a file is produced containing all the formulaic language and the counts.

## Useful links used during development

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



