from flask import Blueprint


users = Blueprint('users', __name__)

@users.route('/')
def user_index():
    return {'msg': 'Success', 'blueprint': 'users'}