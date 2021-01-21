import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict 
from functools import wraps
import jwt


posts = Blueprint('swalef', 'post', url_prefix='swalef')

# creating decorators was taken from https://www.youtube.com/watch?v=WxGBoY5iNXY
# token_required = login_check
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
      return jsonify(data={}, status={"code": 401, "message": "Token has expired"})
    
    return f(current_user, *args, **kwargs)
  return decorated

# index
@posts.route('/', methods=["GET"])
@login_check
def get_all_posts(current_user):
  try:
    posts = [model_to_dict(post) for post in models.Posts.select()]
    print(posts)
    return jsonify(data=posts, status={"code": 200, "message": "success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "error getting the data"})


# create
@posts.route('/', methods=["POST"])
def create_post():
  payload = request.get_json()
  print(payload)
  new_post = models.Posts.create(**payload)
  post_dict = model_to_dict(new_post)
  return jsonify(data=post_dict, status={"code": 200, "message": "success"})

# show
@posts.route('/<id>', methods=["GET"])
def get_one_post(id):
  post = models.Posts.get_by_id(id)
  post_dict = model_to_dict(post)
  comments = [model_to_dict(comment) for comment in post.comments]
  feed = {"feed": post_dict, "comments": comments}
  return jsonify(data=feed, status={"code": 200, "message": "success"})

# update
@posts.route('/<id>', methods=["PUT"])
def update_post(id):
  payload = request.get_json()
  query = models.Posts.update(**payload).where(models.Posts.id == id)
  query.execute()
  return jsonify(data=model_to_dict(models.Posts.get_by_id(id)), status={"code": 200, "message": "success"})

# delete
@posts.route('/<id>', methods= ["DELETE"])
def delete_post(id):
  post = models.Posts.get_by_id(id)
  post_dict = model_to_dict(post)
  print(post_dict)
  query = models.Posts.delete().where(models.Posts.id == id)
  query.execute()
  return jsonify(data=post_dict, status={"code": 200, "message": "success, deleted"})