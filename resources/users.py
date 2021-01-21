import models

from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from playhouse.shortcuts import model_to_dict
import jwt
import datetime

users = Blueprint('users', 'user', url_prefix='/users')


#sign up
@users.route('/create', methods=["POST"])
def create_user():
  payload = request.get_json()
  try:
    models.Users.get(models.Users.username == payload['username'])
    return jsonify(data={}, status={"code": 401, "message": "A user already exists under this name"})
  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password'])
    user = models.Users.create(**payload)

    user_dict = model_to_dict(user)
    del user_dict['password']
    return jsonify(data=user_dict, status={"code" : 201, "message": "User successfully created"})




#log in
@users.route('/login', methods=["POST"])
def login():
  payload = request.get_json()
  try:
    user = models.Users.get(models.Users.username == payload['username'])
    user_dict = model_to_dict(user)
    if(check_password_hash(user_dict['password'], payload['password'])):
      token = jwt.encode({'id': user_dict['id'], 'username': user_dict['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 'THISISASECRETKEY')
      del user_dict['password']
      return jsonify(data={"token": token.decode('UTF-8')}, status={"code": 200, "message": "User logged in"})
    else:
      return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "username or password is incorrect"}) 