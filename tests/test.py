from flask import Flask
from flask import render_template

def get_forks():
    posts = []
    return posts


app = Flask(__name__)
@app.route("/")

def index():

    posts = get_forks()

    return render_template("table.html",

        posts = posts)

if __name__ == "__main__":
    app.run()