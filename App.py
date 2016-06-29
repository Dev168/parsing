import sys
sys.path.append("C:\\Users\\Administrator\\PycharmProjects\\BookmakerPlus")

from flask import Flask
from flask import render_template
from forks_searching.search import get_forks
from gevent import wsgi



app = Flask(__name__)

@app.route("/")
def index():

    posts = get_forks()

    return render_template("index.html", posts = posts)


server = wsgi.WSGIServer(('', 5000), app)
server.serve_forever()