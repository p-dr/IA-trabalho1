def readFile(filename: str) -> tuple:
    """ Lê o arquivo 'filename' e retorna uma tupla com os
    obstáculos, a origem e o destino do tabuleiro """
    obstacles = []
    with open(filename) as file:
        # ignora a primeira linha e os newlines no final de cada linha
        lines = file.read().splitlines()[1:]
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            char = lines[i][j]
            if char == '-':
                obstacles.append((i, j))
            elif char == '#':
                origin = (i, j)
            elif char == '$':
                target = (i, j)
    return (obstacles, origin, target)
