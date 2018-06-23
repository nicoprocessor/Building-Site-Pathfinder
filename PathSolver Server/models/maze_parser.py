import json
import pathlib
import random
import re
import time

from models.pathfinder import Grid
from models.pathfinder import Spot
from models.utils import find_dict_index_in_dict_list
from models.utils import merge_dict_lists_on_specific_keys_with_priority
from models.utils import swap_key_value


class Maze_Parser(object):
    """
    Wrapper class of some general parsing methods
    """

    def __init__(self, item_types, directions, src_ascii_path, src_json_path, dst_ascii_path, dst_json_path):
        self.item_types = item_types
        self.directions = directions
        self.src_ascii_path = src_ascii_path
        self.src_json_path = src_json_path
        self.dst_ascii_path = dst_ascii_path
        self.dst_json_path = dst_json_path

    def generate_random_maze(self, rows, cols, obstacle_rate, start_pos, end_pos):
        """
        Generates a random maze map and writes it to a JSON file.
        :param rows: number of rows of the map
        :param cols: number of cols of the map
        :param obstacle_rate: the rate of obstacle cells
        :param start_pos: the starting position of the maze
        :param end_pos: the goal of the maze
        """
        random_maze = {
            'timestamp': int(time.time()),
            'rows': rows,
            'cols': cols
        }

        obstacles = 0
        item_list = []

        for i in range(rows):
            for j in range(cols):
                item = {'x': i, 'y': j}
                if (i, j) == start_pos:
                    item['type'] = 'start'
                elif (i, j) == end_pos:
                    item['type'] = 'end'
                else:
                    if random.random() > obstacle_rate:
                        item['type'] = 'traversable'
                    else:
                        item['type'] = 'obstacle'
                        obstacles += 1
                item_list.append(item)
        random_maze['maze'] = item_list

        # debug
        print("Obstacles: {} on {} total cells.\n"
              "Expected obstacle rate: {}\n"
              "Actual obstacle rate: {:1.4f}".format(obstacles, rows * cols,
                                                     obstacle_rate, obstacles / (rows * cols)))

        # display the maze and save it to external txt file
        ascii_maze = self.display_maze_from_dict(random_maze, save_to_file=True, print_on_console=False,
                                                 is_solved=False)

        # write the maze to external file
        example_file_path = pathlib.Path.cwd().parent.joinpath('res', self.src_json_path)
        with open(example_file_path, 'w') as f:
            json.dump(random_maze, f, indent=2)

        return random_maze

    def json_to_grid(self):
        """
        Parses a JSON file containing the map and generates a grid using that instance.
        :return: a grid object structured following the given JSON file
        """
        sheet_path = pathlib.Path.cwd().parent.joinpath('res', self.src_json_path)

        with open(sheet_path, 'r') as f:
            parsed_json = json.load(f)
        return self.dict_to_grid(parsed_json)

    @staticmethod
    def dict_to_grid(maze):
        """
        Converts a dictionary to a maze grid.
        :param maze: the dictionary of the maze that has to be converted
        :return: a grid object structured following the given dictionary
        """
        print(f"Rows: {type(maze)}")

        rows = maze['rows']
        cols = maze['cols']
        start_pos_cell = maze['maze'][find_dict_index_in_dict_list(maze['maze'], 'type', 'start')]
        end_pos_cell = maze['maze'][find_dict_index_in_dict_list(maze['maze'], 'type', 'end')]
        start_pos = {'x': start_pos_cell['x'], 'y': start_pos_cell['y']}
        end_pos = {'x': end_pos_cell['x'], 'y': end_pos_cell['y']}

        spots = []
        for s in maze['maze']:
            parsed_spot = Spot(x=s['x'], y=s['y'], spot_type=s['type'])
            spots.append(parsed_spot)

        parsed_grid = Grid(start_coord=start_pos, end_coord=end_pos, rows=rows, cols=cols, spots=spots)
        return parsed_grid

    def ascii_to_dict(self, maze, load_from_file):
        """
        Converts a maze from ascii format to dictionary
        :param maze: the maze that is going to be converted
        :param load_from_file: load ascii string from file if set to True
        :return: the dictionary containing the maze map
        """
        # load maze lines
        maze_lines = []

        if load_from_file:
            maze_path = pathlib.Path.cwd().parent.joinpath('res', self.src_ascii_path)
            with open(maze_path, 'r') as f:
                for line in f:
                    maze_lines = line
        else:
            print(f"Maze: {maze}\n"
                  f"type: {type(maze)}")
            maze_lines = maze.split('\\n')

        #  print(f"Maze lines: {maze_lines}\ntype: {type(maze_lines)}")

        # string processing
        lines = []
        for line in maze_lines:
            if line != '':
                line = re.sub(r"(\d|\s)+", '', line)  # remove any digit or whitespace
                if len(line) == 0:  # skip line if empty
                    continue
                else:
                    line = re.sub(r"'+", '', line)  # remove new lines characters
                    line = re.sub(r"\\n", '', line)  # remove superscript characters
                    lines.append(line)

        print(f"Lines {lines}")

        conversion_map = swap_key_value(self.item_types)

        # structure extraction
        maze_dict = {
            'timestamp': int(time.time()),
            'rows': len(lines),
            'cols': len(lines[0])
        }
        cells = []

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

    def save_dict_to_json(self, dic):
        """
        Writes a dictionary to the given json file
        :param dic: the dictionary that has to be written
        """
        file_path = pathlib.Path.cwd().parent.joinpath('res', self.dst_json_path)
        with open(file_path, 'w'):
            json.dump(dic, file_path)
        pass

    def ascii_to_grid(self, maze, load_from_file):
        """
        Creates a maze grid from a ascii string contained in the given file
        :param maze: the string that is going to be converted
        :param load_from_file: load ascii string from file if set to True
        :return: the grid created from the parsed ascii string
        """
        parsed_dict = self.ascii_to_dict(maze=maze, load_from_file=load_from_file)
        print(f"Parsed dictionary: {parsed_dict}")
        parsed_grid = self.dict_to_grid(parsed_dict)
        return parsed_grid

    def dict_maze_to_ascii(self, maze, print_on_console):
        """Converts the maze map using ascii character
        :param maze: the map that needs to be converted
        :param print_on_console: print the maze on the console if True
        :return: the structure of the maze just printed
        """
        lines = []

        for i in range(maze['rows']):
            ascii_line = ''
            for j in range(maze['cols']):
                current_element_type = maze['maze'][i * maze['cols'] + j]['type']
                # print("({},{}): {}".format(i, j, current_element_type))
                ascii_line += self.item_types[current_element_type] + ' '
            if print_on_console:
                print(ascii_line)
            lines.append(ascii_line)
        return '\n'.join(lines)

    def display_maze_from_dict(self, maze, save_to_file, print_on_console, is_solved):
        """
        Converts the maze map using ascii character
        :param maze: the map that needs to be converted
        :param save_to_file: save the maze to file if True
        :param print_on_console: print the maze on the console if True
        :param is_solved: flag that tells if the maze passed as parameter
            is already solved (contains cells of type: 'solution')
        :return: the structure of the maze just printed
        """
        ascii_maze = self.dict_maze_to_ascii(maze=maze, print_on_console=print_on_console)

        if save_to_file:
            if is_solved:
                # save to destination file
                file_path = pathlib.Path.cwd().parent.joinpath('res', self.dst_ascii_path)
            else:
                # save to source file
                file_path = pathlib.Path.cwd().parent.joinpath('res', self.src_ascii_path)
            with open(file_path, 'w') as f:
                f.write(ascii_maze)
        return ascii_maze

    def display_solution_from_dict(self, maze, maze_solution, save_to_file, print_on_console):
        """
        Prints the maze map with the solution calculated and saves it to an external file
        :param maze: the maze without the solution path
        :param maze_solution: the list of spots to follow to complete the maze
        :return: the solved maze in dict format
        """

        rows = maze['rows']
        cols = maze['cols']

        # print(f"Maze solution:{maze_solution}")
        # merge the maze with the solution giving the priority to the solution
        merged_dict_list = merge_dict_lists_on_specific_keys_with_priority(l1=maze['maze'], l2=maze_solution,
                                                                           duplicates=False,
                                                                           priority=2,
                                                                           comparison_keys=['x', 'y'])
        # reconstruct the maze in order to display and save it
        # print(f"Merged_maze {merged_dict_list}")
        solved_maze = {
            'rows': rows,
            'cols': cols,
            'maze': merged_dict_list
        }
        maze_solved_ascii = self.display_maze_from_dict(maze=solved_maze, save_to_file=save_to_file,
                                                        print_on_console=print_on_console, is_solved=True)
        return solved_maze

    @staticmethod
    def pack_moves(actions):
        """
        Packs the action string such as multiple action moves in a row are
        substituted with the number that indicates the consecutive moves.
        :param actions: the actions that the entity has to follow
        :return: the packed string of actions
        """
        packed_actions = ''
        previous_moves_counter = 0

        for current_action in actions:
            if current_action == '1':  # the current action is M
                previous_moves_counter += 1
            else:  # current action is R
                if previous_moves_counter != 0:
                    packed_actions += str(previous_moves_counter)
                previous_moves_counter = 0
                packed_actions += str(current_action)

        if previous_moves_counter != 0:
            packed_actions += str(previous_moves_counter)

        return packed_actions

    def path_to_moves(self, maze_solution_path, starting_orientation='N'):
        """
        Convert the maze solution to a dictionary containing the moves that
        the entity will follow in order to complete the game
        :param maze_solution_path: the maze solution
        :param starting_orientation: the starting orientation of the entity. By default it is set to North (UP)
        :return: the string containing the solution converted in entity actions
        """
        actions = ''
        current_orientation = starting_orientation

        for i, current_cell in enumerate(maze_solution_path[:-1]):
            next_cell = maze_solution_path[i + 1]
            starting_move = True if i == 0 else False
            next_actions, current_orientation = self.move_to_actions(current_cell=current_cell, next_cell=next_cell,
                                                                     previous_orientation=current_orientation,
                                                                     starting_move=starting_move)
            actions += next_actions

        actions = self.pack_moves(actions)
        return actions

    def move_to_actions(self, current_cell, next_cell, previous_orientation, starting_move):
        """
        Returns the moves that the entity has to follow in order to achieve the given steps.
        :param current_cell: the current position
        :param next_cell: the next position
        :param previous_orientation: the previous orientation of the entity
        :param starting_move: flag that tells if the current move is the first. This flag is necessary since the first
                move is the only one that can lead to a multiple rotation.
        :return: the moves that the entity has to follow in order to achieve the move indicated from the couple of steps
        """

        # available actions: rotate (R), move forward (M)
        # available rotation directions: +90° (+), -90° (-), 0 (blank)
        actions = ''

        # identify the direction of the movement
        if current_cell['y'] > next_cell['y']:  # moving left (W)
            movement_direction = 'W'
        elif current_cell['y'] < next_cell['y']:  # moving right (E)
            movement_direction = 'E'
        else:  # moving up or down (N|S)
            if current_cell['x'] > next_cell['x']:  # moving down (S)
                movement_direction = 'N'
            else:  # moving up (N)
                movement_direction = 'S'

        next_orientation = previous_orientation

        # check if the entity needs to rotate before moving to the next cell
        if previous_orientation != movement_direction:
            if starting_move:  # we can't assume that the entity will have to rotate once by 90°
                if self.directions[(self.directions.index(previous_orientation) + 1) % len(
                        self.directions)] != movement_direction:  # rotation by +90° isn't enough
                    if self.directions[(self.directions.index(previous_orientation) + 2) % len(
                            self.directions)] != movement_direction:  # rotation by +180° isn't enough
                        rotation_direction = '-'  # since +180° isn't enough we can
                        # assume that the desired rotation is +270° = -90°
                    else:  # +180°
                        rotation_direction = '++'
                else:  # +90°
                    rotation_direction = '+'
            else:  # we can assume that the maximum rotation required is 90°
                if self.directions[(self.directions.index(previous_orientation) + 1) %
                                   len(self.directions)] == movement_direction:
                    rotation_direction = '+'
                else:
                    rotation_direction = '-'
            actions = rotation_direction
            next_orientation = movement_direction
        else:  # the previous orientation was already in the direction of the movement
            pass

        return actions + '1', next_orientation
