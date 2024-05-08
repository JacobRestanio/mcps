import networkx as nx
import tracemalloc
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
        file.write(f"test, size, maxflow size, maxflow time, maxflow mem\n")

    for tree_size in [10, 100, 1000, 10000]:
        for i in range(1000):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            tracemalloc.start()
            st = time.time()
            maxflow_mcps = find_mcps(tree)
            maxflow_time = time.time() - st
            maxflow_size = len(maxflow_mcps)
            current, maxflow_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            with open("mcps_max_flow.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {maxflow_size}, {maxflow_time}, {maxflow_mem}\n")


if __name__ == "__main__":
    main()
