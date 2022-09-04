
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import sqlalchemy


app = Flask(__name__)

#Define seccret key to decrypt and encrypt session data
app.secret_key = "hello"

#Confirg settings for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # This is optional

#To store data longer i.e in permanent sessions
from datetime import timedelta
app.permanent_session_lifetime = timedelta(minutes=5)

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






#Rendering a template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        name = request.form["nm"]
        session.permanent = True #This will set the session data to the duration set
        session["user"] = name
        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            user = users(name, "")
            db.session.add(user)
            db.session.commit()

        return redirect(url_for("user"))
        #return redirect(url_for("sesl"))
        #return redirect(url_for("user", user=name))
    else:
        return render_template("login.html")
'''
@app.route("/<user>")
def user(user):
    user = session["user"]
    return f"<h1>{user}</h1>"
'''

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None #Sets the value email to none.
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not Logged in!")
        return redirect(url_for("login"))

@app.route("/sesl")
def sesl():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else: 
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("You have been Logged Out!", "info")
    return redirect(url_for("login"))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)