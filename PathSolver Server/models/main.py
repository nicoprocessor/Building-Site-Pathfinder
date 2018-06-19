from grid_parser import parse_json_file
import models as pf
from grid_parser import
from grid_parser import parse_json_file


def solve_maze(path_alternatives):
    """Parse the the file with the actual maze map and solve it using A*"""
    parsed_grid = parse_json_file()
    parsed_grid.a_star()


if __name__ == '__main__':
    grid = pf.Grid(start_coord=None, end_coord=None, rows=5, cols=5)
    print(grid)
    feasible, path = grid.a_star()
    print("Is feasible? {}".format(feasible))
