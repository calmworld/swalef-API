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
      current_user = model_to_dict(current_user)
    except:
      return jsonify(data={}, status={"code": 401, "message": "Token is invalid"})
    
    return f(current_user, *args, **kwargs)
  return decorated


# index
@posts.route('/', methods=["GET"])
def get_all_posts():
  try:
    posts = [model_to_dict(post) for post in models.Posts.select().limit(3)]
    print(posts)
    return jsonify(data=posts, status={"code": 200, "message": "success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "error getting the data"})


# create
@posts.route('/', methods=["POST"])
@login_check
def create_post(current_user):
  payload = request.get_json()
  # print(payload)
  new_post = models.Posts.create(title=payload['title'], body=payload['body'], topic=payload['topic'], created_by=current_user['id'])
  post_dict = model_to_dict(new_post)
  #hide the user who created the posts password
  del post_dict['created_by']['password']

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
@login_check
def update_post(current_user, id):
  payload = request.get_json()
  query = models.Posts.update(**payload).where(models.Posts.id == id)
  query.execute()
  return jsonify(data=model_to_dict(models.Posts.get_by_id(id)), status={"code": 200, "message": "success"})


# delete
@posts.route('/<id>', methods= ["DELETE"])
@login_check
def delete_post(current_user, id):
  post = models.Posts.get_by_id(id)
  post_dict = model_to_dict(post)
  print(post_dict)
  query1 = models.Comments.delete().where(models.Comments.parent_post == id)
  query = models.Posts.delete().where(models.Posts.id == id)
  query1.execute()
  query.execute()
  return jsonify(data=post_dict, status={"code": 200, "message": "success, deleted"})


#Show User posts
@posts.route('/myposts', methods=["GET"])
@login_check
def user_feeds(current_user):
  user = models.Users.get_by_id(current_user['id'])
  feeds = [model_to_dict(feed) for feed in user.posts]
  return jsonify(data=feeds, status={"code": 200, "message": "user feeds success"})


#sort route
@posts.route('/sort/<topic>', methods=["GET"])
def testing(topic):
  feeds = ''
  if topic == 'recent':
    feeds_query = models.Posts.select().order_by(-models.Posts.created_at).limit(10)
    feeds = [model_to_dict(feed) for feed in feeds_query]
  elif topic == 'all':
    feeds_query = models.Posts.select()
    feeds = [model_to_dict(feed) for feed in feeds_query]
  else:
    testing = models.Posts.select().where(models.Posts.topic == topic)
    feeds = [model_to_dict(feed) for feed in testing]
    print(feeds)
  return jsonify(data=feeds, status={"code": 200, "message": "successfully filtered"})


