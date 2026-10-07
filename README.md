# SC2001 Lab 2 - Part (a)

## Question

Suppose the input graph `G = (V, E)` is stored in an adjacency matrix and an array is used for the priority queue. Implement Dijkstra's algorithm using this setting and analyze its time complexity theoretically and empirically.

## Files

- `dijkstra_matrix_array.py`: readable implementation of Dijkstra's algorithm.
- `benchmark_part_a.py`: empirical timing script for different graph sizes.

## How the Graph Is Stored

The graph is stored as a square matrix.

```python
graph[u][v]
```

means the edge weight from vertex `u` to vertex `v`.

If there is no edge from `u` to `v`, the matrix stores:

```python
math.inf
```

This avoids confusion between "no edge" and a real edge with weight `0`.

## How the Priority Queue Works

The priority queue is implemented using a normal array-style scan.

At every step, the algorithm searches through all vertices and chooses the unvisited vertex with the smallest current distance. This is simple to understand, but it is slower than a binary heap for large sparse graphs.

## Theoretical Time Complexity

Let:

- `|V|` be the number of vertices.
- `|E|` be the number of edges.

Using an array priority queue:

- Extracting the minimum-distance vertex takes `O(|V|)` time because all vertices are scanned.
- This extraction happens up to `|V|` times.
- Therefore, the priority queue part costs `O(|V|^2)`.

Using an adjacency matrix:

- When a vertex is selected, the algorithm scans its whole matrix row to check every possible neighbour.
- Each row has `|V|` entries.
- This happens up to `|V|` times.
- Therefore, the neighbour-checking part also costs `O(|V|^2)`.

So the total time complexity is:

```text
O(|V|^2) + O(|V|^2) = O(|V|^2)
```

If the matrix must first be built from an edge list, creating the matrix takes `O(|V|^2 + |E|)` time. However, once the matrix is already given, the Dijkstra run itself is `O(|V|^2)`.

The important point is that this version does not become much faster when the graph is sparse. Even if `|E|` is small, the adjacency matrix still forces the algorithm to scan many "no edge" entries.

## Space Complexity

The adjacency matrix stores `|V| * |V|` entries, so the graph storage is:

```text
O(|V|^2)
```

The algorithm also keeps arrays for distance, previous vertex, and visited state:

```text
O(|V|)
```

Therefore, the total space complexity is dominated by the matrix:

```text
O(|V|^2)
```

## Running the Code

Run the example:

```bash
python dijkstra_matrix_array.py
```

Run the benchmark:

```bash
python benchmark_part_a.py
```

You can also choose your own graph sizes:

```bash
python benchmark_part_a.py --sizes 100 200 400 800 1600 --density 0.20 --repeats 5
```

## Empirical Analysis

The benchmark generates reachable random directed graphs and measures the median running time for each graph size.

The value `microseconds_per_V_squared` is useful because this algorithm is expected to grow approximately with `|V|^2`. If the theoretical analysis is correct, this value should stay roughly in the same range as `|V|` increases.

For sparse graphs, increasing `|V|` still causes about quadratic growth because the adjacency matrix scans all possible neighbour positions, not only the real edges.

### Sample Result 1: Increasing `|V|`

Command used:

```bash
python benchmark_part_a.py --sizes 50 100 200 400 800 --density 0.20 --repeats 5
```

Measured results:

| `|V|` | `|E|` | Density | Median seconds | Microseconds / `|V|^2` |
|---:|---:|---:|---:|---:|
| 50 | 490 | 0.2000 | 0.000516 | 0.2065 |
| 100 | 1980 | 0.2000 | 0.001740 | 0.1740 |
| 200 | 7960 | 0.2000 | 0.007557 | 0.1889 |
| 400 | 31920 | 0.2000 | 0.031368 | 0.1961 |
| 800 | 127840 | 0.2000 | 0.061817 | 0.0966 |

The running time generally increases as `|V|` increases. The normalized value, microseconds per `|V|^2`, remains in the same broad range, which supports the theoretical `O(|V|^2)` analysis.

### Sample Result 2: Changing `|E|` While Keeping `|V|` Fixed

Commands used:

```bash
python benchmark_part_a.py --sizes 600 --density 0.02 --repeats 7
python benchmark_part_a.py --sizes 600 --density 0.20 --repeats 7
python benchmark_part_a.py --sizes 600 --density 0.60 --repeats 7
```

Measured results:

| `|V|` | `|E|` | Density | Median seconds | Microseconds / `|V|^2` |
|---:|---:|---:|---:|---:|
| 600 | 7188 | 0.0200 | 0.104025 | 0.2890 |
| 600 | 71880 | 0.2000 | 0.067536 | 0.1876 |
| 600 | 215640 | 0.6000 | 0.077887 | 0.2164 |

Although `|E|` increases greatly, the timing remains in the same order of magnitude. This happens because the adjacency matrix version scans all `|V|^2` possible edge positions whether those edges exist or not. Normal computer timing can be noisy, so the exact numbers may not increase perfectly, but the overall trend matches the theory: `|V|` is the main factor for this implementation.
