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
items = []


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


def ASCII_to_dict(conversion_map):
    """
    Converts a maze from ASCII format to dictionary
    :param conversion_map: ASCII character to item type
    :return: the dictionary containing the maze map
    """
    maze_path = pathlib.Path.cwd().parent.joinpath('res', 'ASCII_maze-example.txt')
    lines = []
    with open(maze_path, 'r') as f:
        for line in f:
            if line != '':
                line = re.sub(r"'+", '', line)  # remove new lines characters
                line = re.sub(r"$\n", '', line)  # remove superscript characters
                lines.append(line)

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


if __name__ == '__main__':
    rows, cols = 10, 10
    start_pos = (0, 0)
    end_pos = (rows - 1, cols - 1)

    # generate_random_maze(rows, cols, 0.17, start_pos=start_pos, end_pos=end_pos)

    # grid, parsed_dict = parse_json_file()
