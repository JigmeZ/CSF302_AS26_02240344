"""
Lab 7 - Question 3
Dijkstra, Kruskal, and Prim algorithms.

An edge is written as (weight, first_vertex, second_vertex).
"""

import heapq
import random
import time


def dijkstra(graph, start):
    """Find shortest distances from start in a graph with non-negative edges."""
    distance = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distance[start] = 0
    heap = [(0, start)]
    visited = set()

    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if vertex in visited:
            continue
        visited.add(vertex)

        for neighbour, weight in graph[vertex]:
            if neighbour in visited:
                continue
            new_distance = current_distance + weight
            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = vertex
                heapq.heappush(heap, (new_distance, neighbour))

    return distance, previous


def make_path(previous, start, end):
    """Create the path from start to end using the previous-vertex table."""
    path = []
    while end is not None:
        path.append(end)
        if end == start:
            return path[::-1]
        end = previous[end]
    return []  # The vertex cannot be reached.


class UnionFind:
    """A simple structure used by Kruskal to detect cycles."""

    def __init__(self, number_of_vertices):
        self.parent = list(range(number_of_vertices))

    def find(self, vertex):
        while vertex != self.parent[vertex]:
            vertex = self.parent[vertex]
        return vertex

    def join(self, first, second):
        first = self.find(first)
        second = self.find(second)
        if first == second:
            return False
        self.parent[second] = first
        return True


def kruskal(number_of_vertices, edges):
    """Return the edges and total weight of a minimum spanning tree."""
    sets = UnionFind(number_of_vertices)
    tree = []

    for weight, first, second in sorted(edges):
        if sets.join(first, second):
            tree.append((first, second, weight))

    total = sum(weight for _, _, weight in tree)
    return tree, total


def prim(number_of_vertices, edges):
    """Return the edges and total weight of a minimum spanning tree."""
    graph = [[] for _ in range(number_of_vertices)]
    for weight, first, second in edges:
        graph[first].append((weight, second))
        graph[second].append((weight, first))

    tree = []
    visited = {0}
    heap = [(weight, 0, neighbour) for weight, neighbour in graph[0]]
    heapq.heapify(heap)

    while heap and len(visited) < number_of_vertices:
        weight, first, second = heapq.heappop(heap)
        if second in visited:
            continue

        visited.add(second)
        tree.append((first, second, weight))

        for next_weight, neighbour in graph[second]:
            if neighbour not in visited:
                heapq.heappush(heap, (next_weight, second, neighbour))

    total = sum(weight for _, _, weight in tree)
    return tree, total


def random_graph(number_of_vertices, extra_edges):
    """Make a connected random undirected graph."""
    edges = []
    used_edges = set()

    # First connect every vertex, so the graph is definitely connected.
    for vertex in range(1, number_of_vertices):
        parent = random.randrange(vertex)
        edges.append((random.randint(1, 100), parent, vertex))
        used_edges.add(tuple(sorted((parent, vertex))))

    # Add more edges.
    wanted_edges = number_of_vertices - 1 + extra_edges
    while len(edges) < wanted_edges:
        first, second = random.sample(range(number_of_vertices), 2)
        edge = tuple(sorted((first, second)))
        if edge not in used_edges:
            used_edges.add(edge)
            edges.append((random.randint(1, 100), first, second))

    return edges


def main():
    # ---------------- Dijkstra ----------------
    graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: [],
    }

    distance, previous = dijkstra(graph, 0)
    print("Dijkstra from vertex 0:")
    for vertex in graph:
        print(vertex, "distance =", distance[vertex],
              "path =", make_path(previous, 0, vertex))

    # ---------------- MST algorithms ----------------
    edges = [(4, 0, 1), (1, 0, 2), (2, 1, 2),
             (5, 1, 3), (8, 2, 3)]

    print("\nKruskal total weight:", kruskal(4, edges)[1])
    print("Prim total weight:   ", prim(4, edges)[1])

    for _ in range(100):
        test_edges = random_graph(20, 30)
        assert kruskal(20, test_edges)[1] == prim(20, test_edges)[1]
    print("Random MST test: 100/100 passed")

    # Dijkstra is not suitable for negative edges.
    bad_graph = {
        0: [(1, 10), (2, 1)],
        1: [(2, -20)],
        2: [],
    }
    wrong_distance = dijkstra(bad_graph, 0)[0][2]
    print("\nNegative-edge example:")
    print("Dijkstra returns", wrong_distance,
          "but the correct distance is -10.")

    # Timing: sparse graph has about 3V edges; dense graph has about V^2/4.
    for name, extra_edges in [("sparse", 2 * 1000),
                              ("dense", 250000 - 1000 + 1)]:
        test_edges = random_graph(1000, extra_edges)

        start = time.perf_counter()
        kruskal(1000, test_edges)
        kruskal_time = time.perf_counter() - start

        start = time.perf_counter()
        prim(1000, test_edges)
        prim_time = time.perf_counter() - start

        print(name, "graph: Kruskal =", round(kruskal_time, 3),
              "seconds, Prim =", round(prim_time, 3), "seconds")


if __name__ == "__main__":
    main()
