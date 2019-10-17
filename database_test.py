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
    mean_outpath = summaries_dir/('mean_' + outfname)

    if mean_outpath.exists() and ('-r' not in argv):
        print(f'"{str(boards_file)}" exists on filesystem. Add -r to overwrite.')
        continue

    print('\nCURRENT DATABASE:', boards_file.name, '\n')
    std_outpath = summaries_dir/('std_' + outfname)
    summary_mean = pd.DataFrame()
    summary_std = pd.DataFrame()

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
        s_stds = search_data.std()
        summary_mean = pd.concat([summary_mean, s_means], axis=1, sort=True)
        summary_std = pd.concat([summary_std, s_stds], axis=1, sort=True)

    ### SAVE SUMMARIES
    summary_mean.columns = names
    summary_std.columns = names
    summary_mean.to_csv(mean_outpath, sep='\t')
    summary_std.to_csv(std_outpath, sep='\t')
    print('MEANS')
    print(summary_mean)
    print('STANDARD DEVS.')
    print(summary_std)
