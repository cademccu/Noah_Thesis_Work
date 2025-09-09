import csv 

def lines(path):
    with open(path, 'r', newline='') as f:
        for line in csv.reader(f):
            yield line

from pathlib import Path
Path("file.txt").write_text("a,1,2\nb,20,40") 

gen = lines("file.txt")
print(next(gen))
print(next(gen))
print(next(gen))
