from app import app
import os


app.secret_key = os.getenv('somerandomstring')


@app.route('/')
def index():
    return {'status': 'success', 'msg': 'Welcome to the homepage'}