#Lesson 2

#First import Flask
from flask import Flask, redirect, url_for, render_template

#Second Create an Instance of Flask Web App
app = Flask(__name__)

#Rendering a template
@app.route("/")
def home():
    return render_template("index.html")

#To pass a variable to the template file
@app.route("/<name>")
def user(name):
    return render_template("index.html", content=name, r=2)

#To pass a list variable to the template file
@app.route("/list")
def list():
    return render_template("index.html", content=["Joe", "Peter", "Mary"], r=2)



if __name__ == '__main__':
    app.run(debug=True)