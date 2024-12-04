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
R, C, board = aoc.read_board(lines)

start, end = aoc.find_in_board(board, "S", "E")

dist, prev = aoc.shortest_path(start, aoc.neighbours(board, allowed={".", "E"}))

print("Distance:", dist[end])

# Mark the shortest path with `P`, but not marking the start and end.
n = end
while True:
    n = prev[n]
    if n == start: 
        break
    else:
        board[n] = "P"

print()
aoc.print_board(board)
```

Output:

```text
Distance: 11

SPPP..
.##P.#
.#PP..
.#P###
.#PPPE
```

