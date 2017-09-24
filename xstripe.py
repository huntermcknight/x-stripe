# Hunter McKnight
# KRCourse 2017

import csv
from extract import extract, encode_all
from solver import *
from sat_encoding import encode_sudoku, sat_to_sudoku

DEBUG = True

def solve_as(puzzle, rules):
    """
    ([[int]], [[int]]) -> bool, (int, int, int)

    Solve the given puzzle as according to the given
    rules and return the most relevant zchaff output:
    satisfiability and solver metrics.
    """

    full_cnf = rules + puzzle

    result = solve(full_cnf)
    if (DEBUG and is_sat(result)):
        sat_to_sudoku(result[17:17+9*9*9], 9, 9, 9)

    return is_sat(result), get_metrics(result)

def main():
    """
    (None) -> None

    Try to solve a database of puzzles as both x-sudoku
    and sudoku stripes. Print a file of solution metrics.
    """

    print('Extracting puzzles from sudoku.csv...')
    puzzles = extract()
    print('Extracted.')
    # for testing purposes, use only the first 100 puzzles
    # for experiment, use all puzzles
    print('Encoding puzzles as cnfs...')
    puzzle_cnfs = encode_all(puzzles)
    print('Encoded.')

    print('Encoding rules for x-sudoku...')
    x_rules = encode_sudoku(9, 9, 9, x = True)
    print('Encoded.')
    print('Encoding rules for sudoku stripe...')
    stripe_rules = encode_sudoku(9, 9, 9, stripe = True)
    print('Encoded.')

    count_valid_x = 0
    count_valid_stripe = 0
    x_comparison_metrics = []
    stripe_comparison_metrics = []

    print('Solving puzzles...')
    for i in range(len(puzzle_cnfs)):
        is_sat_x, x_metrics = solve_as(puzzle_cnfs[i], x_rules)

        if is_sat_x:
            count_valid_x += 1

        is_sat_stripe, stripe_metrics = solve_as(puzzle_cnfs[i], stripe_rules)

        if is_sat_stripe:
            count_valid_stripe += 1

        # if (is_sat_x and is_sat_stripe):
        x_comparison_metrics.append(x_metrics)
            # stripe_comparison_metrics.append(stripe_metrics)
        # print a progress update for every 10% completed
        # if (i + 1) % (len(puzzle_cnfs) // 10) == 0:
        #     print(str((i + 1) // (len(puzzle_cnfs) // 10)) + '0%...')
    print('Solved.')

    print(str(count_valid_x) + ' puzzles solvable as x-sudoku')
    print(str(count_valid_stripe) + ' puzzles solvable as sudoku stripe')
    print(str(len(stripe_comparison_metrics)) + ' puzzles solvable both ways')


    print('Writing metrics to metrics.csv...')
    with open('metrics.csv', mode = 'w') as output:
        csv_output = csv.writer(output)
        csv_output.writerow(('x_max_level', 'x_num_decisions', 'x_conflicts'))
        for row in x_comparison_metrics:
            csv_output.writerow(row)
        # TODO: print sudoku stripe metrics
    print('Written.')


if __name__ == '__main__':
    main()
