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













`