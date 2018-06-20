from models.parser import Parser

item_types = {
    'traversable': '_',
    'obstacle': 'X',
    'robot': 'R',
    'start': 'S',
    'end': 'E'
}

# available directions of movement, written in clockwise order
directions = ['N', 'E', 'S', 'W']


def solve_maze(path_alternatives):
    """
    Parse the the file with the actual maze map and solve it using A*
    :param path_alternatives: the number of alternative paths required
    :return:
    """
    parser = Parser(directions=directions, item_types=item_types, src_ASCII_path='ASCII_maze-example.txt',
                    src_json_path='map_example.json', dst_json_path='map_example.json')
    parsed_grid = parser.ASCII_to_grid()
    print(parsed_grid)
    path = parsed_grid.a_star(path_alternatives)
    print(path)


if __name__ == '__main__':
    solve_maze(path_alternatives=0)
