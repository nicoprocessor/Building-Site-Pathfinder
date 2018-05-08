import math
from typing import Dict
from queue import PriorityQueue

incremental_cost = 1
spot_type_traversable = "traversable"
spot_type_obstacle = "obstacle"
spot_type_robot = "robot"
spot_type_start = "start"
spot_type_end = "end"

type_conversion = {
    spot_type_traversable: '0',
    spot_type_obstacle: 'X',
    spot_type_robot: 'R',
    "path": '0'
}


def manhattan_distance(a, b):
    """Returns the manhattan distance between two spots."""
    return abs(b.x - a.x) + abs(b.y - a.y)


def euclidean_distance(a, b):
    """Returns the euclidean distance between two spots."""
    return math.sqrt(pow(b.x - a.x, 2) + pow(b.y - a.y, 2))


def eval_heuristic(a, b):
    return manhattan_distance(a, b)


class Spot(object):
    """A traversable spot on the grid"""

    def __init__(self, x, y, spot_type=spot_type_traversable):
        self.f = 1e+6  # cost function
        self.g = 1e+6  # actual cost from the starting node
        self.h = 0  # heuristic - educated guess
        self.x = x
        self.y = y
        self.neighbors = []  # adjacent spots
        self.previous = None  # previous node in the path
        self.spot_type = spot_type

    def __lt__(self, other):
        self_priority = (self.f, self.h)
        other_priority = (other.f, other.h)
        return self_priority > other_priority

    def __repr__(self):
        return "Spot at x:" + str(self.x) + " y:" + str(self.y)

    def __str__(self):
        return "Spot at x:" + str(self.x) + " y:" + str(self.y)

    def add_neighbors(self, grid):
        """Evaluate neighbors for the given spot. A neighbor spot is any adjacent spot on
            the grid to the actual spot such as the Manhattan distance is exactly 1.
        """
        if self.x < grid.cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < grid.rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])


class CheckablePriorityQueue(PriorityQueue):
    """Extension of PriorityQueue class, add the functionality of membership test"""

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class Grid(object):
    """A grid made of spots"""

    def __init__(self, rows: int, cols: int, start_coord: Dict[str, int], end_coord: Dict[str, int]):
        self.mesh = None
        self.rows = rows
        self.cols = cols
        for i in range(rows):
            self.mesh[i] = [None] * cols
            for j in range(cols):
                self.mesh[i][j] = Spot(i, j, spot_type_traversable)

        self.start_spot = Spot(start_coord['x'], start_coord['y'])
        self.end_spot = Spot(end_coord['x'], end_coord['y'])

        # fill neighbors
        for i in range(rows):
            for j in range(cols):
                self.mesh[i][j].add_neighbors()

    def __str__(self):
        pass

    def __repr__(self):
        pass

    @property
    def a_star(self):
        """A* pathfinding algorithm"""
        path = []
        open_queue = CheckablePriorityQueue()
        closed_set = []

        open_queue.put(self.start_spot)

        # A* main loop
        while True:
            if open_queue.qsize() > 0:
                # Best next option
                current_spot = open_queue.queue[0]

                if current_spot == self.end_spot:
                    # Found destination, start backtracking to find path to starting spot
                    temp = current_spot
                    path.append(current_spot)

                    while temp.previous is not None:
                        path.append(temp.previous)
                        temp = temp.previous

                    print("Path found!")
                    return True, list(reversed(path))

                else:
                    # move the best option from open set to closed set
                    closed_set.append(current_spot)
                    open_queue.get()

                    # check all the neighbors
                    neighbors = current_spot.neighbors
                    for current_neighbor in neighbors:
                        # check if neither the neighbor hasn't been visited yet nor it's an obstacle
                        if current_neighbor.spot_type != spot_type_obstacle and current_neighbor not in closed_set:
                            # I could have reached the next spot by following a less efficient path.
                            temp_g = current_spot.g + eval_heuristic(current_neighbor, current_spot)

                            if temp_g < current_neighbor.g or current_neighbor.g == 10e+6:
                                current_neighbor.g = temp_g

                            if not open_queue.__contains__(current_neighbor):
                                open_queue.put(current_neighbor)

                            # update neighbor status
                            current_neighbor.h = eval_heuristic(current_neighbor, end_spot)
                            current_neighbor.f = current_neighbor.g + current_neighbor.h
                            current_neighbor.previous = current_spot
            else:
                # no solution
                print("No path found!")
                return False, []
