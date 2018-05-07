from flask import Flask

app = Flask(__name__)


@app.route("/")
def show_dashboard():
    placeholder_msg = "Imagine a beautiful dashboard here!"
    return placeholder_msg
