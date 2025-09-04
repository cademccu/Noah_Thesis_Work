


def liner(line):
    print(line)
    while "(" in line and ")" in line:
        p_start = line.index("(") 
        depth = 0
        for i in range(p_start + 1, len(line)):
            if line[i] == ")" and depth == 0:
                line = line[:p_start] + line[i + 1:]
                break
            elif line[i] == ")" and depth > 0:
                depth -= 1
            elif line[i] == "(":
                depth += 1
    print(line)    

