from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os #To set out file paths

# Initialiaze the app
app = Flask(__name__)
#Settting up the base directory - this allows us to locate the path to the database

basedir = os.path.abspath(os.path.dirname(__file__))

#Confirg settings for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This is optional

#Setting up a database object
db = SQLAlchemy(app)

#Initialiaze Marshmellow - Note the order of initializing db and ma matters
ma = Marshmallow(app)

#Setting up a Model class
class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=True)
  description = db.Column(db.String(200))
  price = db.Column(db.Float)
  qty = db.Column(db.Integer)

  def __init__(self, name, description, price, qty):
    self.name = name
    self.description = description
    self.price = price
    self.qty = qty

# Product Schema - THis is used to define the output format with the use of marshmellow
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'name', 'description', 'price', 'qty')


# Init schema
product_schema = ProductSchema() #This is used to serialiaze the product that is to be sent back
products_schema = ProductSchema(many=True) # Used to serialize many products

#Route 1: Creating a product
@app.route('/product', methods=["POST"])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product(name, description, price, qty)

    db.session.add(new_product)
    db.session.commit()

    return product_schema.jsonify(new_product)

# Route 2: Get All Products
@app.route('/product', methods=['GET'])
def get_products():
  all_products = Product.query.all()
  app.logger.info(all_products) # Print information on console
  result = products_schema.dump(all_products)
  return jsonify(result)

# ROute 3: Get a Single Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
  product = Product.query.get(id)
  return product_schema.jsonify(product)

'''
products_schema.dump(all_products) # Used when dealing with an array of items
product_schema.jsonify(product) # Used when dealing with a single item

'''
# Route 3: UPdate Product
@app.route('/product/<id>', methods=['PUT'])
def update_product(id):
  product = Product.query.get(id)

  name = request.json['name']
  description = request.json['description']
  price = request.json['price']
  qty = request.json['qty']

  product.name = name
  product.description = description
  product.price = price
  product.qty = qty

  db.session.commit()

  return product_schema.jsonify(product)

# Route 4: Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def delete_product(id):
  product = Product.query.get(id)
  db.session.delete(product)
  db.session.commit()

  return product_schema.jsonify(product)


@app.route('/', methods=["GET"])
def test():
    return jsonify({'msg': "Hello World"})
       
#Run Server      
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  