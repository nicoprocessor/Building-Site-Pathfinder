import math
import time
from queue import PriorityQueue

incremental_cost = 1
spot_type_traversable = "traversable"
spot_type_obstacle = "obstacle"
spot_type_robot = "robot"
spot_type_start = "start"
spot_type_end = "end"
spot_type_solution = "solution"

type_conversion = {
    spot_type_traversable: '_',
    spot_type_obstacle: 'X',
    spot_type_robot: 'R',
    spot_type_solution: '$'
}


def manhattan_distance(a, b):
    """
    Returns the Manhattan distance between two spots.
    :param a: the coordinates of the first spot
    :param b: the coordinates of the second spot
    :return: the Manhattan distance
    """
    return abs(b.x - a.x) + abs(b.y - a.y)


def euclidean_distance(a, b):
    """
    Returns the euclidean distance between two spots.
    :param a: the coordinates of the first spot
    :param b: the coordinates of the second spot
    :return: the euclidean distance
    """
    return math.sqrt(pow(b.x - a.x, 2) + pow(b.y - a.y, 2))


def eval_heuristic(a, b, heuristic):
    """
    Evaluate the distance between the two given spots using the given heuristic
    :param a: the coordinates of the first spot
    :param b: the coordinates of the second spot
    :param heuristic: the required heuristic
    :return: the distance between the given spots
    """
    if heuristic == 'MANHATTAN':
        return manhattan_distance(a, b)
    else:
        return euclidean_distance(a, b)


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
        return "Spot at x: {} y: {} type: {}".format(str(self.x), str(self.y), self.spot_type)


class CheckablePriorityQueue(PriorityQueue):
    """
    Extension of PriorityQueue class, add the functionality of membership test
    """

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue


class Grid(object):
    """
    A grid made of spots
    """

    def __init__(self, start_coord, end_coord, rows, cols, spots):
        self.rows = rows
        self.cols = cols
        self.mesh = [None] * cols

        # init mesh
        for i in range(rows):
            self.mesh[i] = [None] * cols
            for j in range(cols):
                self.mesh[i][j] = spots[i * cols + j]

        # fill neighbors
        for i in range(rows):
            for j in range(cols):
                self.add_neighbors(self.mesh[i][j])

        # start_spot and end_spot expected format {'x': 0, 'y': 0}
        self.start_spot = self.mesh[start_coord['x']][start_coord['y']]
        self.end_spot = self.mesh[end_coord['x']][end_coord['y']]

    def add_neighbors(self, current_spot):
        """
        Evaluate neighbors for the given spot. A neighbor spot is any adjacent spot on
        the grid to the actual spot such as the Manhattan distance is exactly 1.
        :param current_spot: the spot that has to be modified
        """
        candidate_neighbors = []

        if current_spot.x < self.cols - 1:
            # add the neighbor on the right
            candidate_neighbors.append(self.mesh[current_spot.x + 1][current_spot.y])
        if current_spot.x > 0:
            # add the neighbor on the left
            candidate_neighbors.append(self.mesh[current_spot.x - 1][current_spot.y])
        if current_spot.y < self.rows - 1:
            # add the neighbor below
            candidate_neighbors.append(self.mesh[current_spot.x][current_spot.y + 1])
        if current_spot.y > 0:
            # add the neighbor above
            candidate_neighbors.append(self.mesh[current_spot.x][current_spot.y - 1])

        # Append only if the neighbor is not an obstacle
        # This will save time later when we'll check every neighbor
        for candidate in candidate_neighbors:
            if candidate.spot_type != spot_type_obstacle:
                current_spot.neighbors.append(candidate)

    def a_star(self, alternatives=0):
        """
        Solves the maze from start to end using A* algorithm
        :param alternatives: number of alternative paths to evaluate (use, with caution)
        :return: the list of spots that solves the maze or a list of lists of possible solutions, if the maze is solvable.
                False otherwise.
        """
        # TODO implement alternatives
        path = []
        solution = {'alternatives': alternatives}
        open_queue = CheckablePriorityQueue()
        closed_set = []

        open_queue.put(self.start_spot)

        # A* main loop
        while True:
            start = time.process_time()
            if open_queue.qsize() > 0:
                # Best next option
                current_spot = open_queue.queue[0]

                if current_spot == self.end_spot:
                    end = time.process_time()

                    # Found destination, start backtracking to find path to starting spot
                    temp = current_spot
                    path.append({'x': current_spot.x, 'y': current_spot.y, 'type': spot_type_solution})

                    while temp.previous is not None:
                        path.append({'x': temp.previous.x, 'y': temp.previous.y, 'type': spot_type_solution})
                        temp = temp.previous

                    print("Path found!")
                    solution['elapsed_time'] = end - start
                    solution['steps'] = len(path)
                    solution['path'] = list(reversed(path))
                    return True, solution

                else:
                    # move the best option from open set to closed set
                    closed_set.append(current_spot)
                    open_queue.get()

                    # check all the neighbors
                    neighbors = current_spot.neighbors

                    for current_neighbor in neighbors:
                        # check if neither the neighbor hasn't been visited
                        # we don't need to check if the neighbor is not an obstacle
                        # because we removed those when generating the grid
                        if current_neighbor not in closed_set:
                            # I could have reached the next spot by following a less efficient path.
                            temp_g = current_spot.g + eval_heuristic(current_neighbor, current_spot,
                                                                     heuristic='MANHATTAN')

                            if temp_g < current_neighbor.g or current_neighbor.g == 10e+6:
                                current_neighbor.g = temp_g

                            if not open_queue.__contains__(current_neighbor):
                                open_queue.put(current_neighbor)

                            # update neighbor status
                            current_neighbor.h = eval_heuristic(current_neighbor, self.end_spot, heuristic='MANHATTAN')
                            current_neighbor.f = current_neighbor.g + current_neighbor.h
                            current_neighbor.previous = current_spot
            else:
                # no solution found
                print("No path found!")
                end = time.process_time()
                return False, {'elapsed_time': end - start}

    def __str__(self):
        return "Cols: {}\nRows: {}\nStart: {}\nEnd: {}\nMesh: {}".format(self.cols, self.rows, self.start_spot,
                                                                         self.end_spot, self.mesh)

    def __repr__(self):
        pass
