from app import db

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String())
    item_description = db.Column(db.String())
    item_price = db.Column(db.Integer())

    def __init__(self, item_name, item_description, item_price):
        self.item_name = item_name
        self.item_description = item_description
        self.item_price = item_price

    def __repr__(self):
        return '<id {}>'.format(self.id)

    @staticmethod
    def to_dict(menu):
        dct = {
            "id": menu.id,
            "item_name": menu.item_name,
            "item_description": menu.item_description,
            "item_price": menu.item_price,
        }

        return dct


    @staticmethod
    def to_list_dict(menus):
        return {
            "metaData": {
            },
            "items": [Menu.to_dict(menu) for menu in menus]
        }
