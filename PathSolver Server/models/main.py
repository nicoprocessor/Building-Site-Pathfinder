import models.parser as parser


def solve_maze(path_alternatives):
    """Parse the the file with the actual maze map and solve it using A*"""
    parsed_grid = parser.json_to_grid('map_example.json')
    path = parsed_grid.a_star()
    #print(path)


if __name__ == '__main__':
    solve_maze(0)
