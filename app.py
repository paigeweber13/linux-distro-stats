from flask import Flask, render_template

import linuxstats.stats

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/distro-stats")
def get_distro_stats():
    return stats.main()

# @app.route("/js/<script_name>")
# def resolve(script_name):
#     return 'wip'

# @app.route("/hello")
# def hello():
#     return "Hello world!"
