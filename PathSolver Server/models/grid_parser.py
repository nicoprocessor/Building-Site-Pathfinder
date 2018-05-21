import time
import json
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


def parse_json_file(file_in):
    with open(file_in, 'r') as f:
        parsed_json = json.load(f)
        pprint(parsed_json)
        return parsed_json


if __name__ == '__main__':
    f = r'C:\Users\nicol\Desktop\Building Site PF\PathSolver Server\res\map_example.json'
    items = parse_json_file(f)
