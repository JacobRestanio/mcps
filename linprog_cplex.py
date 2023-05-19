import pulp as lp
import networkx as nx
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
    file.write(f"test, size, cplex size, cplex time\n")

    for tree_size in [10, 100, 1000, 10000]:
        for iteration in range(1000):
            tree = nx.random_tree(tree_size)

            st = time.process_time()
            cplex_mcps = find_mcps(tree)
            cplex_time = time.process_time() - st
            cplex_size = len(cplex_mcps)

            file.write(f"{iteration+1}, {tree_size}, {cplex_size}, {cplex_time}\n")

    file.close()


if __name__ == "__main__":
    main()
