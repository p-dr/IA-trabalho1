def readFile(filename: str):
    """ Lê o arquivo 'filename' e retorna uma tupla com os
    obstáculos, a origem e o destino para cada labirinto do arquivo """
    with open(filename, 'r') as file:
        while True:
            obstacles = set()
            rows = file.readline().split(' ')[0]
            if not rows:
                break
            for i in range(int(rows)):
                line = file.readline()[:-1]
                for j in range(len(line)):
                    char = line[j]
                    if char == '-':
                        obstacles.add((i, j))
                    elif char == '#':
                        origin = (i, j)
                    elif char == '$':
                        target = (i, j)
            yield (obstacles, origin, target)
