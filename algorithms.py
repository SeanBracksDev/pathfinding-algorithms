from heapq import heappop, heappush

from node import Node, NodeType


def a_star_step(
    nodes: list[list[Node]],
    current_node: Node,
    finish_node: Node,
    visited_nodes: set[Node],
    queue: list[int, Node],
) -> tuple[list[list[Node]], set[Node], list[int, Node]]:
    """Performs one step of the A* algorithm

    :param list[list[Node]] nodes: list of list of nodes
    :param Node current: current node
    :param Node finish: finish node
    :param set[Node] visited: visited nodes
    :param PriorityQueue[int, Node] queue: queue of nodes to visit, ordered by a* heuristic
    :return Node, tuple[list[list[Node]], set[Node], PriorityQueue[int, Node]]: new_current_cell, updated cells, visited nodes, queue
    """

    def h(p1: tuple[int, int], p2: tuple[int, int]):
        """heuristic function to calculate the distance between two points

        :param int p1: point 1
        :param int p2: point 2
        """
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

    visited_nodes.add(current_node)
    neighbours = current_node.get_neighbours(nodes)
    for neighbour in neighbours:
        if neighbour not in visited_nodes:
            _g = 1  # g is the cost of the path from the start node to the current node
            _h = h(
                (neighbour.x, neighbour.y), (finish_node.x, finish_node.y)
            )  # h is the heuristic function, which is the distance between the current node and the finish node
            _f = _g + _h
            nodes[neighbour.x][neighbour.y].weight = _f
            if (_f, neighbour) not in queue:
                heappush(queue, (_f, neighbour))
    print(queue)
    new_current_node = heappop(queue)[1]
    current_node.update_type(NodeType.VISITED)
    new_current_node.update_type(NodeType.CURRENT)
    return new_current_node, nodes, visited_nodes, queue
