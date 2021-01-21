import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict

comments = Blueprint('comments', 'comment', url_prefix='/comments')

# create
@comments.route('/<id>', methods=["POST"])
def create_comment(id):
    payload = request.get_json()
    new_comment = models.Comments.create(body=payload['body'], parent_post=id)
    comment_dict = model_to_dict(new_comment)
    return jsonify(data=comment_dict, status={"code": 200, "message": "comment added"})

# update
@comments.route('/<id>', methods=["PUT"])
def update_comment(id):
    payload = request.get_json()
    query = models.Comments.update(**payload.where(models.Comments.id == id))
    query.execute()
    return jsonify(data=model_to_dict(models.Comments.get_by_id(id)), status={"code": 200, "message": "comment updated successfully"})

# delete
@comments.route('/<id>', methods= ["DELETE"])
def delete_comment(id):
  comment = models.Comments.get_by_id(id)
  comment_dict = model_to_dict(comment)
  # print(comment_dict)
  query = models.Comments.delete().where(models.Comments.id == id)
  query.execute()
  return jsonify(data=comment_dict, status={"code": 200, "message": "success, deleted"})

