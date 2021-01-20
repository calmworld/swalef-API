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


@posts.route('/<id>', methods=["GET"])
def get_one_post(id):
  post = models.Posts.get_by_id(id)
  print(post.__dict__)
  return jsonify(data=model_to_dict(post), status={"code": 200, "message": "success"})


@posts.route('/<id>', methods=["PUT"])
def update_post(id):
  payload = request.get_json()
  query = models.Posts.update(**payload).where(models.Posts.id == id)
  query.execute()
  return jsonify(data=model_to_dict(models.Posts.get_by_id(id)), status={"code": 200, "message": "success"})

@posts.route('/<id>', methods= ["DELETE"])
def delete_post(id):
  post = models.Posts.get_by_id(id)
  post_dict = model_to_dict(post)
  print(post_dict)
  query = models.Posts.delete().where(models.Posts.id == id)
  query.execute()
  return jsonify(data=post_dict, status={"code": 200, "message": "success, deleted"})