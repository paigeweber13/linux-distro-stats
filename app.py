from flask import Flask, render_template

import linuxstats.test_page

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/test-page")
def display_test_page():
    return linuxstats.test_page.main()

# @app.route("/js/<script_name>")
# def resolve(script_name):
#     return 'wip'

# @app.route("/hello")
# def hello():
#     return "Hello world!"
