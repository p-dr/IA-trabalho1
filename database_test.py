from utils import search_algs, names
from search_test import test_search
from gen_boards import read_boards

import pandas as pd
from pathlib import Path
from copy import deepcopy
from sys import argv

boards_dir = Path('board_database')
out_dir = Path('test_out')
summaries_dir = out_dir/'summaries'

if '--all' in argv:
    file_list = boards_dir.glob('*')
elif len(argv) == 1:
    print('Provide board database files to test on or --all option.')
    exit()
else:
    file_list = (Path(f) for f in argv[1:])

for boards_file in file_list:
    outfname = boards_file.stem + '.tsv'
    outpath = summaries_dir/outfname

    if outpath.exists() and ('-r' not in argv):
        print(f'"{str(boards_file)}" exists on filesystem. Add -r to overwrite.')
        continue

    print('\nCURRENT DATABASE:', boards_file.name, '\n')
    summary = pd.DataFrame()

    for s, name in zip(search_algs, names):
        print('Using method:', name)
        search_data = pd.DataFrame()

        raw_boards = read_boards(boards_file)
        for i, raw_board in enumerate(raw_boards):
            print(f'Searching on board {i}...', end='\r')
            board = deepcopy(raw_board)
            search_res = test_search(board, s.search, only_stats=True)
            search_data = search_data.append(search_res, ignore_index=True)
        print('Done.' + ' ' * 50)

        ### SAVE SEARCH DATA
        search_data.to_csv(out_dir/name/outfname, sep='\t')
        s_means = search_data.mean()
        summary = pd.concat([summary, s_means], axis=1, sort=True)

    ### SAVE SUMMARY
    summary.columns = names
    summary.to_csv(outpath, sep='\t')
    print(summary)
