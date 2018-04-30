# import timeit
import math
import random
from queue import PriorityQueue

cols = 10
rows = 10
grid = [None] * rows  # [[]] 2D mesh

incremental_cost = 1
spot_type_traversable = "traversable"
spot_type_obstacle = "obstacle"

type_conversion = {
    spot_type_traversable: 'o',
    spot_type_obstacle: 'x',
    "current": '$',
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


def a_star():
    """A* pathfinding algorithm"""
    path = []
    open_queue = CheckablePriorityQueue()
    closed_set = []

    # init pathfinding - these can be randomized
    start_spot = grid[0][0]
    end_spot = grid[rows - 1][cols - 1]
    open_queue.put(start_spot)

    # A* main loop
    while True:
        if open_queue.qsize() > 0:
            # Best next option
            current_spot = open_queue.queue[0]

            if current_spot == end_spot:
                # Found destination, start backtracking to find path to starting spot
                temp = current_spot
                path.append(current_spot)

                while temp.previous is not None:
                    path.append(temp.previous)
                    temp = temp.previous

                print("Path found!")
                return True, path

            else:
                # move the best option from open set to closed set
                closed_set.append(current_spot)
                open_queue.get()

                # check all the neighbors
                neighbors = current_spot.neighbors
                for current_neighbor in neighbors:
                    # check if neither the neightbor hasn't been visited yet nor it's an obstacle
                    if current_neighbor.spot_type != spot_type_obstacle and current_neighbor not in closed_set:
                        # I could have reached the next spot by following a less efficient path.
                        temp_g = current_spot.g + eval_heuristic(current_neighbor, current_spot)

                        # check if current neighbor is in a better path then the previous one or if it's the first time we visit this spot
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

    def add_neighbors(self):
        """Evaluate neighbors for the given spot. A neighbor spot is any adjacent spot on
            the grid to the actual spot such as the Manhattan distance is exactly 1.
        """
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])


class CheckablePriorityQueue(PriorityQueue):
    """Extension of PriorityQueue class, add the functionality of membership test"""

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


# main
if __name__ == '__main__':
    # init spots
    for i in range(rows):
        grid[i] = [None] * cols
        for j in range(cols):
            grid[i][j] = Spot(i, j, spot_type_traversable)

    # for i in range(rows):
    #     if i != 4:
    #         grid[i][cols-i-1] = Spot(i, i, spot_type_obstacle)

    # for i in range(20):
    #     rand_x = random.randint(1, rows-1)
    #     rand_y = random.randint(1, cols-1)
    #     grid[rand_x][rand_y] = Spot(rand_x, rand_y, spot_type_obstacle)

    # fill neighbors
    for i in range(rows):
        for j in range(cols):
            grid[i][j].add_neighbors()

    print("Pathfinding...")
    feasible, path = a_star()

    if feasible:
        for step, spot_index in enumerate(list(reversed(path))):
            print('{} {}'.format(step, spot_index.__str__()))
