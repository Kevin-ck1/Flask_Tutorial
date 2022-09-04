from flask import Blueprint, render_template

#Setting up the file as a blueprint
second = Blueprint("second", __name__, static_folder="static", template_folder="template")

@second.route("/home")
def home():
    render_template("home.html")