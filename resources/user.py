import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    #define the requeseted parameters that will be included in data within POST
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="this field cannot be left blank!"
    )
    
    def post(self):
        data = UserRegister.parser.parse_args()

        #check to see if that username already exists
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201