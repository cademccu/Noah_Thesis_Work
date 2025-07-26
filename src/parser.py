

import spacy
import sys




class Conversation:
    
    def __init__(self, filename):
        self._FILENAME = filename
        self._METADATA = ""
        self._LINES = []
        self._TOKENIZED_LINES = {}
        self.nlp = spacy.load("en_core_web_lg")

    def set_metadata(self, metadata):
        """
        Sets the objects metadata parameters
        """
        self._METADATA = metadata

    def set_lines(self, lines):
        """
        sets the lines object, a list of lines in the conversation
        """
        self._LINES = lines
        # make tokenized lines by label
        for line in self._LINES:
            self._TOKENIZED_LINES[line[0:line.index(":") + 1]] = self.nlp(line)

        for key, value in self._TOKENIZED_LINES.items():
            print(key)
        
    def read_file(self):
        """
        Reads the metadata and data lines into seperate, parseable objects
        """
        with open(self._FILENAME, "rt") as f:
            metadata = ""
            line = f.readline()
            # metadata
            while line:
                if line[0] == "<":
                    metadata += line
                else:
                    break
                line = f.readline()

            self.set_metadata(metadata)
            lines = []
            # read actual lines of text from document
            while line:
                if len(line) > 2:
                    lines.append(line)
                line = f.readline()

            self.set_lines(lines)

convo1 = Conversation("../data/02010_02172_C_UNTAGGED.txt")
convo1.read_file()

# rint(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)


