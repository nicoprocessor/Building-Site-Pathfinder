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
    :return: the solution path evaluated
    """
    parsed_grid = parsing_tool.ascii_to_grid()
    solution = parsed_grid.a_star(path_alternatives)
    return [] if not solution[0] else solution[1]['path']


# main
if __name__ == '__main__':
    parser = Parser(directions=directions, item_types=item_types,
                    src_ascii_path='ascii_maze-example.txt',
                    src_json_path='maze_example.json',
                    dst_ascii_path='ascii_maze-solution.txt',
                    dst_json_path='maze_solution.json')
    size = 5
    start = (0, 0)
    end = (size - 1, size - 1)
    obstacle_rate = 0.24
    maze = parser.generate_random_maze(rows=size, cols=size,
                                       obstacle_rate=obstacle_rate,
                                       start_pos=start, end_pos=end)
    maze = maze
    solution = solve_maze(parsing_tool=parser, path_alternatives=0)

    if len(solution) > 0:
        # display solution and save it to external file both in JSON and ascii format
        solved_maze = parser.display_solution_from_dict(maze=maze, maze_solution=solution, save_to_file=True,
                                                        print_on_console=False)

        # convert the solution to entity moves and save it to external file in JSON format
        moves = parser.path_to_moves(maze_solution_path=solution, starting_orientation='S')
        print(moves)
    else:
        # TODO send error code to the application and ask to change the map, otherwise seeya!
        pass
