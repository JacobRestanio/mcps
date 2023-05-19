import networkx as nx
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

    # Apply reduction rule 4
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
        file.write(f"test, size, divconq size, divconq time\n")

    for tree_size in [10, 100, 1000, 10000, 100000, 1000000]:
        for iteration in range(1000):
            tree = nx.random_tree(tree_size)

            st = time.process_time()
            divconq_mcps = find_mcps(tree, tree.copy(), 0)
            divconq_time = time.process_time() - st
            divconq_size = len(divconq_mcps)

            with open("mcps_divconq.txt", "a") as file:
                file.write(f"{iteration+1}, {tree_size}, {divconq_size}, {divconq_time}\n")


if __name__ == "__main__":
    main()
