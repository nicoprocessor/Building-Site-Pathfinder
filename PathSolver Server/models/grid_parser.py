import json
import pathlib
import random
import time
from collections import OrderedDict

from pathfinder import Grid

item_types = {
    'traversable': ' ',
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
        parsed_grid = Grid(start_coord=start_pos, end_coord=end_pos, rows=rows, cols=cols)
    return parsed_grid


if __name__ == '__main__':
    rows, cols = 20, 20
    start_pos = (0, 0)
    end_pos = (rows - 1, cols - 1)

    generate_random_maze(rows, cols, 0.22, start_pos=start_pos, end_pos=end_pos)
    parse_json_file()
