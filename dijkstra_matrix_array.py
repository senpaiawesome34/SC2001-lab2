"""Dijkstra's algorithm using an adjacency matrix and an array priority queue.

Graph representation:
    graph[u][v] is the weight of the edge from vertex u to vertex v.
    math.inf means there is no edge.
    graph[u][u] should normally be 0.

Priority queue representation:
    The "queue" is represented by the visited[] array.
    To extract the next closest vertex, we scan all vertices linearly.
"""

from math import inf


NO_EDGE = inf


def find_closest_unvisited(distance, visited):
    """Return the unvisited vertex with the smallest known distance."""
    closest_vertex = None
    closest_distance = inf

    for vertex in range(len(distance)):
        if not visited[vertex] and distance[vertex] < closest_distance:
            closest_vertex = vertex
            closest_distance = distance[vertex]

    return closest_vertex


def dijkstra(graph, source):
    """Find shortest paths from source to all vertices in graph.

    Returns:
        distance: distance[v] is the shortest distance from source to v.
        previous: previous[v] is the vertex before v on the shortest path.
    """
    number_of_vertices = len(graph)
    check_graph(graph, source)

    distance = [inf] * number_of_vertices
    previous = [None] * number_of_vertices
    visited = [False] * number_of_vertices

    distance[source] = 0

    for _ in range(number_of_vertices):
        current = find_closest_unvisited(distance, visited)

        if current is None:
            break

        visited[current] = True

        for neighbour in range(number_of_vertices):
            weight = graph[current][neighbour]

            if visited[neighbour] or weight == NO_EDGE:
                continue

            new_distance = distance[current] + weight

            if new_distance < distance[neighbour]:
                distance[neighbour] = new_distance
                previous[neighbour] = current

    return distance, previous


def build_path(previous, source, destination):
    """Rebuild one shortest path from source to destination."""
    path = []
    current = destination

    while current is not None:
        path.append(current)

        if current == source:
            path.reverse()
            return path

        current = previous[current]

    return []


def check_graph(graph, source):
    """Check for common input mistakes before running the algorithm."""
    number_of_vertices = len(graph)

    if source < 0 or source >= number_of_vertices:
        raise ValueError("source must be a valid vertex index")

    for row in graph:
        if len(row) != number_of_vertices:
            raise ValueError("graph must be a square adjacency matrix")

        for weight in row:
            if weight != NO_EDGE and weight < 0:
                raise ValueError("Dijkstra's algorithm cannot use negative weights")


def demo():
    """Small example that can be run with: python dijkstra_matrix_array.py"""
    graph = [
        [0, 10, 3, NO_EDGE, NO_EDGE],
        [NO_EDGE, 0, 1, 2, NO_EDGE],
        [NO_EDGE, 4, 0, 8, 2],
        [NO_EDGE, NO_EDGE, NO_EDGE, 0, 7],
        [NO_EDGE, NO_EDGE, NO_EDGE, 9, 0],
    ]

    source = 0
    distance, previous = dijkstra(graph, source)

    print("Source vertex:", source)
    print("Shortest distances:", distance)

    for destination in range(len(graph)):
        path = build_path(previous, source, destination)
        print(f"Path to {destination}: {path}")


if __name__ == "__main__":
    demo()
