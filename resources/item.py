from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

#create new resource, this is the item resource and define the get request
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="this field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="every item needs a store id!"
    )


    #decorator that requeres a jwt token
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

#post must pass the same variable as GET

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists.'}, 400

        #parse data
        data = Item.parser.parse_args()

        #create item based on parsed data
        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500 #internal server error

        return item.json(), 201


    def delete(self, name):

        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {"message": "Item deleted."}

    def put(self, name):
        #using a parser to only accept specific keys into payload
        data = Item.parser.parse_args()

        #find item in database
        item = ItemModel.find_by_name(name)

        #if item does not exist, insert it
        if item is None:
        #create a model that is item.
            item = ItemModel(name, data['price'], data['store_id'])
        else:
        #if it does exists, change the model price to the data price
            item.price = data['price']
            item.store_id = data['store_id']

        #commit the save
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}