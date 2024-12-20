# Examples


## Compute a Shortest Path on a Board

Suppose that `input.txt` has the following contents:

```text
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

lines = aoc.read_lines("input.txt")
R, C, board = aoc.parse_board(lines)

start, end = aoc.find_in_board(board, "S", "E")

dist, prev = aoc.shortest_path(start, aoc.neighbours(board, allowed={".", "E"}))

print("Distance:", dist[end])

# Find a shortest path and mark it with `P`.
path = aoc.backtrace(end, prev)[0]

print()
aoc.print_board(board, marks={"P": path})
```

Output:

```text
Distance: 11

PPPP..
.##P.#
.#PP..
.#P###
.#PPPP
```

