from flask import Flask, request

from models.maze_interface import solve_maze

app = Flask(__name__)


@app.route('/', methods=['GET'])
def solve():
    args = request.args.to_dict()
    entity_actions = solve_maze(maze=args['maze'],
                                starting_orientation=args['starting_orientation'])
    return entity_actions



# run here
if __name__ == '__main__':
    app.run(port=5000)
