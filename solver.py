# Hunter McKnight
# KRCourse 2017

import subprocess

def solve(clauses):
    """
    ([[int]]) -> [str]

    Given a cnf formatted as a numpy array, submit the cnf
    to zchaff and return zchaff's output as a list of strings.

    Modified from David Musicant's original script
    https://github.com/FatTony746/clueReasoner/blob/master/SATSolver.py
    """
    # create a cnf file to pass to zchaff
    maxVar = 0
    for clause in clauses:
        for literal in clause:
            maxVar = max(abs(literal),maxVar)
    out = open('query.cnf','w')
    print('c This DIMACS format CNF file was generated by solver.py', file = out)
    print('c Do not edit.', file = out)
    print('p cnf',maxVar,len(clauses), file = out)
    for clause in clauses:
        for literal in clause:
            print(literal, end = ' ', file = out)
        print('0', file = out)
    out.close();

    # pass the cnf file to zchaff
    process = subprocess.Popen('/usr/local/zchaff64/zchaff query.cnf',stdout=subprocess.PIPE,
                shell=True, universal_newlines=True)
    # if necessary, change the preceding path name to point
    # to zchaff on your machine
    process.wait()
    stdout = process.stdout
    result = stdout.read().split()
    stdout.close()

    return result

def get_metrics(result):
    """
    ([str]) -> (bool, int, int, int)

    Read zchaff output and return the instance satisfiability,
    Max Decision Level, Num. of Decisions, and Added Conflict Clauses.
    """

    sat = False
    level = 0
    decisions = 0
    conflicts = 0

    words = iter(result)
    try:
        while next(words) != 'Level':
            pass
        level = int(next(words))
        while next(words) != 'Decisions':
            pass
        decisions = int(next(words))
        while next(words) != 'Conflict':
            pass
        # we have one more string to get out of the way, 'Clauses'
        next(words)
        conflicts = int(next(words))
        while str(next(words)) != 'RESULT:':
            pass
        answer = str(next(words))
        if answer == 'SAT':
            sat = True
        elif answer == 'UNSAT':
            sat = False
        else:
            print("Error: SAT/UNSAT not indicated.")
    except StopIteration:
            print("Error: Unexpected file end.")

    return (sat, level, decisions, conflicts)

def get_solution(result):
    """
    ([str]) -> [str]

    Read zchaff output for a satisfiable instance and
    return a list of satisfying variable assignments.
    """

    var_list = []

    words = iter(result)
    try:
        while next(words) != 'Satisfiable':
            pass
        var = next(words)
        while var != 'Random':
            var_list.append(var)
            var = next(words)
    except StopIteration:
            print("Error: Unexpected file end.")

    return var_list
