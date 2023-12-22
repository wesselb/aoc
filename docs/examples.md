# Examples


## Compute a Shortest Path on a Board

Suppose that `input.txt` has the following contents:

```
S.....
.##..#
.#....
.#.###
.#...E
```

We would like to find the shortest path from `S` to `E`.
You can do this in the following way:

```python
import aoc

R, C, board = aoc.read_board("input.txt")

start, end = aoc.find_in_board(board, "S", "E")

dist, prev = aoc.shortest_path(start, aoc.neighbours(board, allowed={".", "E"}))

print(dist[end])
```

