# Hunter McKnight
# KRCourse 2017

import numpy as np

def extract():
    """
    () -> np.array

    Given a .csv of 1,000,000 standard 9x9 sudoku puzzles and their solutions,
    export the puzzles into a numpy array.

    Modified from Bryan Park's script to extract puzzles from his sudoku dataset.
    """
    puzzles = np.zeros((1000000, 81), np.int32)
    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:]):
        puzzle, solution = line.split(",")
        for j, p in enumerate(puzzle):
            puzzles[i, j] = p
    puzzles = puzzles.reshape((-1, 9, 9))
    return puzzles

def encode(puzzle):
    """
    (np.array) -> str

    Given a sudoku puzzle formatted as a numpy array, output the DIMACS cnf
    associated with the puzzle's givens. This cnf does not encode the general
    rules of sudoku, nor does it have a header. Those will be added at a later
    processing step.
    """

    cnf = ""

    for i in range(9):
        for j in range(9):
            if puzzle[i][j] != 0:
                # the proposition that the cell in row i, column j
                # takes this value becomes a unit clause
                cnf += str(i * 81 + j * 9 + puzzle[i][j]) + " 0\n"

    return cnf

def encode_all(puzzles):
    """
    (np.array) -> [str]

    Given an array of sudoku puzzles formatted as numpy arrays, output a list
    of DIMACS cnfs associated with the puzzles' givens. These cnfs do not
    encode the general rules of sudoku, nor do they have headers. Those will be
    added at a later processing step.
    """

    cnfs = []

    for puzzle in puzzles:
        cnfs.append(encode(puzzle))

    return cnfs

