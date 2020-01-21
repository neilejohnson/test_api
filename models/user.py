import sqlite3
from db import db

#define User class that is used in security.
class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

#class method used to authenticate. it accepts one parameter besides the cls, which is username
#it queries the data.db database for that username. 
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
#returns that user information as the User class which will be used in securite.py to authenticate

    @classmethod
    def find_by_id(cls, _id):
        #the column in db is id but here _id is the variable name in python
        return cls.query.filter_by(id=_id).first()