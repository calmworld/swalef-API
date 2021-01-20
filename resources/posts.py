import models

from flask import Blueprint, jsonify, request
from playhouse.shortcuts import model_to_dict 

posts = Blueprint('swalef', 'post', url_prefix='swalef')

@posts.route('/', methods=["GET"])
def get_all_posts():
  return "hello from the index route" 