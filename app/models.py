from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False, Required=True)
    username = db.Column(db.String(64), index=True)
    firebase_uid = db.Column(db.Integer)
    canvas_key = db.Column(db.String(128), index=True)
    todoist_key = db.Column(db.String(128), index=True)

    
    @property
    def canvas_key(self):
        return self.canvas_key

    @canvas_key.setter
    def hash_canvas_key(self, key):
        self.canvas_key = generate_password_hash(key)

    @property
    def is_correct_canvas_key(self, key):
        return check_password_hash(self.canvas_key, key)


    @property
    def todoist_key(self):
        return self.todoist_key

    @todoist_key.setter
    def hash_todoist_key(self, key):
        self.canvas_key = generate_password_hash(key)

    @property
    def is_correct_todoist_key(self, key):
        return check_password_hash(self.todosit_key, key)


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    



