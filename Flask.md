# Flask - Tech with Tim

To install flask into the system run 

`pip install flask`

Once installed navigate to the project folder and create a file `myApp.py`. This will be the base of the application. This file will be similar to the `views.py` file in *Django*. In that it controls the logic of the application.

To setup the application, on the `myApp.py` , we write:

```python
#First import Flask
from flask import Flask

#Second Create an Instance of Flask Web App
app = Flask(__name__)


if __name__ == '__main__':
    app.run()
```

The above code is used to initialize a *flask application*, to run the code 

`python myApp.py` 

In our case the application will run under the local host pot `http://127.0.0.1:5000`.

## Initializing a Page

Next defining the pages on the website, lets start with the **home page**, in the `myApp.py`. To make a page, we create a function that returns what is to be displayed in the page.

```python
def home():
    return "Hello! This is the main page <h1>HELLO</h1>
```

To define how to get to the function, we add the route/path to the function. To do so we decorate the function with `@app.route("/")`. 

Hence to create a single page the `myApp.py`, will be as shown below

```python
#First import Flask
from flask import Flask

#Second Create an Instance of Flask Web App
app = Flask(__name__)

#Creating a page
@app.route("/")
def home():
    return "Hello! This is the main page <h1>HELLO</h1>"

if __name__ == '__main__':
    app.run()
```

Testing other functionalities,

* To pass a variable from the url path to the function

  ```python
  @app.route("/<name>")
  def user(name):
      return f"Hello {name}"
  
  ```

  

* To redirect a user to another page, in this case we want to redirect a user from the **admin page** into the **home page**. First we will have to import `redirect` and `url_for` from `flask`. Secondly when we write the function, the `url_for` will receive the name of the function that we want to redirect to, in this case the `home` function. Note that we use the function name and not the functions path.

  ```python
  @app.route("/admin")
  def admin():
      return redirect(url_for("home"))
  ```



* To redirect to a function that accepts and arguments:

  ```python
  @app.route("/adminUser")
  def adminUser():
      return redirect(url_for("user", name="Admin!"))
  ```

  

So far to observe any change, we had to close and restart the server, to make any change to reflect in the browser, we can set the debug mode to true. We do this in two way, firstly the app instance we can write ` app.debug = True`, or pass it to the run as `debug = True`.



Also placing a slash (**/** ) after the route will enable the user to access the page with or without the slash in the path of the page

```python
@app.route("/admin/")
def admin():
    return redirect(url_for("home"))
```





## Templates

To render HTML into the page, we will first import `render_template`, to the `myApp.py` file. In this case, it is preferable to place the HTML files into a folder `templates` , located under our route directory. 

Creating and index.html and placing it into templates folder

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Tutorial</title>
</head>
<body>
    <h1>Home Page</h1>
    <p>Hello World</p>
    <p>Hello {{content}}/ {{2}}</p>
    
</body>
</html>
```



To the the page, in `myApp.py`, we write

``` python
@app.route("/")
def home():
    return render_template("index.html")
```



When the above is run, the page will render the html page.

To pass an  argument into the page, we use the curly brackets syntax on the html and on the function, we write the code

```python
@app.route("/<name>")
def user(name):
    return render_template("index.html", content=name, r = 2)
```



To write a python logic on to the template we use the {%...%}, syntax as shown below

```python+html
{% for x in range(10)%}
   {%if x%2 == 1%}
      <p>{{x}}</p>
   {%endif%}
{%endfor%}
```

To pass a list to the template

```python
@app.route("/list")
def list():
    return render_template("index.html", content=["Joe", "Peter", "Mary"], r=2)
```



## Template inheritance 

It works similar to the one in *Django* with the `layout.html` housing most of the *HTML* code, and we extend it to the other *HTML* pages. To do so we incorporate the use of blocks

Hence the *layout.html* will be:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Flask Tutorial</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```

Now reconfiguring the index.html

```html
{% extends "layout.html" %}

{% block content %}
<h1 class="text-3xl font-bold underline">
    Hello world!
</h1>
{%endblock%}
```



## HTTP Methods (GET/POST) & Forms

We can restrict a method to receive the specified method of request. This is done by adding the methods attibute in the decorator and passing the request method to it. `@app.route("/login", methods=["POST", "GET"])`. The example below explains the two methods

```python
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        return redirect(url_for("user", user=name))
    else:
        return render_template("login.html")
```



## Sessions

Used to store information temporarily on the server.

To use *sessions* we will first have to import `session`

Also we have to define a secret key to decrypt and encrypt session data.

```python
from flask import Flask, redirect, url_for, render_template, request, session


app = Flask(__name__)

#Define seccret key to decrypt and encrypt session data
app.secret_key = "hello"

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        session["user"] = name  ##Placing data into the session
        return redirect(url_for("ses"))
        #return redirect(url_for("user", user=name))
    else:
        return render_template("login.html")
    
@app.route("/ses")
def ses():
    if "user" in session:
        user = session["user"] # REtriving session data
        return f"<h1>{user}</h1>"
    else: 
        return redirect(url_for("login"))

# To Clear the session i.e log out
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
```



To store section data for long periods,

```python
#To store data longer i.e in permanent sessions
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        session.permanent = True #This will set the session data to the duration set
        session["user"] = name
        return redirect(url_for("sesl"))
        #return redirect(url_for("user", user=name))
    else:
        return render_template("login.html")
```



## Message Flashing

To flash a message to the GUI, In this case we are to flash a message to the user once logout is successful

* First we will have to import `flash`.

* On the logout function before the logout we are to add `flash("You have been Logged Out!", "info")`

* ```python
  from flask import Flask, redirect, url_for, render_template, request, session, flash
  
  @app.route("/logout")
  def logout():
      session.pop("user", None)
      flash("You have been Logged Out!", "info")
      return redirect(url_for("login"))
  ```

* To display the message, on the `login` page we will have to check for availability of message

  ```html
  {% with messages = get_flashed_messages() %}
      {%if messages %}
          {%for msg in messages %}
              <p>{{msg}}</p>
          {%endfor%}
      {%endif%}
  {%endwith%}
  ```





## SQLAlchemy Database

 For this serious the database to be used is `SQLAlchemy`

To install the database, run `pip install flask-sqlalchemy`

Then import it on the views page.  `from flask_sqlalchemy import SQLAlchemy`

Then, set up a database object `db = SQLAlchemy(app)`, then we write the config details

The we set-up the model class

```python
from flask_sqlalchemy import SQLAlchemy

#Confirg settings for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This is optional

#Setting up a database object
db = SQLAlchemy(app)

#Setting up a Model class
class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
        
        
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)  
```



To save data into the database

```python
user = users(name, "")
db.session.add(user)
db.session.commit()
```

To retrieve data from the database

```python
found_user = users.query.filter_by(name=user).first()
```

To delete data from the database

```python
found_user = users.query.filter_by(name=user).first()
found_user.delete()
db.session.commit()
```





## Static Files

For static files the default is placing them in the static folder in the root directory and we incorporate them into the template with

 `<link rel="stylesheet" href="{{url_for('static', filename='style.css')}}">`

If the file is in a sub-folder

`<img src="{{url_for('static', filename='images/img.png)}}" >`





## Blueprints

It helps to divide the app into various sub-app files

First set-up the base file as always

```python
#First import Flask
from flask import Flask, redirect, url_for, render_template, request, session, flash


app = Flask(__name__)


if __name__ == '__main__':
    app.run()
```



The create the secondary files i.e `second.py`, with the code as shown below

```python
from flask import Blueprint, render_template

#Setting up the file as a blueprint
second = Blueprint("second", __name__, static_folder="static", template_folder="template")

@second.route("/home")
def home():
    return render_template("home.html")
```

Now in the main file we import the secondary file

```python

#First import Flask
from flask import Flask, redirect, url_for, render_template, request, session, flash
from second import second

app = Flask(__name__)
app.register_bluprint(second, url_prefix="/admin")


if __name__ == '__main__':
    app.run()
```

Note that the `url_prefix` , add the stated name to url before our end path

In a case where the secondary files are in a sub-folder and not in the main directory, on the sub-folder we will have to create a blank python file called `__init__.py`. This will make the folder become a python package. And now to import the second file;

```python
#First import Flask
from flask import Flask, redirect, url_for, render_template, request, session, flash
from admin.second import second

app = Flask(__name__)
app.register_bluprint(second, url_prefix="/admin")


if __name__ == '__main__':
    app.run()
```





## Restful API

Requirements:-

* SQLAlchemy
* Marshmallow - for serialization 

To install 

`pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy`

`marshmallow-sqlalchemy` - This integrates the sqlalchemy to marshmallow.

Below is the basic settup for a restful API

```python
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os #To set out file paths

# Initialiaze the app
app = Flask(__name__)


@app.route('/', methods=["GET"])
def test():
    return jsonify({'msg': "Hello World"})
       
#Run Server      
if __name__ == '__main__':
    app.run(debug=True)  
```

 The above is tested using **POSTMAN** to check if it works.

Below is an example of a restful api server, where the request are made via **POSTMAN**, curtersy of traversy media

```python
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
```

