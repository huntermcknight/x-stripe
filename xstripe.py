# Hunter McKnight
# KRCourse 2017

import csv
from extract import extract, encode_all, compress, decode
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

    metrics = get_metrics(result)

    if metrics[0]:
        solution = get_solution(result)
        if (DEBUG):
            sat_to_sudoku(solution, 9, 9, 9)
    else:
        solution = ''

    return metrics, solution

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
    puzzle_cnfs = encode_all(puzzles[:100])
    print('Encoded.')

    print('Encoding rules for x-sudoku...')
    x_rules = encode_sudoku(9, 9, 9, x = True)
    print('Encoded.')
    print('Encoding rules for sudoku stripe...')
    stripe_rules = encode_sudoku(9, 9, 9, stripe = True)
    print('Encoded.')

    count_valid_x = 0
    count_valid_stripe = 0
    count_valid_both = 0
    x_comparison_metrics = []
    stripe_comparison_metrics = []
    x_solutions = []
    stripe_solutions = []

    print('Solving puzzles...')
    for i in range(len(puzzle_cnfs)):
        x_metrics, x_solution = solve_as(puzzle_cnfs[i], x_rules)

        if x_metrics[0]:
            count_valid_x += 1
            x_solutions.append((compress(puzzles[i]), compress(decode(x_solution))))

        stripe_metrics, stripe_solution = solve_as(puzzle_cnfs[i], stripe_rules)

        if stripe_metrics[0]:
            count_valid_stripe += 1
            stripe_solutions.append((compress(puzzles[i]), compress(decode(stripe_solution))))
            if x_metrics[1]:
                count_valid_both += 1
        x_comparison_metrics.append(x_metrics)
        #stripe_comparison_metrics.append(stripe_metrics)

        # print a progress update for every 10% completed
        if (i + 1) % (len(puzzle_cnfs) // 10) == 0:
            print(str((i + 1) // (len(puzzle_cnfs) // 10)) + '0%...')
            print(str(count_valid_x) + ' puzzles solvable as x-sudoku')
            print(str(count_valid_stripe) + ' puzzles solvable as sudoku stripe')
            print(str(count_valid_both) + ' puzzles solvable both ways')
    print('Solved.')

    print('Writing metrics to metrics.csv...')
    with open('metrics.csv', mode = 'w') as output:
        csv_output = csv.writer(output)
        csv_output.writerow(('x_satisfiable', 'x_max_level', 'x_num_decisions', 'x_conflicts'))
        for row in x_comparison_metrics:
            csv_output.writerow(row)
        # TODO: print sudoku stripe metrics
    print('Written.')

    print('Writing solutions to x-solutions.csv...')
    with open('x-solutions.csv', mode = 'w') as solutions:
        csv_output = csv.writer(solutions)
        for pair in x_solutions:
            csv_output.writerow(pair)
    print('Written')

    print('Writing solutions to stripe-solutions.csv...')
    with open('stripe-solutions.csv', mode = 'w') as solutions:
        csv_output = csv.writer(solutions)
        for pair in stripe_solutions:
            csv_output.writerow(pair)
    print('Written')


if __name__ == '__main__':
    main()
