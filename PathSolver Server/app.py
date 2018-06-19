from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'])
def find_path():
    # TODO
    pass


# run here
if __name__ == '__main__':
    app.run(port=5000)
