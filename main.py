import linprog_pulp as pulp
import linprog_cplex as cplex
import divconq
import networkx as nx
import time
import datetime


def is_path_set(G, cps):
    g = G.copy()
    g.remove_edges_from(cps)
    for v in list(g.nodes):
        if g.degree(v) > 2:
            return False

    return True


def main():
    num_different = 0
    with open("mpcsoutput.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"test, tree size, divconq size, divconq time, pulp size, pulp time, cplex size, cplex time\n")

    for tree_size in [10, 100, 1000, 10000]:
        for i in range(100):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            st = time.time()
            divconq_mcps = divconq.find_mcps(tree, tree.copy(), 0)
            divconq_time = time.time() - st
            divconq_size = len(divconq_mcps)

            st = time.time()
            pulp_mcps = pulp.find_mcps(tree)
            pulp_time = time.time() - st
            pulp_size = len(pulp_mcps)

            st = time.time()
            cplex_mcps = cplex.find_mcps(tree)
            cplex_time = time.time() - st
            cplex_size = len(cplex_mcps)

            with open("mpcsoutput.txt", "a") as file:
                file.write(
                    f"{i+1}, {tree_size}, {divconq_size}, {divconq_time:.5f}, {pulp_size}, {pulp_time:.5f}, {cplex_size}, {cplex_time:.5f}\n"
                )


if __name__ == "__main__":
    main()
