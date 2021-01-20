import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict 

posts = Blueprint('swalef', 'post', url_prefix='swalef')

@posts.route('/', methods=["GET"])
def get_all_posts():
  try:
    posts = [model_to_dict(post) for post in models.Posts.select()]
    print(posts)
    return jsonify(data=posts, status={"code": 200, "message": "success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "error getting the data"})

@posts.route('/', methods=["POST"])
def create_post():
  payload = request.get_json()
  print(payload)
  new_post = models.Posts.create(**payload)
  post_dict = model_to_dict(new_post)
  return jsonify(data=post_dict, status={"code": 200, "message": "success"})
