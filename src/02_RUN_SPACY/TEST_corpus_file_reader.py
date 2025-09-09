

from corpus_file_reader import CorpusFileReader

_file = "/Users/burnt/SPITE/CODE/noah_work/Noah_Thesis_Work/data/CCOT/WORK/22-232_231-S.txt"
cfp = CorpusFileReader(_file)

print("FILE: " + _file)

line = cfp.next_line()

while line:
    print(line)
    line = cfp.next_line()



