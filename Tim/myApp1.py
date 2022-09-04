## This is for lesson 1

#First import Flask
from flask import Flask, redirect, url_for

#Second Create an Instance of Flask Web App
app = Flask(__name__)

#Creating a page
@app.route("/")
def home():
    return "Hello! This is the main page <h1>HELLO</h1>"

#Passing a variable to the function from the web browser
@app.route("/<name>")
def user(name):
    return f"Hello {name}"

# To redirect someone to a different page
@app.route("/admin")
def admin():
    return redirect(url_for("home"))#Inside the *url_for* we input the name of the function 

# To redirect someone to the user function
@app.route("/adminUser")
def adminUser():
    return redirect(url_for("user", name="Admin!"))


if __name__ == '__main__':
    app.run(debug=True)