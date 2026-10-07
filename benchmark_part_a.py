"""Empirical timing for part (a).

This measures Dijkstra's algorithm when:
    1. the graph is stored as an adjacency matrix, and
    2. the priority queue is implemented as a simple array scan.

Run:
    python benchmark_part_a.py
"""

from argparse import ArgumentParser
from math import inf
from random import Random
from statistics import median
from time import perf_counter

from dijkstra_matrix_array import NO_EDGE, dijkstra


def make_random_matrix(number_of_vertices, density, seed):
    """Create a reachable directed graph as an adjacency matrix.

    density is approximately E / (V * (V - 1)).
    A simple chain is added first so that every vertex is reachable from 0.
    """
    rng = Random(seed)
    graph = [[NO_EDGE] * number_of_vertices for _ in range(number_of_vertices)]

    for vertex in range(number_of_vertices):
        graph[vertex][vertex] = 0

    edges = set()

    for vertex in range(number_of_vertices - 1):
        graph[vertex][vertex + 1] = rng.randint(1, 20)
        edges.add((vertex, vertex + 1))

    possible_edges = number_of_vertices * (number_of_vertices - 1)
    target_edges = max(len(edges), int(possible_edges * density))

    while len(edges) < target_edges:
        start = rng.randrange(number_of_vertices)
        end = rng.randrange(number_of_vertices)

        if start == end or (start, end) in edges:
            continue

        graph[start][end] = rng.randint(1, 20)
        edges.add((start, end))

    return graph, len(edges)


def time_one_graph(number_of_vertices, density, repeats, seed):
    """Return median running time for one graph size."""
    graph, number_of_edges = make_random_matrix(number_of_vertices, density, seed)
    timings = []

    for _ in range(repeats):
        start_time = perf_counter()
        dijkstra(graph, source=0)
        end_time = perf_counter()
        timings.append(end_time - start_time)

    return number_of_edges, median(timings)


def run_benchmark(sizes, density, repeats):
    print(f"Density target: {density}")
    print(f"Repeats per size: {repeats}")
    print()
    print("V,E,E/(V*(V-1)),median_seconds,microseconds_per_V_squared")

    for index, number_of_vertices in enumerate(sizes):
        number_of_edges, seconds = time_one_graph(
            number_of_vertices=number_of_vertices,
            density=density,
            repeats=repeats,
            seed=1000 + index,
        )
        possible_edges = number_of_vertices * (number_of_vertices - 1)
        actual_density = number_of_edges / possible_edges
        microseconds_per_v_squared = seconds * 1_000_000 / (number_of_vertices**2)

        print(
            f"{number_of_vertices},"
            f"{number_of_edges},"
            f"{actual_density:.4f},"
            f"{seconds:.6f},"
            f"{microseconds_per_v_squared:.4f}"
        )


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=[50, 100, 200, 400, 800],
        help="vertex counts to test",
    )
    parser.add_argument(
        "--density",
        type=float,
        default=0.20,
        help="approximate edge density between 0 and 1",
    )
    parser.add_argument(
        "--repeats",
        type=int,
        default=5,
        help="number of runs per graph size",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    run_benchmark(args.sizes, args.density, args.repeats)
