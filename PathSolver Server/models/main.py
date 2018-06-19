from grid_parser import parse_json_file


def solve_maze(path_alternatives):
    """Parse the the file with the actual maze map and solve it using A*"""
    parsed_grid = parse_json_file()
    parsed_grid.a_star()


if __name__ == '__main__':
    pass
