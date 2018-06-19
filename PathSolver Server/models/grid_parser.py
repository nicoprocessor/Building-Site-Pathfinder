import json
import pathlib
import random
import time
from collections import OrderedDict
from pprint import pprint

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
    Generates a random map to test the pathfinder algorithm, just for debug
    :param rows: number of rows of the map
    :param cols: number of cols of the map
    :param obstacle_rate: the rate of obstacle cells
    :param start_pos: the starting position of the maze
    :param end_pos: the goal of the maze
    :return: the random maze map
    """
    map = OrderedDict()
    map['timestamp'] = int(time.time())
    map['rows'] = rows
    map['cols'] = cols

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
                item['type'] = 'traversable' if random.random() > obstacle_rate else 'obstacle'
            item_list.append(item)

    map['map_list'] = item_list
    return map


def parse_json_file():
    """
    Parses a JSON file containing the map and generates a Grid system using that instance
    :return:
    """
    # TODO
    sheet_path = pathlib.Path.cwd().parent.joinpath('res', 'map_example.json')
    with open(sheet_path, 'r') as f:
        parsed_json = json.load(f)
        pprint(parsed_json)
        return parsed_json


if __name__ == '__main__':
    items = parse_json_file()
