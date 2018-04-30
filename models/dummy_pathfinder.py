# import timeit
import math

cols = 5
rows = 5
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
    open_set = []
    closed_set = []

    # init pathfinding - these can be randomized
    start_spot = grid[0][0]
    end_spot = grid[rows - 1][cols - 1]
    open_set.append(start_spot)

    # A* main loop
    while True:
        if len(open_set) > 0:
            # Best next option - the one with lowest f (cost)
            smallest_score_spot_index = 0
            for i in range(len(open_set)):
                if open_set[i].f < open_set[smallest_score_spot_index].f:
                    smallest_score_spot_index = i

                # If we have a tie according to the standard heuristic
                # select the one with the smallest heuristic score (closest to goal)
                elif open_set[i].f == open_set[smallest_score_spot_index].f:
                    if open_set[i].h < open_set[smallest_score_spot_index].h:
                        smallest_score_spot_index = i

            # update current spot
            current_spot = open_set[smallest_score_spot_index]

            if open_set[smallest_score_spot_index] == end_spot:
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
                open_set.remove(current_spot)

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

                        if current_neighbor not in open_set:
                            open_set.append(current_neighbor)

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
        self.f = 0  # cost function
        self.g = 1e+6  # actual cost from the starting node
        self.h = 0  # heuristic - educated guess
        self.x = x
        self.y = y
        self.neighbors = []  # adjacent spots
        self.previous = None  # previous node in the path
        self.spot_type = spot_type

    def __repr__(self):
        return str(self.spot_type)

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


# main
if __name__ == '__main__':
    # init spots
    for i in range(rows):
        grid[i] = [None] * cols
        for j in range(cols):
            grid[i][j] = Spot(i, j, spot_type_traversable)

    for i in range(rows):
        if i != 2:
            grid[i][cols - i - 1] = Spot(i, i, spot_type_obstacle)

    # fill neighbors
    for i in range(rows):
        for j in range(cols):
            grid[i][j].add_neighbors()

    print("Pathfinding...")
    feasible, path = a_star()

    if feasible:
        for step, spot_index in enumerate(list(reversed(path))):
            print('{} {}'.format(step, spot_index.__str__()))

