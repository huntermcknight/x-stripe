#!/usr/bin/env

'''
Caitlin Lagrand
SAT encoding for sudoku puzzles
TODO:
    encode rules for sudoku stripe
'''

import math
import numpy as np
import pycosat

def create_variables(n_rows, n_columns, n_numbers):
    ''' Create (n_rows x n_columns x n_numbers) variables that
        represent the tiles of the sudoku with all possible values. '''
    variables = np.zeros([n_rows, n_columns, n_numbers], dtype = np.int)
    for i in range(n_rows):
        for j in range(n_columns):
            for k in range(n_numbers):
                variables[i][j][k] = i*n_columns*n_numbers + j*n_numbers + k +1
    return variables


def each_cell(variables):
    ''' Encode the rules for each cell must contain exactly one number. '''
    columns = variables.shape[0]
    rows = variables.shape[1]
    numbers = variables.shape[2]
    enc = []
    for row in range(rows):
        for column in range(columns):
            one_number = []
            for number in range(numbers):
                # Each cell has to be filled with one number
                one_number += [int(variables[row][column][number])]
                # Each cell can only contain one number
                for n in range(number + 1, numbers):
                        enc += [[int(-1 * variables[row][column][number]),
                                 int(-1 * variables[row][column][n])]]
            enc += [one_number]
    return enc


def each_row(variables):
    ''' Encode the rules for each number can only occur once per row. '''
    columns = variables.shape[0]
    rows = variables.shape[1]
    numbers = variables.shape[2]
    enc = []
    for row in range(rows):
        for number in range(numbers):
            one_number = []
            for column in range(columns):
                # Each number must occur at least once per row
                one_number += [int(variables[row][column][number])]
                # Each number can only occur once per row
                for c in range(column + 1, columns):
                        enc += [[int(-1 * variables[row][column][number]),
                                 int(-1 * variables[row][c][number])]]
            enc += [one_number]
    return enc


def each_column(variables):
    ''' Encode the rules for each number can only occur once per column. '''
    columns = variables.shape[0]
    rows = variables.shape[1]
    numbers = variables.shape[2]
    enc = []
    for column in range(columns):
        for number in range(numbers):
            one_number = []
            for row in range(rows):
                # Each number must occur at least once per column
                one_number += [int(variables[row][column][number])]
                # Each number can only occur once per column
                for r in range(row + 1, rows):
                        enc += [[int(-1 * variables[row][column][number]),
                                 int(-1 * variables[r][column][number])]]
            enc += [one_number]
    return enc


def each_block(variables):
    ''' Encode the rules for each number can only occur once per block. '''
    columns = variables.shape[0]
    rows = variables.shape[1]
    numbers = variables.shape[2]
    # If square root is not an integer, skip block rules
    if ((not math.sqrt(columns).is_integer())
         or (not math.sqrt(rows).is_integer())): return []
    enc = []
    for row in range(int(math.sqrt(rows))):
        for column in range(int(math.sqrt(columns))):
            for number in range(numbers):
                one_number = []
                for r_block in range(int(math.sqrt(rows))):
                    for c_block in range(int(math.sqrt(columns))):
                        # Each number must occur at least once per block
                        one_number += [int(variables[row*int(math.sqrt(rows))
                                       + r_block][column*int(math.sqrt(columns))
                                       + c_block][number])]
                        # Each number can only occur once per block
                        for r in range(r_block + 1, int(math.sqrt(rows))):
                            for c in range(c_block + 1, int(math.sqrt(columns))):
                                    enc += [[int(-1 * variables[row*int(math.sqrt(rows)) + r_block][column*int(math.sqrt(columns)) + c_block][number]),
                                             int(-1 * variables[row*int(math.sqrt(rows)) + r][column*int(math.sqrt(columns)) + c][number])]]
                enc += [one_number]
    return enc


def each_diagonal(variables):
    ''' Encode the rules for each number can only occur once per diagonal. '''
    columns = variables.shape[0]
    rows = variables.shape[1]
    numbers = variables.shape[2]
    enc = []
    for index in range(rows):
        one_number = []
        for number in range(numbers):
            # Each number must occur at least once per diagonal
            # Left top - right bottom
            one_number += [int(variables[index][index][number])]
            # Right top - left bottom
            one_number += [int(variables[index][columns-1-index][number])]
            # Each number can only occur once per diagonal
            for i in range(index + 1, rows):
                    # Left top - right bottom
                    enc += [[int(-1 * variables[index][index][number]),
                             int(-1 * variables[i][i][number])]]
                    # Right top - left bottom
                    enc += [[int(-1 * variables[index][columns-1-index][number]),
                             int(-1 * variables[i][columns-1-i][number])]]
        enc += [one_number]
    return enc


def sat_to_sudoku(sat_sudoku, n_rows, n_columns, n_numbers):
    ''' Pretty print the solution of the sudoku found by the SAT sovler.
        TODO: print the horizontal bar better for 16x16.'''
    if sat_sudoku == "UNSAT":
        print("UNSAT")
        return
    for row in range(n_rows):
        r = row * n_columns * n_numbers
        printing_row = []
        for column in range(n_columns):
            c = r + column * n_numbers
            for number in range(n_numbers):
                n = c + number
                if sat_sudoku[n] > 0:
                    print('{:^4}'.format(str(number + 1)), end="")
            if (column+1) % math.sqrt(n_columns) == 0 and column < n_columns-1:
                print("| ", end="")
        print("\n")
        if (row+1) % math.sqrt(n_rows) == 0 and row < n_rows - 1:
            print('{:-^4}'.format((n_numbers + 4)* '---'))


def encode_sudoku(n_rows, n_columns, n_numbers, x=False, stripe=False):
    ''' Encode a (n_rows x n_columns x n_numbers) sudoku. '''
    variables = create_variables(n_rows, n_columns, n_numbers)
    encoded = each_cell(variables)
    encoded += each_row(variables)
    encoded += each_column(variables)
    encoded += each_block(variables)
    if (x):
        encoded += each_diagonal(variables)
    return encoded


def to_DIMACS(encoding, name, number_variables):
    ''' Convert the encoding to the DIMACS format.
        c [filename]
        c
        p cnf [number_variables] [number_clauses]
        clause_1
        ...
        clause_n'''
    DIMACS_encoding = "c " + name + "\nc \n"
    number_clauses = len(encoding)
    DIMACS_encoding += "p cnf " + str(number_variables) + " " + \
                        str(number_clauses) + "\n"
    for clause in encoding:
        for literal in clause:
            DIMACS_encoding += (str(literal) + " ")
        DIMACS_encoding += "0\n"
    return DIMACS_encoding


def main():
    # 3x3 sudoku example
    encode_sudoku3 = encode_sudoku(3, 3, 3)
    sat_sudoku3 = pycosat.solve(encode_sudoku3)
    sat_to_sudoku(sat_sudoku3, 3, 3, 3)
    print(to_DIMACS(encode_sudoku3, "sudoku3.cnf", 3*3*3))

    # 9x9 sudoku example
    encode_sudoku9 = encode_sudoku(9, 9, 9, True)
    sat_sudoku9 = pycosat.solve(encode_sudoku9)
    sat_to_sudoku(sat_sudoku9, 9, 9, 9)

    # 16x16 sudoku example
    encode_sudoku16 = encode_sudoku(16, 16, 16)
    sat_sudoku16 = pycosat.solve(encode_sudoku16)
    sat_to_sudoku(sat_sudoku16, 16, 16, 16)


if __name__ == "__main__":
    main()
