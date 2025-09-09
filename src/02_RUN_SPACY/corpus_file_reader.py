


import sys



class CorpusFileReader:
    """
    This class reads the cleaned up corpus files. It returns line-by-line data for the actual
    conversation, and can return the '<>' surrounded metadata as well if needed. 

    Processes metadata on calls to get_metadata() and removes the speaker/line-number 
    information for lines.

    """

    def __init__(self, _file):
        self._METADATA = None
        self._FILE = _file
        self._CORPUS_FILE = open(_file, "rt")
        self._GENERATOR = None
        


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
            while True:
                if len(line) > 0 and line.strip()[0] == "<":
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

    def next_line(self):
        """
        Gets the next line in the file, or returns None if there are no more lines.

        Returns:
            (str|None): the next line in the file
        """
        # doing this with a generator, but obfuscating for readability
        if self._GENERATOR is None:
            self._GENERATOR = self._get_generator()
        try:
            return next(self._GENERATOR)
        except StopIteration:
            return None
       

    def _get_generator(self):
        """
        Gets the next non-empty, non-metadata line from the file

        Returns:
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
                full_line = line
                line = line.strip().split()

                if line[1] in ["A:", "B:", "S?:", "S:", "A;"]:
                    # different labelling schemes on second token
                    yield " ".join(line[2:])
                elif line[0] in ["A:", "B:", "S?:"]: 
                    # no line number, just speaker
                    yield " ".join(line[1:])
                elif re.search(r"[0-9]{1,3}[AB]{1}\:{1}", line[0]):
                    # combined number and speaker with ':'
                    yield " ".join(line[1:])
                elif re.search(r"[0-9]{1,3}\s{1,2}[ABS]{1}\s{1}", fline):
                    # line number, space (1 or 2), A|B|S, space
                    yield " ".join(line[2:])
                    









