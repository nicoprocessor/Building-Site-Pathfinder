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
    maze = args['maze']
    starting_orientation = args['starting_orientation']
    solution = solve_maze(maze=maze, starting_orientation=starting_orientation)
    # solution = {'moves': moves, 'solution_steps': solution_steps,
    # 'entity_moves': entity_moves, 'compression_rate': compression_rate}

    print(f"Starting orientation: {starting_orientation}\n"
          f"Moves: {solution['moves']}\n"
          f"Solution steps: {solution['solution_steps']}\n"
          f"Entity moves: {solution['entity_moves']}\n"
          f"Compression rate: {solution['entity_moves']:.3f}")
    return jsonify(solution)


# run here
if __name__ == '__main__':
    app.run(port=5000)
