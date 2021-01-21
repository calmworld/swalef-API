import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict
import jwt
from functools import wraps

comments = Blueprint('comments', 'comment', url_prefix='/comments')


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
            current_user = model_to_dict(current_user)
        except:
            return jsonify(data={}, status={"code": 401, "message": "Token is invalid"})
        
        return f(current_user, *args, **kwargs)
    return decorated


# create
@comments.route('/<id>', methods=["POST"])
@login_check
def create_comment(current_user, id):
    payload = request.get_json()
    new_comment = models.Comments.create(body=payload['body'], parent_post=id, created_by=current_user['id'])
    comment_dict = model_to_dict(new_comment)
    del comment_dict['created_by']['password']
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

