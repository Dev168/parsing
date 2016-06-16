

from flask import Flask
from flask import render_template
app = Flask(__name__)
@app.route("/")



def index():


    posts = [
        {   'event' : 'Rus-Eng',
            'percent': "10%",
            'name': "England win",
             'coeff': "2.05",
                      "href": "vk1.com"

        },
        {
            'event' : 'Rus-Por',
            'percent': "11%",
            'name': "Rus win",
             'coeff' :"3.05",
            "href": "vk.com"
        }








    ]


    return render_template("table.html",

        posts = posts)

if __name__ == "__main__":
    app.run()