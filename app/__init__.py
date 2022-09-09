from flask import Flask
from app.routes.users import users
from app.routes.tasks import tasks
import os



app =  Flask(__name__)

app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(tasks, url_prefix='/tasks')



app.secret_key = os.getenv('somerandomstring')


@app.route('/')
def index():
    return {'status': 'success', 'msg': 'Server is live!'}