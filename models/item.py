from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    #precision is numbers after the decimal point
    price = db.Column(db.Float(precision=2))

    #links store and store_id to Store Model
    #this also shows that there can only be one store attached to an item because of the stores.id
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        #create an item model within items where name is equal to variable name
        return cls.query.filter_by(name=name).first() #selecting first oonly
              
#this upserts or updates and or inserts to the database
#so we combined the insert and update              
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

