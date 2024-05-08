import networkx as nx
import tracemalloc
import time
import datetime
import sys


def find_mcps(G, T, r, parent=None):
    # Let S be the neighbors of the root
    S = list(G[r])
    has_parent = 0
    if parent or parent == 0:
        S.remove(parent)
        has_parent = 1

    # Let C be the MCPS
    C = set()

    # Reduction rules 1
    if G.degree(r) - has_parent == 0:
        return C

    # Recurse on subtrees rooted at vertices in S
    for s in S:
        C.update(find_mcps(G, T, s, r))

    # Apply reduction rule 2
    for s in S:
        if T.degree(s) == 3:
            C.update([(r, s)])
            T.remove_edge(r, s)

    # Apply reduction rule 3
    if T.degree(r) - has_parent >= 3:
        edges_to_add = T.degree(r) - has_parent - 2
        for s in S:
            if edges_to_add > 0 and T.has_edge(r, s):
                C.update([(r, s)])
                T.remove_edge(r, s)
                edges_to_add -= 1

    return C


def main():
    sys.setrecursionlimit(10000)
    with open("mcps_divconq.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"test, size, divconq size, divconq time, divconq mem\n")

    for tree_size in [10, 100, 1000, 10000]:
        for i in range(1000):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            tracemalloc.start()
            st = time.time()
            divconq_mcps = find_mcps(tree, tree.copy(), 0)
            divconq_time = time.time() - st
            divconq_size = len(divconq_mcps)
            current, divconq_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            with open("mcps_divconq.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {divconq_size}, {divconq_time}, {divconq_mem}\n")


if __name__ == "__main__":
    main()
