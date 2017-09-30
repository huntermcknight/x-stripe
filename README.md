# Comparative Difficulty of X-Sudoku and Sudoku Stripe
Sudoku SAT-solver experiment for UvA MasterAI Knowledge Representation course

X-sudoku is a variation of sudoku demanding both main diagonals of the puzzle contain the digits 1-9. Sudoku stripe is a variation 
demanding that the digits 1-9 appear in ascending or descending order in at least one row, column, or region. We hypothesize that 
sudoku stripe is generally more difficult for a SAT solver than x-sudoku in terms of search depth and number of decisions required 
to determine whether a given puzzle has a model. (For more detailed motivation and explication of this hypothesis, see our report.)

This repository contains scripts to parse puzzle datasets, encode/decode sudoku puzzles and rules, and interact with SAT solvers.

## Getting Started
### Scripts
Scripts are written in Python for version 3.5.2. The following packages are also used: numpy, math, csv, itertools, pycosat, sys, 
subprocess.

### Dataset
For convenience, the dataset we used in our experiment is included in this repository as sudoku17.txt. This dataset was provided
by Dr. Gordon Royle at the University of Western Australia. For more information about Dr. Royle's website, see his website (link
in acknowledgments). If you choose a different dataset, be sure to modify the filepath for the method extract() in the script 
extract.py.

### Solvers
For our experiment, we used zChaff (version 2007.3.12, 64 bit) and Armin Biere's CaDiCaL (version sc17). These are not included in 
the repository and must be installed separately (links in acknowledgments). If necessary, modify the filepaths in the solve() method 
of solver.py to match the locations of these solvers on your machines. If you choose different solvers, the other scripts in solver.py 
used to parse solver output may need to be modified as well.

### Running the experiment
To run the experiment with zChaff, simply execute
```
python xstripe.py
```
To run the experiment with CaDiCaL, execute
```
python xstripe.py cadical
```
Results will be stored in the new files metrics.csv, x-solutions.csv, and stripe-solutions.csv.

## Authors
Hunter McKnight and Caitlin Lagrand

## Acknowledgements
* Dr. Frank van Harmelen, professor
* Finn Potason, teaching assistant
* Dr. Gordon Royle, for providing dataset (http://staffhome.ecm.uwa.edu.au/~00013890/sudokumin.php)
* Princeton University, for creating and maintaining zChaff (https://www.princeton.edu/~chaff/zchaff.html)
* Dr. Armin Biere, for creating and maintaining CaDiCaL (https://github.com/arminbiere/cadical)
* Brian Park at Kaggle and David Musicant, whose code inspired parts of extract.py and solver.py
