


import sys
import re



class CorpusFileReader:
    """
    This class reads the cleaned up corpus files. It returns line-by-line data for the actual
    conversation, and can return the '<>' surrounded metadata as well if needed. 

    Processes metadata on calls to get_metadata() and removes the speaker/line-number 
    information for lines.

    """

    def __init__(self, _file):
        self._METADATA = self._set_metadata(_file)
        self._FILE = _file
        self._CORPUS_FILE = open(_file, "rt")
        self._GENERATOR = None
        self._A , self._B = self._get_speakers()
        self._THROWN_OUT_LINES_S = 0 
        


    def _set_metadata(self, _file):
        """
        Fetches all the metadata from the file.

        Args:
            _file (str): path to file
        Returns:
            (list<str>): the list of all metadata lines.
        """
        m_list = []
        with open(_file, "rt") as f:
            line = f.readline()
            while line:
                if len(line.strip()) > 0 and line.strip()[0] == "<":
                    m_list.append(line)
                line = f.readline()
        return m_list


    def get_metadata(self):
        """
        Get the metadata associated with this file.

        Returns:
            (list<str>): The metadata, unprocessed, of this file
        """
        if self._METADATA is None:
            self._METADATA = self._set_metadata(self._FILE)
        return self._METADATA

    def get_speakers(self):
        """
        Get a dictionary of speakers A and B parsed from the file.
        """
        return {"A":self._A,"B":self._B}



    def _get_speakers(self):
        """
        OH YEAH TURNS OUT WE NEED TO FETCH THE SPEAKERS FROM THE METADATA
        this is the internal version called in init -- for the usable version
        use the non-underscored version
        """
        speakers_line = None
        for line in self._METADATA:
            # after some corpus modification and much checking, believe it or not,
            # these two catagories cover all 775 files. grep it if you dont 
            # beleive me (in the postprocessed data)
            if line.startswith("<Student A") or line.startswith("<A"):
                speakers_line = line
                break
        if speakers_line is None:
            print("[ERROR]  No speakers line was found in C01_corpus_file_reader.py _get_speakers()")
            sys.exit(-1)
        
        # A always comes first...
        # pull names from filename... 
        try:
            match1 = re.search(("[0-9]{2}" + self._FILE[-9:-6]), speakers_line)
            match2 = re.search(("[0-9]{2}" + self._FILE[-13:-10]), speakers_line)
            if match1.start() > match2.start():
                # A is the first occuring
                return self._FILE[-9:-6], self._FILE[-13:-10]
            else:
                return self._FILE[-13:-10], self._FILE[-9:-6]
        except AttributeError:
            # this one isnt my fault
            # believe it or not, the transcribers do not always put the correct 
            # ID numbers in the damn file and thus there is a None returned as
            # a match. Print out relevant file info so it can be addressed in
            # 03_special_cases.py
            print("Error in searching for speakers in metadata:")
            print("FILENAME: " + self._FILE)
            print("LINE:     " + speakers_line)
            print("NUM_1:    " + self._FILE[-9:-6])
            print("NUM_2:    " + self._FILE[-13:-10])
            print()
            # this is for several in depth layers of fixing. should never hit this error 
            # now but keeping because my distrust in this corpus is high and mighty
            # for fixing easier... ugh
            #print('fix_metadata_id("{}", "{}", "<A is {}; B is {}>")'.format(self._FILE[-16:], speakers_line.strip(), self._FILE[-16:-14], self._FILE[-16:-14]))
            # new output system since this is the worst ive ever seen.
            #print("XXXXX|" + self._FILE[-16:] + "|" + self._FILE[-9:-6] + "|" + self._FILE[-13:-10] + "|" + speakers_line.strip())
            #sys.exit(-1)
            return "000", "000" # just to see...

            

    def next_line(self):
        """
        Gets the next line in the file, or returns None if there are no more lines.

        Returns:
            tup(str,str):
                (str|None): the Speaker, either A or B
                (str|None): the next line in the file
        """
        # doing this with a generator, but obfuscating for readability
        if self._GENERATOR is None:
            self._GENERATOR = self._get_generator()
        try:
            return next(self._GENERATOR)
        except StopIteration:
            return (None, None)
       

    def _get_generator(self):
        """
        Gets the next non-empty, non-metadata line from the file

        Returns:
            tup(str,str):
                (str|None): the Speaker, either A or B
                (str|None) Returns the next non-empty, non-metadata line
        """
        
        # this is lazy but im not engineering here, sorry yeild!
        for line in self._CORPUS_FILE:
            if len(line.strip()) == 0:
                continue
            elif line.strip()[0] == "<":
                # metadata line
                continue
            elif line.split()[0].lower() in ["verified", "verfied"]:
                # writing verified on wrong line, and mispelling sometimes
                continue
            else:
                # This right here is where the shennanigans begins...
                # there are multiple different 'approaches' it seems some of the researchers 
                # associated with this project have taken in transcribing the converstations.
                # WE only want the actual words transcribed. Much of the cleaning has already 
                # been done, but now we have to deal with the way the transcribers 'interpreted'
                # letting the user of the data kno which individual is speaking. 
                # All methods have been tested in ../testing_scripts/verify_format.py and 
                # along with the cleaning have managed to fix and reduce all abnormalities to 
                # 0 (hopefully).
                fline = line
                line = line.strip().split()

                if line[1] in ["A:", "B:", "S?:", "S:", "A;"]:
                    # different labelling schemes on second token
                    if line[1] in ["A:", "A;"]:
                        yield ("A", " ".join(line[2:]))
                    elif line[1] == "B:":
                        yield ("B", " ".join(line[2:]))
                    else:
                        self._THROWN_OUT_LINES_S += 1
                        continue
                elif line[0] in ["A:", "B:", "S?:"]: 
                    # no line number, just speaker
                    if line[0] == "A:":
                        yield ("A", " ".join(line[1:]))
                    elif line[0] == "B:":
                        yield ("B", " ".join(line[1:]))
                    else:
                        self._THROWN_OUT_LINES_S += 1
                        continue
                elif re.search(r"[0-9]{1,3}[AB]{1}\:{1}", line[0]):
                    # combined number and speaker with ':'
                    if "A" in line[0]:
                        yield ("A", " ".join(line[1:]))
                    else:
                        yield ("B", " ".join(line[1:]))
                elif re.search(r"[0-9]{1,3}\s{1,2}[ABS]{1}\s{1}", fline):
                    # line number, space (1 or 2), A|B|S, space
                    # probably a better way to do this... but
                    for c in fline:
                        if c == "A":
                            yield ("A", " ".join(line[2:]))
                        elif c == "B":
                            yield ("B", " ".join(line[2:]))
                        else:
                            self._THROWN_OUT_LINES_S += 1
                        continue
                    









