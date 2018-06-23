from flask import Flask, request, jsonify

from models.maze_interface import solve_maze

app = Flask(__name__)


@app.route('/', methods=['GET'])
def solve():
    """
    Solve the maze instance
    :return: the string of instructions that the entity has
            to follow in order to solve the maze
    """
    args = request.args.to_dict()
    entity_actions, solution_steps, entity_moves, compression_rate = solve_maze(maze=args['maze'],
                                                                                starting_orientation=args[
                                                                                    'starting_orientation'])
    if entity_actions == '0':
        return jsonify(entity_actions)
    else:
        return jsonify(entity_actions, solution_steps, entity_moves, compression_rate)


# run here
if __name__ == '__main__':
    app.run(port=5000)
