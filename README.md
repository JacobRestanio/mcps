# MPS Tree Implementation
Implementation of various algorithms for the maximum path set problem in trees.

## Dependencies
You must have python 3 installed:  
https://www.python.org/downloads/.

The project requires the following libraries:
- networkx
- PuLP

To install those libraries, use pip.  
`pip install networkx`  
`pip install pulp`

The results cited are from using a CPLEX solver. If you do not have CPLEX installed on your machine, change the import in main.py from linprog_cplex to linprog_pulp.

## Running the Experiments
To rerun the experiments, run the main file `python ./main.py`

Each algorithm can be run individually as well, e.g. `python ./divcong.py`
