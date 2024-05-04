import enum
from typing import Self

import pygame


class Colour(enum.Enum):
    """Colours used in the visualizer"""

    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY = (128, 128, 128)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)


class NodeType(enum.Enum):
    """Types of nodes in the grid"""

    UNVISITED = 0
    VISITED = 1
    WALL = 2
    START = 3
    FINISH = 4
    CURRENT = 5
    NEIGHBOUR = 6  # TODO REMOVE


class Node:
    """Node which represents a cell in the grid"""

    def __init__(self, x: int, y: int, dimension: int, node_type: NodeType = NodeType.UNVISITED) -> None:
        self.x = x
        self.y = y
        self.node_type = node_type
        self.last_updated = 0
        self.dimension = dimension
        self.weight = None

    def draw(self, window):
        """draws the node on the screen

        :param _type_ window: window to draw the node on # TODO
        """
        match self.node_type:
            case NodeType.UNVISITED:
                colour = Colour.WHITE
            case NodeType.VISITED:
                colour = Colour.YELLOW
            case NodeType.WALL:
                colour = Colour.BLACK
            case NodeType.START:
                colour = Colour.GREEN
            case NodeType.FINISH:
                colour = Colour.RED
            case NodeType.CURRENT:
                colour = Colour.PURPLE
            case NodeType.NEIGHBOUR:  # TODO REMOVE
                colour = Colour.ORANGE

        pygame.draw.rect(
            window, colour.value, (self.x * self.dimension, self.y * self.dimension, self.dimension, self.dimension)
        )

        if self.weight:
            font = pygame.font.Font(None, 20)
            text = font.render(str(self.weight), True, Colour.BLACK.value)
            window.blit(text, (self.x * self.dimension + 5, self.y * self.dimension + 5))

    def update_type(self, node_type: NodeType):
        """updates the node type based on the current type"""
        if self.node_type not in (NodeType.START, NodeType.FINISH):
            self.node_type = node_type
            self.last_updated = pygame.time.get_ticks()
            return True
        return False

    def get_neighbours(self, cells: list[list[Self]]) -> list["Node"]:
        """returns the neighbours of the node"""
        neighbours = []
        rows = len(cells)
        if self.x < rows - 1 and cells[self.x + 1][self.y].node_type != NodeType.WALL:
            neighbours.append(cells[self.x + 1][self.y])
        if self.x > 0 and cells[self.x - 1][self.y].node_type != NodeType.WALL:
            neighbours.append(cells[self.x - 1][self.y])
        if self.y < rows - 1 and cells[self.x][self.y + 1].node_type != NodeType.WALL:
            neighbours.append(cells[self.x][self.y + 1])
        if self.y > 0 and cells[self.x][self.y - 1].node_type != NodeType.WALL:
            neighbours.append(cells[self.x][self.y - 1])

        return neighbours

    def __lt__(self, other):
        return self.weight < other.weight

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"Node({self.x + 1}, {self.y + 1})"

    def __repr__(self) -> str:
        return self.__str__()
