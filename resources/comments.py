import models

from flask import Blueprint('comments', 'comment', url_prefix='/comments')


@comments.route('/<id>', methods=["POST"])
def create_comment(id):
    payload = request.get_json()
    new_comment = models.Comments.create(body=payload['body'], parent_post=id)
    comment_dict = model_to_dict(new_comment)
    return jsonify(data=comment_dict, status={"code": 200, "message": "comment added"})