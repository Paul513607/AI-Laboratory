def parse(filename):
    file = open(filename, "r")
    size_str = file.readline()
    size = int(size_str[size_str.find("=") + 2:])
    blocked_positions = []
    line = file.readline()
    index = line.find("[") + 1
    index1 = line.find(',')
    num1 = int(line[index + 1:index1]) - 1
    index2 = line.find(']')
    num2 = int(line[index1 + 1:index2]) - 1
    if 0 <= num1 < size and 0 <= num2 < size:
        blocked_positions.append((num1, num2))

    while line:
        line = file.readline()
        if line == ']':
            break

        index = line.find("[")
        index2 = line.find(',')
        index1 = line.find(',')
        num1 = int(line[index + 1:index1]) - 1
        index2 = line.find(']')
        num2 = int(line[index1 + 1:index2]) - 1
        if 0 <= num1 < size and 0 <= num2 < size:
            blocked_positions.append((num1, num2))

    return size, blocked_positions