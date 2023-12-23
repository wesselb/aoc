from queue import PriorityQueue, Queue
from typing import Callable, Dict, Iterator, Optional, Set, Tuple, TypeVar

__all__ = ["shortest_path"]


Node = TypeVar("Node")


def shortest_path(
    start: Node,
    nbs: Callable[[Node], Iterator[Tuple[Node, float]]],
    callback: Callable[[Node, float], bool] = lambda n, d: False,
    heuristic: Callable[[Node], float] = lambda n: 0,
    revisit: bool = False,
    seen: Optional[Set[Node]] = None,
) -> Tuple[Dict[Node, float], Dict[Node, Node]]:
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
        heuristic (Callable[[Node], float], optional): An heuristic that needs to lower
            bounds the distance to the end node. It should also be monotonic, meaning
            that it never decreases by more than the edge weight. If it is not
            monotonic, you should set `revisit` to `True` to still find the optimal
            path.
        revisit (bool, optional): Allow the algorithm to revisit the same node more
            then once. Defaults to `False`.
        seen (set[Node], optional): Consider these nodes alaready seen.

    Returns:
        tuple[dict[Node, float], dict[Node, Node]]:
            * For every node, the shortest path distance to that node.
            * For every node except `start`, the previous node in the shortest path to
              that node.
    """
    dist: Dict[Node, float] = {start: 0}
    prev: Dict[Node, Node] = {}
    seen = seen or set()

    q: Queue[Tuple[float, Node]] = PriorityQueue()
    q.put((heuristic(start), start))

    while not q.empty():
        d1, n1 = q.get()

        # This needs to execute first to ensure that `d1` is right.
        if n1 in seen:
            continue

        if callback(n1, d1):
            break

        # In Dijkstra's algorithm, `n1` is chosen such that (a) `n1` is unseen and (b)
        # `n1` has lowest `dist[n1] = d1`. By the induction hypothesis, for all seen
        # nodes `n2`, `dist[n2]` is the shortest distance from `start` to `n2`. It is
        # now true that `d1` is the shortest distance from `start` to `n1`. To prove
        # this, let us call unseen nodes directly connected to seen nodes *fronteer
        # nodes*. Consider a path from `start` to `n1` that has distance less than
        # `d1`. If it directly connects from `n1` to seen nodes, by construction of
        # the algorithm, its distance must be equal to `d1`. If it does not directly
        # connect from `n1` to seen nodes, it must eventually enter the seen nodes
        # via some fronteer node `n2`. However, `dist[n2] = d2 >= d1` and edges are
        # non-negative, so any path from `start` to `n1` via `n2` must have distance
        # more than `d1`. We conclude that `d1` truly is the shortest distance from
        # `start` to `n1`.
        #
        # For this argument to work, `n1` does not exactly have to be chosen such that
        # `d1` is smallest. For all other fronteer nodes `n2`, `d1` just needs to be
        # smaller than `d2` plus the shortest distance from `n2` to `n1`. Now suppose
        # that we instead choose `n1` according to smallest `d1 + h1` where
        # `h1 = heuristic(n1)` and `h2 = heuristic(n2)`, then
        #
        #     (d2 + dist(n2 -> n1))
        #         =  (d2 + h2 - h2 + dist(n2 -> n1))
        #         >= (d1 + h1 - h2 + dist(n2 -> n1)).
        #
        # Hence, if `h2 + dist(n2 -> n1) >= h1`, then we can complete the induction step
        # as above. The condition `h1 - h2 <= dist(n2 -> n1)` says that, by going from
        # `n2` to `n1`, the heuristic value never decreases by more than the shortest
        # distance from `n2` to `n1`. If `n1` and `n2` are connected via an edge, this
        # means that the heuristic value never decrease by more than the edge weight.
        # This is the stated monotonicity condition.
        #
        # If the heuristic is not monotonic, you need to search over all possible
        # paths by allowed the algorithm to revisit the same node more than once.

        if not revisit:
            seen.add(n1)

        for n2, w12 in nbs(n1):
            assert w12, f"Weight must be non-negative: {w12}."

            if n2 in seen:
                continue

            alt = d1 + w12
            if alt < dist.get(n2, float("inf")):
                dist[n2] = alt
                prev[n2] = n1
                q.put((dist[n2] + heuristic(n2), n2))

    return dist, prev