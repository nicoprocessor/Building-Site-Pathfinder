from models.parser import Parser

item_types = {
    'traversable': '_',
    'solution': '$',
    'obstacle': 'X',
    'robot': 'R',
    'start': 'S',
    'end': 'E'
}

# available directions of movement, written in clockwise order
directions = ['N', 'E', 'S', 'W']


def solve_maze(parsing_tool, path_alternatives):
    """
    Parse the the file with the actual maze map and solve it using A*
    :param parsing_tool: parser object that loads the maze instance
    :param path_alternatives: the number of alternative paths required
    :return:
    """
    parsed_grid = parsing_tool.ASCII_to_grid()
    path = parsed_grid.a_star(path_alternatives)
    # parser.display_solution(maze=parsing_tool.ASCII_file_to_dict(),
    #                         maze_solution=path[1]['path'],
    #                         save_to_file=True)
    return path


if __name__ == '__main__':
    parser = Parser(directions=directions, item_types=item_types,
                    src_ASCII_path='ASCII_maze-example.txt',
                    src_json_path='maze_example.json',
                    dst_ASCII_path='ASCII_maze-solution.txt',
                    dst_json_path='maze_solution.json')
    parser.generate_random_maze(5, 5, 0.2, (0, 0), (4, 4))
    solution = solve_maze(parsing_tool=parser, path_alternatives=0)
    print(f"Solution: {solution}")
