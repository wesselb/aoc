from collections import defaultdict
from typing import Callable, Dict, Generator, Iterable, Set, Tuple, TypeVar

from .graph import shortest_path

__all__ = ["max_flow"]

Node = TypeVar("Node")


def max_flow(
    nodes: Iterable[Node],
    nbs: Callable[[Node], Iterable[Tuple[Node, float]]],
    source: Node,
    sink: Node,
) -> Tuple[float, Dict[Tuple[Node, Node], float], Tuple[Set[Node], Set[Node]]]:
    """Compute the maximum flow and minimum cut with Edmond Karp's variation of
    the Ford-Fulkerson algorithm.

    Args:
        nodes (Set[Nodes]): Nodes of the graph.
        nbs (Callable[[Node], Iterable[tuple[Node, float]]]): Neighbourhood function.
            See :func:`.graph.shortest_path`.
        source (Node): Source node.
        sink (Node): Sink node.

    It is clear that every cut value upper bounds every flow value. Consider the maximum
    flow. Then all nodes reachable from `source` in the residual graph define a cut with
    value equal to the maximum flow value. Therefore, the maximum flow value is equal
    to the minimum cut value.

    To find the maximum flow, we iteratively find paths along which we can increase the
    flow using a BFS. BFS will find the path with the least number of edges in O(E)
    time, and it will never choose the same path twice. Since there are at most
    O(V E) paths along which to increase the flow, this algorithm runs in O(V E^2)
    time.

    Returns:
        float: Maximum flow value and minimum cut value.
        Dict[Tuple[Node, Node], float]: A maximum flow.
        Tuple[Set[Node], Set[Node]]: Node partition of a minimum cut.
    """
    assert source != sink, "Source and sink are the same, but must be different."

    flow: Dict[Tuple[Node, Node], float] = defaultdict(int)

    def bfs_nbs(n1: Node) -> Generator[Tuple[Node, float], None, None]:
        """Neighbourhood function to perform a BFS in the residual graph."""
        for n2, w12 in nbs(n1):
            w12 -= flow[n1, n2]
            assert w12 >= 0, "Flow exceeds edge capacity."
            if w12 > 0:
                # Return unity weight to perform a BFS.
                yield n2, 1

    # Cache edge weights for faster look-up.
    ws: Dict[Tuple[Node, Node], float] = {
        (n1, n2): w12 for n1 in nodes for n2, w12 in nbs(n1)
    }

    while True:
        dist, prev = shortest_path(source, bfs_nbs)

        if sink in dist:
            # Found an augmenting path.
            path, n = [sink], sink
            while n != source:
                n = prev[n]
                path.append(n)
            path = list(reversed(path))

            # Check by how much the flow can be increased along this path.
            c = min(ws[n1, n2] for n1, n2 in zip(path[:-1], path[1:]))

            # Increase the flow by that much.
            for n1, n2 in zip(path[:-1], path[1:]):
                flow[n1, n2] += c
                flow[n2, n1] -= c

        else:
            # No augmenting path possible. We're done!
            max_flow_value = sum(flow[source, n] for n, _ in nbs(source))
            source_connected = set(dist.keys())
            return (
                max_flow_value,
                dict(flow),
                (source_connected, set(nodes) - source_connected),
            )
