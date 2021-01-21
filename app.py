from flask import Flask, jsonify, g, request
from flask_cors import CORS
import os
from functools import wraps
import jwt
from playhouse.shortcuts import model_to_dict
import models
from resources.posts import posts
from resources.comments import comments
from resources.users import users


def login_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify(data={}, status={"code": 401, "message" : "Login required"})

        try:
            data = jwt.decode(token, 'THISISASECRETKEY')
            current_user = models.Users.get(models.Users.id == data['id'])
        except:
            return jsonify(data={}, status={"code": 401, "message": "Token is invalid"})

        return f(current_user, *args, **kwargs)
    return decorated


DEBUG = True
PORT = 8000

app = Flask(__name__)

CORS(posts, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(posts, url_prefix='/swalef')

CORS(comments, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(comments, url_prefix='/comments')

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(users, url_prefix='/users')

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
# def index():
#     return 'Hey check this out'

@login_check
def index(current_user):
    user_dict = model_to_dict(current_user)
    return jsonify(data=user_dict, status={"code": 200, "message": "session is valid"})


if 'On_HEROKU' in os.environ:
    print('\non Heroku!')
    models.initialize()


# run app
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)