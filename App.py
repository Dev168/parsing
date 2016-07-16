import sys
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\BookmakerPlus")
from flask import Flask
from flask import render_template
from forks_searching.search import get_forks
import json
import time


app = Flask(__name__)

@app.route("/")
def index():

    t1=time.time()
    posts = get_forks()
    t2 = time.time()
    perf = t2- t1
    perf = str(round(perf, 3)) + " sec"

    return render_template("index.html", posts=posts, perf=perf)

@app.route("/forks")
def forks():

    return json.dumps(get_forks(), indent=4)
