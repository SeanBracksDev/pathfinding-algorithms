# Example file showing a circle moving on screen

from queue import PriorityQueue

import pygame

from algorithms import a_star_step
from node import Colour, Node, NodeType

GRID_DIMENSION = 1000
GRID_COLS = 8
CELL_DIMENSION = GRID_DIMENSION // GRID_COLS

# pygame setup
pygame.init()
pygame.display.set_caption("Pathfinding Visualizer")


def draw_grid(window, _cells: list[list[Node]]):
    """draws the grid on the screen

    :param _type_ window: window to draw the grid on
    :param list[list[Node]] _cells: list of cells to draw
    """
    for _row in _cells:
        for _col in _row:
            _col.draw(screen)
            pygame.draw.line(
                window, Colour.GREY.value, (_col.x * CELL_DIMENSION, 0), (_col.x * CELL_DIMENSION, GRID_DIMENSION)
            )
            pygame.draw.line(
                window, Colour.GREY.value, (0, _col.y * CELL_DIMENSION), (GRID_DIMENSION, _col.y * CELL_DIMENSION)
            )


def get_clicked_cell(_pos: tuple[int, int]) -> tuple[int, int]:
    """returns the cell that was clicked

    :param tuple[int, int] _pos: _description_
    :return tuple[int, int]: coords of cell that was clicked
    """
    x, y = _pos
    _col = y // CELL_DIMENSION
    _row = x // CELL_DIMENSION
    return _row, _col


cells = [[Node(x, y, CELL_DIMENSION) for y in range(GRID_COLS)] for x in range(GRID_COLS)]

screen = pygame.display.set_mode((GRID_DIMENSION, GRID_DIMENSION))
clock = pygame.time.Clock()
start_cell, finish_cell = None, None
current_cell, visited_cells, queued_cells = None, None, None
running = True

dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            # if the click is outside the grid, ignore
            if pos[0] >= GRID_DIMENSION or pos[1] >= GRID_DIMENSION or pos[0] < 0 or pos[1] < 0:
                continue
            row, col = get_clicked_cell(pos)
            cell = cells[row][col]
            # if the cell was updated recently, ignores
            if cell.last_updated + 1000 < pygame.time.get_ticks():
                if pygame.mouse.get_pressed()[0]:
                    if not start_cell:
                        if cell.update_type(NodeType.START):
                            start_cell = cell
                            current_cell = cell
                    elif not finish_cell:
                        if cell.update_type(NodeType.FINISH):
                            finish_cell = cell
                            visited_cells = set()
                            queued_cells = []
                    else:
                        cell.update_type(NodeType.WALL)

                elif pygame.mouse.get_pressed()[2]:
                    cell.update_type(NodeType.UNVISITED)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if start_cell and finish_cell:
                    current_cell, cells, visited_cells, queued_cells = a_star_step(
                        cells, current_cell, finish_cell, visited_cells, queued_cells
                    )
                    if current_cell.x == finish_cell.x and current_cell.y == finish_cell.y:
                        current_cell.update_type(NodeType.FINISH)
                        print("Finish found!")
    draw_grid(window=screen, _cells=cells)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
