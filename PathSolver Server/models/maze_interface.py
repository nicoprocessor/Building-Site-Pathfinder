from models.maze_parser import Maze_Parser

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

parser = Maze_Parser(directions=directions, item_types=item_types,
                     src_ascii_path='ascii_maze-example.txt',
                     src_json_path='maze_example.json',
                     dst_ascii_path='ascii_maze-solution.txt',
                     dst_json_path='maze_solution.json')


def solve_maze(maze, starting_orientation, path_alternatives=0):
    """
    Parse the the file with the actual maze map and solve it using A*
    :param maze: the maze map in ASCII format
    :param starting_orientation: the starting orientation of the entity
    :param path_alternatives: the number of alternative paths required
    :return: the solution path evaluated
    """
    parsed_grid = parser.ascii_to_grid(maze=maze, load_from_file=False)
    solution = parsed_grid.a_star(path_alternatives)[1]['path']

    if len(solution) > 0:
        # display solution and save it to external file both in JSON and ascii format
        # solved_maze = parser.display_solution_from_dict(maze=maze, maze_solution=solution, save_to_file=True,
        #                                                 print_on_console=False)

        # convert the solution to entity moves and save it to external file in JSON format
        moves = parser.path_to_moves(maze_solution_path=solution, starting_orientation=starting_orientation)
        solution_steps = len(solution)
        entity_moves = len(moves)
        compression_rate = entity_moves / solution_steps

        # print(f"Starting orientation: {starting_orientation}\n"
        #       f"Moves: {moves}\n"
        #       f"Solution steps: {solution_steps}\n"
        #       f"Entity moves: {entity_moves}\n"
        #       f"Compression rate: {compression_rate:.3f}")

        return {'moves': moves, 'solution_steps': solution_steps,
                'entity_moves': entity_moves, 'compression_rate': compression_rate}
    else:
        # no path found
        return {'moves': '0'}


def random_maze(size, start, end, obstacle_rate):
    """
    Generates a random maze map and writes it to a JSON file.
    :param size: number of rows/cols of the map
    :param obstacle_rate: the rate of obstacle cells
    :param start: the starting position of the maze (tuple)
    :param end: the goal of the maze (tuple)
    :return: the maze generated randomly
    """
    maze = parser.generate_random_maze(rows=size, cols=size,
                                       obstacle_rate=obstacle_rate,
                                       start_pos=start, end_pos=end)
    return maze
