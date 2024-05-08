import pulp as lp
import networkx as nx
import tracemalloc
import time
import datetime


def find_mcps(G):
    graph = G.copy()
    node_list = list(graph.nodes)
    edge_list = list(graph.edges)
    C = set()

    model = lp.LpProblem(name="mps-problem", sense=lp.LpMaximize)

    # decision variables
    X = {(i, j): lp.LpVariable(name=f"x_({i},{j})", lowBound=0, upBound=1) for (i, j) in edge_list}

    # objective function
    model += lp.lpSum(X.values())

    # constraints
    for n in node_list:
        model += (lp.lpSum([x for (u, v), x in X.items() if (u, v) in nx.edges(graph, nbunch=n)]) <= 2, f"c_{n}")

    status = model.solve(lp.CPLEX_CMD(msg=False, timeLimit=1800))

    for (u, v), x in X.items():
        if x.value() == 0:
            C.update([(u, v)])

    return C


def main():
    file = open("mcps_linprog_cplex.txt", "w")
    file.write(f"{datetime.datetime.now()}\n")
    file.write(f"test, size, cplex size, cplex time, cplex mem\n")

    for tree_size in [10, 100, 1000, 10000]:
        for i in range(1000):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            tracemalloc.start()
            st = time.time()
            cplex_mcps = find_mcps(tree)
            cplex_time = time.time() - st
            cplex_size = len(cplex_mcps)
            current, cplex_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            file.write(f"{i+1}, {tree_size}, {cplex_size}, {cplex_time}, {cplex_mem}\n")

    file.close()


if __name__ == "__main__":
    main()
