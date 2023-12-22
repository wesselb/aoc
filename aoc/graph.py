from queue import PriorityQueue
from typing import Callable, Iterator, TypeVar

__all__ = ["shortest_path"]


Node = TypeVar("Node")


def shortest_path(
    start: Node,
    nbs: Callable[[Node], Iterator[tuple[Node, float]]],
    callback: Callable[[Node, float], bool] = lambda n, d: False,
) -> tuple[dict[Node, float], dict[Node, Node]]:
    """Dijkstra's algorithm to compute all shortest paths starting at `start`.

    Args:
        start (Node): Start.
        nbs (Callable[[Node], Iterator[tuple[Node, float]]]): A function that
            takes in a node and iterates over all neighbours, giving tuples containing
            the neighbour and the weight of the edge to that neighbour. The weights
            must be non-negative.
        callback (Callable[[Node, float], bool], optional): A function that is called at
            every iteration with the current node and the true shortest path distance to
            that node. If this function returns `True`, the algorithm will stop.
            Otherwise, the algorithm will continue.

    Returns:
        tuple[dict[Node, float], dict[Node, Node]]:
            * For every node, the shortest path distance to that node.
            * For every node except `start`, the previous node in the shortest path to
                that node.
    """
    dist = {start: 0}
    prev = {}
    seen = set()

    q = PriorityQueue()
    q.put((0, start))

    while not q.empty():
        d1, n1 = q.get()

        # This needs to execute first to ensure that `d1` is right.
        if n1 in seen:
            continue
        seen.add(n1)

        if callback(n1, d1):
            break

        for n2, w12 in nbs(n1):
            assert w12, f"Weight must be non-negative: {w12}."

            if n2 in seen:
                continue

            alt = d1 + w12
            if alt < dist.get(n2, float("inf")):
                dist[n2] = alt
                prev[n2] = n1
                q.put((dist[n2], n2))

    return dist, prev
