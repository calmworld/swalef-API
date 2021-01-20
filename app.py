from flask import Flask, jsonify, g
from flask_cors import CORS
import os

import models
from resources.posts import posts

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.register_blueprint(posts, url_prefix='/swalef')

@app.before_request
def before_request():
    """Connect to the database before each request."""
    print("you should see this before each request")
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """Close db after each request"""
    print("you should see this after each request")
    g.db.close()
    return response

# The default URL ends in / ("my-website.com/").
@app.route('/')
def index():
    return 'Hey check this out'

if 'On_HEROKU' in os.environ:
    print('\non Heroku!')
    models.initialize()

# run app
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)