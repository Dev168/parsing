import sys
from flask import Flask
from flask import render_template, request
sys.path.append("C:\\Users\\Vlad\\PycharmProjects\\BookmakerPlus")
from forks_searching.search import get_forks
import time
import rest_api


app = Flask(__name__)


@app.route("/")
def index():

    t1 = time.time()
    posts = get_forks()

    t2 = time.time()
    perf = t2- t1
    perf = str(round(perf, 3)) + " sec"

    return render_template("index.html", posts=posts, perf=perf)


@app.route("/editor")
def editor():

    return render_template("editor.html")


@app.route("/api/getSportsList")
def get_sports_list():
    return rest_api.get_sports_select_list()


@app.route("/api/getLeaguesList")
def get_leagues_list():
    sportuuid = request.args.get('uuid')
    return rest_api.get_leagues_select_list(sportuuid)


@app.route("/api/getParticipants")
def get_participants():
    leagueuuid = request.args.get('uuid')
    return rest_api.get_participants(leagueuuid)


@app.route("/api/getLeagues")
def get_leagues():
    sportuuid = request.args.get('uuid')
    return rest_api.get_leagues(sportuuid)


@app.route("/api/getSports")
def get_sports():
    return rest_api.get_sports()
