import sys
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\BookmakerPlus")
from flask import Flask
from flask import render_template
from forks_searching.search import get_forks
import json


app = Flask(__name__)

@app.route("/")
def index():

    posts = get_forks()

    return render_template("index.html", posts = posts)

@app.route("/forks")
def forks():

    return json.dumps(get_forks(), indent=4)
