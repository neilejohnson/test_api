#import modules
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


#these are from my own security.py module
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

#create app and api
app = Flask(__name__)

#tell SQL Alchemy that our database lives in the root folder at data.db
#can use oracle or mysql and you can define them below. doesn't need to be sqlite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#SQL ALCHEMY SET TO NOT TRACK MODIFICATIONS AS THIS USES UP PROCESSING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'

api = Api(app)

#this will create a new endpoint that is /auth
jwt = JWT(app, authenticate, identity)

items = []


#add resource to api and point to an endpoint with string variable for the name.
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

#run the app at port 5000. This is uaully default
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)