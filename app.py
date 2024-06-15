from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///consumable.db'

db=SQLAlchemy(app)

class Consumable(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(50))
    quantity=db.Column(db.String(50))#, primary_key = True)

    def __init__(self, name, quantity):
        self.name=name
        self.quantity=quantity

with app.app_context():#создание БД
    db.create_all()


@app.route('/add_consumables', methods=['POST'])#метод записи расходников
def add_consumables():
    name = request.form['name']
    quantity = request.form['quantity']
    consumable = Consumable(name, quantity)
    db.session.add(consumable)
    db.session.commit()
    return{"success":"Consumable added successfully"}


@app.route('/get_consumables/<int:id>')#метод получения расходников
def get_consumables(id):
    consumable = Consumable.query.get(id)
    if consumable:
        return jsonify({
            'id': consumable.id,
            'name': consumable.name,
            'quantity': consumable.quantity
        })
    else:
        return{'error':'Consumable not found'}



if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
