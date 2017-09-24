# Hunter McKnight
# KRCourse 2017

import numpy as np

def extract():
    """
    (None) -> np.array

    Given a .csv of 1,000,000 standard 9x9 sudoku puzzles and their solutions,
    export the puzzles into a numpy array.

    Modified from Bryan Park's script to extract puzzles from his sudoku dataset.
    """
    # Test only an x or stripe sudoku
    n_sudokus = 3
    puzzles = np.zeros((n_sudokus, 81), np.int32)
    for i, line in enumerate(open('stripe_test_sudoku.csv', 'r').read().splitlines()[1:]):
    # for i, line in enumerate(open('x_test_sudoku.csv', 'r').read().splitlines()):
    # puzzles = np.zeros((1000000, 81), np.int32)
    # for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
        puzzle, solution = line.split(",")
        for j, p in enumerate(puzzle):
            puzzles[i, j] = p
    puzzles = puzzles.reshape((-1, 9, 9))
    return puzzles

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
