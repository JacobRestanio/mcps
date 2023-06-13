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

    # objective
    model += lp.lpSum(X.values())

    # constraints
    for n in node_list:
        model += (lp.lpSum([x for (u, v), x in X.items() if (u, v) in nx.edges(graph, nbunch=n)]) <= 2, f"{n}")

    status = model.solve(lp.PULP_CBC_CMD(msg=False, timeLimit=1800))

    for (u, v), x in X.items():
        if x.value() == 0:
            C.update([(u, v)])

    return C


def main():
    with open("mcps_linprog_pulp.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"test, size, linprog size, linprog time\n")

    for tree_size in [10, 100, 1000, 10000]:
        for iteration in range(1000):
            tree = nx.random_tree(tree_size)

            st = time.process_time()
            linprog_mcps = find_mcps(tree)
            linprog_time = time.process_time() - st
            linprog_size = len(linprog_mcps)

            with open("mcps_linprog_pulp.txt", "a") as file:
                file.write(f"{iteration+1}, {tree_size}, {linprog_size}, {linprog_time}\n")


if __name__ == "__main__":
    main()
