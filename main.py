# import linprog_pulp as solver
import linprog_cplex as solver
import divconq
import maxflow
import networkx as nx
import tracemalloc
import datetime
import time


def is_path_set(G, cps):
    g = G.copy()
    g.remove_edges_from(cps)
    for v in list(g.nodes):
        if g.degree(v) > 2:
            return False

    return True


def main():
    date = datetime.datetime.now()
    with open("mcps_results.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, divconq, maxflow, cplex\n")
    with open("mcps_time.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, divconq, maxflow, cplex\n")
    with open("mcps_memory.txt", "w") as file:
        file.write(f"{date}\n")
        file.write(f"test, size, divconq, maxflow, cplex\n")

    for tree_size in [10, 100, 1000, 10000]:
        for i in range(1000):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            tracemalloc.start()
            st = time.time()
            divconq_mcps = divconq.find_mcps(tree, tree.copy(), 0)
            divconq_time = time.time() - st
            current, divconq_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            maxflow_mcps = maxflow.find_mcps(tree)
            maxflow_time = time.time() - st
            current, maxflow_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            solver_mcps = solver.find_mcps(tree)
            solver_time = time.time() - st
            current, solver_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            with open("mcps_results.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {len(divconq_mcps)}, {len(maxflow_mcps)}, {len(solver_mcps)}\n")
            with open("mcps_time.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {divconq_time}, {maxflow_time}, {solver_time}\n")
            with open("mcps_memory.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {divconq_mem}, {maxflow_mem}, {solver_mem}\n")


if __name__ == "__main__":
    main()
