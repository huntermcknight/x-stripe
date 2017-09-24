# Hunter McKnight
# KRCourse 2017

import numpy as np

def extract():
    """
    (None) -> np.array

    Given a .txt of 49151 minimal 9x9 sudoku puzzles and their solutions,
    export the puzzles into a numpy array.

    Modified from Bryan Park's script to extract puzzles from his sudoku dataset
    on Kaggle.

    https://www.kaggle.com/bryanpark/sudoku

    Dataset created by Sandy Gordon at UWA.

    http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php
    """

    # Test only an x or stripe sudoku
    # n_sudokus = 3
    # puzzles = np.zeros((n_sudokus, 81), np.int32)
    # for i, line in enumerate(open('stripe_test_sudoku.csv', 'r').read().splitlines()[1:]):
    # for i, line in enumerate(open('x_test_sudoku.csv', 'r').read().splitlines()):
    puzzles = np.zeros((49151, 81), np.int32)
    for i, line in enumerate(open('sudoku17.txt', 'r').read().splitlines()):
        for j, p in enumerate(line):
            puzzles[i, j] = p
    puzzles = puzzles.reshape((-1, 9, 9))
    return puzzles

def compress(puzzle):
    """
    (np.array) -> str

    Given a puzzle or solution as an np.array, rewrite the array
    as a single line of text suitable for storing in a .csv file.
    """

    puzzle_str = ''

    for row in puzzle:
        for col in row:
            puzzle_str += str(col)

    return puzzle_str


def encode(puzzle):
    """
    (np.array) -> [[int]]

    Given a sudoku puzzle formatted as a numpy array, output the cnf
    associated with the puzzle's givens.
    """

    cnf = []

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                # the proposition that the cell in row i, column j
                # takes this value becomes a unit clause
                cnf.append([i * 81 + j * 9 + puzzle[i][j]])

    return cnf

def encode_all(puzzles):
    """
    (np.array) -> [[[int]]]

    Given an array of sudoku puzzles formatted as numpy arrays, output a list
    of cnfs associated with the puzzles' givens.
    """

    cnfs = []

    for puzzle in puzzles:
        cnfs.append(encode(puzzle))

    return cnfs

def decode(var_list):
    """
    ([str]) -> np.array

    Given a zchaff model for a satisfiable puzzle, return the solution as
    """

    solution = np.zeros((9, 9), np.int32)

    for var in var_list:
        # negative clauses tell us what numbers don't go in a cell
        # we only care what numbers actually are in a cell
        var = int(var)
        if var > 0:
            cell = ((var - 1) % 9) + 1
            col = ((var - cell) % 81) // 9
            row = ((var - col * 9 - cell)) // 81

            solution[row][col] = cell

    return solution
