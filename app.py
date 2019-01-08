from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/bobs_burger'
app.debug = False

db = SQLAlchemy(app)

class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(), unique=True)
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

@app.route('/menu/<id>', methods=['GET'])
def getMenu(id):
    try:
        results = db.session.query(Menu).get(id)
        if results is None:
            return "record id {} is not found".format(id), 404
        response = Menu.to_list_dict([results])
        return jsonify(response), 200
    except Exception as e:
        return "{}".format(e), 500

@app.route('/menu', methods=['GET'])
def getMenus():
    results = Menu.query.all()
    response = Menu.to_list_dict(results)
    return jsonify(response), 200

@app.route('/menu', methods=['POST'])
def createMenu():
    content = request.json
    print("Request: {}".format(content))
    menu = Menu(content['item_name'], content['item_description'], content['item_price'])
    try:
        db.session.add(menu)
        db.session.commit()
        db.session.refresh(menu)
        return jsonify(Menu.to_list_dict([menu])), 201
    except exc.IntegrityError as i:
        print(f"Integrity: {i.orig}")
        return "{}".format(i.orig), 409
    except Exception as e:
        print("Eception: {}".format(e))
        return "{}".format(e.orig), 500

if __name__ == '__main__':
    app.run(port=5000)