import networkx as nx
import tracemalloc
import datetime
import time
import sys
from matplotlib import pyplot as plt


def find_mps_recursive(T):
    children = []
    siblings = [0]
    distance = 0
    nodes_by_distance = {}
    while True:
        nodes_by_distance[distance] = siblings
        for s in siblings:
            T.nodes[s]['distance'] = distance
            children = [ *children, *[ c for c in list(T[s]) if not 'distance' in T.nodes[c] ] ]
        siblings = children.copy()
        children = []
        if not siblings:
            break
        distance += 1

    P = set()
    P.update(mps_recursion(T, nodes_by_distance, distance))
    return P


def mps_recursion(T, nodes_by_distance, max_distance):
    P = set()
    while not nodes_by_distance[max_distance]:
        max_distance -= 1
        if max_distance == -1:
            return P
    l = nodes_by_distance[max_distance][0]
    nodes_by_distance[max_distance].remove(l)
    
    # Reduction Rule 1
    if len(T) <= 1:
        return P
    
    p = list(T[l])[0]
    p_neighbors = list(T[p])

    # Reduction Rule 2
    if len(p_neighbors) <= 2:
        P.update([(p, l)])
        T.remove_node(l)
        P.update(mps_recursion(T, nodes_by_distance, max_distance))

    # Reduction Rule 3
    else:
        p_neighbors.remove(l)
        p_leaves = [ n for n in p_neighbors if T.nodes[n]['distance'] > T.nodes[p]['distance'] ]
        j = p_leaves[0]
        p_leaves.remove(j)
        P.update([(p, l)])
        P.update([(p, j)])
        nodes_by_distance[T.nodes[j]['distance']].remove(j)
        nodes_by_distance[T.nodes[p]['distance']].remove(p)
        for n in p_leaves:
            nodes_by_distance[T.nodes[n]['distance']].remove(n)
        T.remove_node(l)
        T.remove_node(j)
        T.remove_node(p)
        T.remove_nodes_from(p_leaves)
        P.update(mps_recursion(T, nodes_by_distance, max_distance))

    return P


def find_mps_iterative(T):
    P = set()
    root = 0
    edges = nx.bfs_edges(T, root)
    nodes = [root] + [v for u, v in edges]
    nodes.reverse()
    
    for n in nodes:
        if not n in T:
            continue
        if len(T) <= 1:
            break
        p = list(T[n])[0]
        p_neighbors = list(T[p])
        if len(p_neighbors) <= 2:
            P.update([(p, n)])
            T.remove_node(n)
        elif len(p_neighbors) >= 3:
            p_leaves = [l for l in p_neighbors if len(list(T[l])) == 1]
            p_leaves.remove(n)
            j = p_leaves[0]
            P.update([(p, n)])
            P.update([(p, j)])
            T.remove_node(n)
            T.remove_node(p)
            T.remove_nodes_from(p_leaves)

    return P



def main():
    sys.setrecursionlimit(100000)
    with open("mps_iterative_recursive.txt", "w") as file:
        file.write(f"{datetime.datetime.now()}\n")
        file.write(f"test, size, rec_mps_size, rec_time, rec_mem (bytes), iter_mps_size, iter_time, iter_mem (bytes)\n")

    for tree_size in [10, 100, 1000, 10000, 100000]:
        for i in range(1):
            print(f"test #{i+1}, size {tree_size}")
            tree = nx.random_tree(tree_size)

            rec_tree = tree.copy()
            iter_tree = tree.copy()

            tracemalloc.start()
            st = time.time()
            rec_mps = find_mps_recursive(rec_tree)
            rec_time = time.time() - st
            rec_size = len(rec_mps)
            current, rec_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tracemalloc.start()
            st = time.time()
            iter_mps = find_mps_iterative(iter_tree)
            iter_time = time.time() - st
            iter_size = len(iter_mps)
            current, iter_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            with open("mps_iterative_recursive.txt", "a") as file:
                file.write(f"{i+1}, {tree_size}, {rec_size}, {rec_time}, {rec_mem}, {iter_size}, {iter_time}, {iter_mem}\n")


if __name__ == "__main__":
    main()


