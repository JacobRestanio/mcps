import networkx as nx
import matplotlib.pyplot as plt
import time
import datetime


def find_mcps(tree):
    s = -1
    t = -2
    R, S = nx.bipartite.sets(tree)
    flow_vertices = [s] + [t] + list(R) + list(S)
    flow_edges = []
    for i in R:
        for j in tree[i]:
            flow_edges.append((i, j))

    f = nx.DiGraph()
    f.add_nodes_from(flow_vertices)

    # Connect s to R, S to t, and add flow edges
    f.add_edges_from([(s, i) for i in R], capacity=2)
    f.add_edges_from([(j, t) for j in S], capacity=2)
    f.add_edges_from(flow_edges, capacity=1)

    flow_value, flow_dict = nx.maximum_flow(f, s, t)

    mcps = [(i, j) for (i, j) in flow_edges if flow_dict[i][j] == 0]
    return mcps


def main():
    with open("mcps_max_flow.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"test, size, bmatching size, bmatching time\n")

    for tree_size in [10, 100, 1000, 10000]:
        for iteration in range(1000):
            tree = nx.random_tree(tree_size)

            st = time.time()
            bmatching_mcps = find_mcps(tree)
            bmatching_time = time.time() - st
            bmatching_size = len(bmatching_mcps)

            with open("mcps_max_flow.txt", "a") as file:
                file.write(f"{iteration+1}, {tree_size}, {bmatching_size}, {bmatching_time}\n")


if __name__ == "__main__":
    main()
