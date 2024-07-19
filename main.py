# import linprog_pulp as solver
import linprog_cplex as solver
import iterative_recursive as iter_rec
import maxflow
import networkx as nx
import tracemalloc
import datetime
import time
import sys


def is_path_set(G, cps):
    g = G.copy()
    g.remove_edges_from(cps)
    for v in list(g.nodes):
        if g.degree(v) > 2:
            return False

    return True


def main():
    sys.setrecursionlimit(10000000)
    date = datetime.datetime.now()
    with open("mcps_results.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, recursive, iterative, maxflow, cplex\n")
    with open("mcps_time.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, recursive, iterative, maxflow, cplex\n")
    with open("mcps_memory.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, recursive, iterative, maxflow, cplex\n")

    for tree_size in [100, 1000, 10000, 100000]:
        for i in range(100):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            rec_tree = tree.copy()
            iter_tree = tree.copy()
            maxflow_tree = tree.copy()
            solver_tree = tree.copy()

            tracemalloc.start()
            st = time.time()
            rec_mps = iter_rec.find_mps_recursive(rec_tree)
            rec_time = time.time() - st
            current, rec_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            iter_mps = iter_rec.find_mps_iterative(iter_tree)
            iter_time = time.time() - st
            current, iter_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            maxflow_mcps = maxflow.find_mcps(maxflow_tree)
            maxflow_time = time.time() - st
            current, maxflow_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            if (tree_size > 1000):
                solver_mcps = []
                solver_time = None
                solver_mem = None
            else:
                tracemalloc.start()
                st = time.time()
                solver_mcps = solver.find_mcps(solver_tree)
                solver_time = time.time() - st
                current, solver_mem = tracemalloc.get_traced_memory()
                tracemalloc.stop()

            with open("mcps_results.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {len(rec_mps)}, {len(iter_mps)} {len(maxflow_mcps)}, {len(solver_mcps)}\n")
            with open("mcps_time.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {rec_time}, {iter_time}, {maxflow_time}, {solver_time}\n")
            with open("mcps_memory.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {rec_mem}, {iter_mem}, {maxflow_mem}, {solver_mem}\n")


if __name__ == "__main__":
    main()
