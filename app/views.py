from flask import Flask

from dotenv_utils import get_host, get_port

app = Flask("analizer")

@app.route("/", methods=['GET'])
def index():
    return "it's work."


def run_flask():
    app.run(host=get_host(), port=get_port())
    