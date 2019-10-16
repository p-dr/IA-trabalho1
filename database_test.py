import depth_first_search as dfs
import breadth_first_search as bfs
import best_first as bf
import a_star as a
from search_test import test_search
from gen_boards import read_boards
import pandas as pd
from pathlib import Path
from copy import deepcopy
from sys import argv

boards_dir = Path('board_database')
out_dir = Path('test_summaries')

search_algs = (dfs, bfs, bf, a)
names = ('DFS', 'BFS', 'Best_first', 'A*')
if '--all' in argv:
    file_list = boards_dir.glob('*')
elif len(argv) == 1:
    print('Provide board database files to test on or --all option.')
    exit()
else:
    file_list = argv[1:]

for boards_file in file_list:
    print('\nCURRENT DATABASE:', boards_file.name)
    summary = pd.DataFrame()
    raw_boards = read_boards(boards_file)

    for s, name in zip(search_algs, names):
        print('\nUsing method:', name)
        search_data = pd.DataFrame()
        boards = deepcopy(raw_boards)

        for i, board in enumerate(boards):
            print(f'Searching on board {i}...', end='\r')
            search_res = test_search(board, s.search, only_stats=True)
            search_data = search_data.append(search_res, ignore_index=True)

        # print(search_data.isna().sum())
        s_means = search_data.mean()
        summary = pd.concat([summary, s_means], axis=1, sort=True)

    summary.columns = names
    summary.to_csv(out_dir/(boards_file.stem + '.tsv'), sep='\t')
    print(summary)
