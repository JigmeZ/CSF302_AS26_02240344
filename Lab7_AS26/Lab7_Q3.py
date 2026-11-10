"""
Lab 7 - Question 3: Dijkstra, Kruskal, and Prim.

Graph file format: first line ``V E`` followed by E lines ``u v weight``.
Vertices are numbered 0 through V-1.  Dijkstra treats edges as directed;
the MST functions treat their input edges as undirected.
"""

import heapq
import random
import time


def dijkstra(graph, source):
    distance = {vertex: float("inf") for vertex in graph}
    previous = {vertex: None for vertex in graph}
    distance[source] = 0
    heap = [(0, source)]
    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if current_distance != distance[vertex]:
            continue
        for neighbour, weight in graph[vertex]:
            new_distance = current_distance + weight
            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = vertex
                heapq.heappush(heap, (new_distance, neighbour))
    return distance, previous


def path_to(previous, source, target):
    path = []
    while target is not None:
        path.append(target)
        if target == source:
            return path[::-1]
        target = previous[target]
    return []


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, value):
        while value != self.parent[value]:
            self.parent[value] = self.parent[self.parent[value]]
            value = self.parent[value]
        return value

    def union(self, first, second):
        first, second = self.find(first), self.find(second)
        if first == second:
            return False
        if self.rank[first] < self.rank[second]:
            first, second = second, first
        self.parent[second] = first
        if self.rank[first] == self.rank[second]:
            self.rank[first] += 1
        return True


def kruskal(vertices, edges):
    chosen = []
    sets = UnionFind(vertices)
    for weight, first, second in sorted(edges):
        if sets.union(first, second):
            chosen.append((first, second, weight))
    return chosen, sum(edge[2] for edge in chosen)


def prim(vertices, edges):
    graph = [[] for _ in range(vertices)]
    for weight, first, second in edges:
        graph[first].append((weight, second))
        graph[second].append((weight, first))
    chosen = []
    visited = {0}
    heap = [(weight, 0, neighbour) for weight, neighbour in graph[0]]
    heapq.heapify(heap)
    while heap and len(visited) < vertices:
        weight, first, second = heapq.heappop(heap)
        if second in visited:
            continue
        visited.add(second)
        chosen.append((first, second, weight))
        for next_weight, neighbour in graph[second]:
            if neighbour not in visited:
                heapq.heappush(heap, (next_weight, second, neighbour))
    return chosen, sum(edge[2] for edge in chosen)


def random_connected_graph(vertices, extra_edges):
    edges = []
    used = set()
    for vertex in range(1, vertices):
        parent = random.randrange(vertex)
        weight = random.randint(1, 100)
        edges.append((weight, parent, vertex))
        used.add(tuple(sorted((parent, vertex))))
    while len(edges) < vertices - 1 + extra_edges:
        first, second = random.sample(range(vertices), 2)
        pair = tuple(sorted((first, second)))
        if pair not in used:
            used.add(pair)
            edges.append((random.randint(1, 100), first, second))
    return edges


def main():
    graph = {0: [(1, 4), (2, 1)], 1: [(3, 1)], 2: [(1, 2), (3, 5)],
             3: []}
    distances, previous = dijkstra(graph, 0)
    print("Dijkstra from vertex 0:")
    for vertex in graph:
        print(vertex, "distance =", distances[vertex],
              "path =", path_to(previous, 0, vertex))

    edges = [(4, 0, 1), (1, 0, 2), (2, 1, 2), (5, 1, 3), (8, 2, 3)]
    print("\nKruskal MST weight:", kruskal(4, edges)[1])
    print("Prim MST weight:   ", prim(4, edges)[1])

    for _ in range(100):
        test_edges = random_connected_graph(20, 30)
        assert kruskal(20, test_edges)[1] == prim(20, test_edges)[1]
    print("Random MST verification: 100/100 tests passed")

    negative_graph = {0: [(1, 2), (2, 5)], 1: [(2, -10)], 2: []}
    print("\nNegative-edge warning:")
    print("Dijkstra gives", dijkstra(negative_graph, 0)[0][2],
          "for 0 -> 2, but the correct answer is -8.")

    for extra in (2 * 1000, 250000 - 1000 + 1):
        edges = random_connected_graph(1000, extra)
        start = time.perf_counter()
        kruskal(1000, edges)
        kruskal_time = time.perf_counter() - start
        start = time.perf_counter()
        prim(1000, edges)
        prim_time = time.perf_counter() - start
        label = "sparse" if extra == 2000 else "dense"
        print(label, "graph: Kruskal =", round(kruskal_time, 3),
              "s, Prim =", round(prim_time, 3), "s")


if __name__ == "__main__":
    main()