from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        #return a store model
        store = StoreModel.find_by_name(name)

        if store:
            #would be 200 but that is default so don't need it
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'A store with the name {name} already exists.'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            #500 code since it is a problem on the dabatase not user error.
            return {'message': 'An error occured while creating the store'}, 500         

        #201 as it has been added to the db
        return store.json(), 201

    def delete(self, name):

        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted.'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}