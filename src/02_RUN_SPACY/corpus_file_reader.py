


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
       

    def next(self):
        """
        Gets the next non-empty, non-metadata line from the file

        Returns:
            (str|None) Returns the next non-empty, non-metadata line
        """
        
        # this is lazy but im not engineering here, sorry yeild!
        line = self._CORPUS_FILE.readline()
        while line:
            if len(line.strip()) == 0:
                line = self._CORPUS_FILE.readline()
                continue
            elif line.strip()[0] == "<":
                # metadata line
                line = self._CORPUS_FILE.readline()
                continue
            else:
                # lines have some bs associated with them
                line = line.strip()
                if line # TODO HERE <logic for trimming line numbers here...>
        # if it reaches here, it was EOF
        return None








