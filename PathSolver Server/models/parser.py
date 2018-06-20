import json
import pathlib
import random
import re
import time
from collections import OrderedDict

item_types = {
    'traversable': '_',
    'obstacle': 'X',
    'robot': 'R',
    'start': 'S',
    'end': 'E'
}

# available directions of movement, written in clockwise order
directions = ['N', 'E', 'S', 'W']


def dict_to_items():
    pass


def generate_random_maze(rows, cols, obstacle_rate, start_pos, end_pos):
    """
    Generates a random maze map and writes it to a JSON file
    :param rows: number of rows of the map
    :param cols: number of cols of the map
    :param obstacle_rate: the rate of obstacle cells
    :param start_pos: the starting position of the maze
    :param end_pos: the goal of the maze
    """
    map = OrderedDict()
    map['timestamp'] = int(time.time())
    map['rows'] = rows
    map['cols'] = cols

    obstacles = 0
    item_list = []
    item = {}

    for i in range(rows):
        for j in range(cols):
            item = {}
            item['x'] = i
            item['y'] = j
            if (i, j) == (start_pos):
                item['type'] = 'start'
            elif (i, j) == (end_pos):
                item['type'] = 'end'
            else:
                if random.random() > obstacle_rate:
                    item['type'] = 'traversable'
                else:
                    item['type'] = 'obstacle'
                    obstacles += 1
            item_list.append(item)
    map['maze'] = item_list

    # debug
    print("Obstacles: {} on {} total cells.\n"
          "Expected obstacle rate: {}\n"
          "Actual obstacle rate: {}".format(obstacles, rows * cols,
                                            obstacle_rate, obstacles / (rows * cols)))

    # write the maze to the example file
    example_file_path = pathlib.Path.cwd().parent.joinpath('res', 'map_example.json')
    with open(example_file_path, 'w') as f:
        json.dump(map, f)


def find_dict_index_in_dict_list(lst, key, value):
    """
    Searches for a specific dictionary in a dictionary list based on the pair (key, value)
    and returns the index of the first element that matches
    :param lst: the list of dictionaries
    :param key: the key that has to match with the given value
    :param value: the value that has to match
    :return: the index of the dictionary, if present. Otherwise raises a ValueError exception.
    """
    for index, dic in enumerate(lst):
        if dic[key] == value:
            return index
    raise ValueError


def parse_json_file():
    """
    Parses a JSON file containing the map and generates a Grid system using that instance
    :return: a Grid structured following the JSON file
    """
    sheet_path = pathlib.Path.cwd().parent.joinpath('res', 'map_example.json')

    with open(sheet_path, 'r') as f:
        parsed_json = json.load(f)

        timestamp = parsed_json['timestamp']
        rows = parsed_json['rows']
        cols = parsed_json['cols']
        start_pos_cell = parsed_json['maze'][find_dict_index_in_dict_list(parsed_json['maze'], 'type', 'start')]
        end_pos_cell = parsed_json['maze'][find_dict_index_in_dict_list(parsed_json['maze'], 'type', 'end')]
        start_pos = (start_pos_cell['x'], start_pos_cell['y'])
        end_pos = (end_pos_cell['x'], end_pos_cell['y'])

        print("Start pos: {}\nEnd pos: {}".format(start_pos, end_pos))

        # TODO implement the entire mesh parsing and creation in the grid constructor
        # parsed_grid = Grid(start_coord=start_pos, end_coord=end_pos, rows=rows, cols=cols)
        parsed_grid = None
    return parsed_grid, parsed_json


def swap_key_value(old_dict):
    """
    Creates a new dictionary swapping keys and values of an existing dictionary
    :param old_dict: the dictionary that has to be swapped
    :return: the new dictionary, obtained swapping keys and values
    """
    new_dict = {}
    for old_key, old_value in old_dict.items():
        new_dict[old_value] = old_key

    # print if some keys were overwritten during the process
    if len(new_dict) == len(old_dict):
        print("No keys were lost during the process")
    else:
        print("Some values were lost during the process")
    return new_dict


def ASCII_file_to_dict(conversion_map, file_path):
    """
    Converts a maze from ASCII format to dictionary
    :param conversion_map: ASCII character to item type
    :return: the dictionary containing the maze map
    """
    maze_path = pathlib.Path.cwd().parent.joinpath('res', file_path)
    lines = []
    with open(maze_path, 'r') as f:
        for line in f:
            if line != '':
                line = re.sub(r"(\d|\s)+", '', line)  # remove any digit or whitespace
                if len(line) == 0:  # skip line if empty
                    continue
                else:
                    line = re.sub(r"'+", '', line)  # remove new lines characters
                    line = re.sub(r"$\n", '', line)  # remove superscript characters
                    lines.append(line)

    conversion_map = swap_key_value(conversion_map)
    # init dst dictionary
    maze_dict = OrderedDict()
    maze_dict['timestamp'] = int(time.time())

    maze_dict['rows'] = len(lines)
    maze_dict['cols'] = len(lines[0])
    cells = []

    print(conversion_map)
    # char by char conversion
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            cell = {
                'x': i,
                'y': j,
                'type': conversion_map[char]
            }
            cells.append(cell)
    maze_dict['maze'] = cells

    return maze_dict


def dict_to_ASCII(conversion_map, maze):
    """
    Prints the maze map using ASCII characters
    :param conversion_map: types to ASCII character
    :param maze: the map that needs to be converted
    """
    for i in range(maze['rows']):
        ascii_line = ''
        for j in range(maze['cols']):
            current_element_type = maze['maze'][i * cols + j]['type']
            # print("({},{}): {}".format(i, j, current_element_type))
            ascii_line += conversion_map[current_element_type]
        print(ascii_line)


def path_to_moves(maze_solution_path, starting_orientation='N'):
    """
    Convert the maze solution to a dictionary containing the moves that
    the entity will follow in order to complete the game
    :param maze_solution_path: the maze solution
    :param starting_orientation: the starting orientation of the entity. By default it is set to North (UP)
    :return: the dictionary containing the converted solution
    """
    actions = ''
    current_orientation = starting_orientation

    for i, current_cell in enumerate(maze_solution_path[:-2]):
        next_cell = maze_solution_path[i + 1]
        starting_move = True if i == 0 else False
        next_actions, current_orientation = move_to_actions(current_cell=current_cell, next_cell=next_cell,
                                                            previous_orientation=current_orientation,
                                                            starting_move=starting_move)
        actions += next_actions


def move_to_actions(current_cell, next_cell, previous_orientation, starting_move):
    """
    Returns the moves that the entity has to follow in order to achieve the given steps.
    :param current_cell: the current position
    :param next_cell: the next position
    :param previous_orientation: the previous orientation of the entity
    :param starting_move: flag that tells if the current move is the first. This flag is necessary since the first move is the only one that can lead to a multiple rotation.
    :return: the moves that the entity has to follow in order to achieve the move indicated from the couple of steps
    """
    # considering a single step as tuple of coordinates (x,y)
    # available actions: rotate (R), move forward (M)
    # available move directions: North (N), South (S), East (E), West (W)
    # available rotation directions: +90° (+), -90° (-), 0 (blank)
    actions = ''
    movement_direction, rotate = '', ''

    # identify the direction of the movement
    if current_cell[0] > next_cell[0]:  # moving left (W)
        movement_direction = 'W'
    elif current_cell[0] < next_cell[0]:  # moving right (E)
        movement_direction = 'E'
    else:  # moving up or down (N|S)
        if current_cell[1] > next_cell[0]:  # moving down (S)
            movement_direction = 'S'
        else:  # moving up (N)
            movement_direction = 'N'

    # check if the entity needs to rotate before moving to the next cell
    if previous_orientation != movement_direction:
        if starting_move:  # we can't assume that the entity will have to rotate only by 90°
            if (directions.index(previous_orientation) + 1) % len(
                    directions) != movement_direction:  # rotation by +90° isn't enough
                if (directions.index(previous_orientation) + 2) % len(
                        directions) != movement_direction  # rotation by +180° isn't enough
                    rotation_direction = '-'  # since +180° isn't enough we can assume that the desired rotation is +270° = -90°
                else:  # +180°
                    rotation_direction = '++'
            else:  # +90°
                rotation_direction = '+'
        else:  # we can assume that the maximum rotation required is 90°
            if (directions.index(previous_orientation) + 1) % len(directions) == movement_direction:
                rotation_direction = '+'
            else:
                rotation_direction = '-'
        actions = rotation_direction
    actions += movement_direction

    return actions, movement_direction


if __name__ == '__main__':
# rows, cols = 5, 5
# start_pos = (0, 0)
# end_pos = (rows - 1, cols - 1)

# generate_random_maze(rows, cols, 0.17, start_pos=start_pos, end_pos=end_pos)
# grid, parsed_dict = parse_json_file()
# pprint(ASCII_file_to_dict(item_types, 'ASCII_maze-example.txt'))
