## MCPS Tree Implementation
Implementation of various algorithms for the maximum co-path set problem in trees.

# Dependencies
You must have python3 installed https://www.python.org/downloads/.

The project requires the following libraries:
- networkx
- PuLP
    pip install networkx
    pip install pulp

The results cited are from using a CPLEX solver. If you do not have CPLEX, change from using the linprog_cplex.py file to using linprog_pulp.py. PuLP includes a free solver.

To rerun the experiments, simply run the main file `python3 ./main.py`
