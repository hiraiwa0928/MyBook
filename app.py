from os import urandom
from flask import Flask
from flask import request, render_template, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from requests import get
from json import *

app = Flask(__name__, static_folder="./static/")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mybook.db"
app.config["SECRET_KEY"] = urandom(24)
db = SQLAlchemy(app)
Bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	password = db.Column(db.String(30), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route("/", methods = ["GET", "POST"])
@login_required
def top():
    return render_template("index.html")

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User(username=username, password=generate_password_hash(password, method="sha256"))
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user != None and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            return redirect("/login")
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        searchTerm = request.form.get("searchTerm")
        print(searchTerm)
        return render_template("search.html", searchTerm=searchTerm)
    else:
        pass