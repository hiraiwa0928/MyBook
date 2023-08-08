from os import urandom
from flask import Flask
from flask import request, render_template, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from requests import get
from json import loads
from requests import get

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

@app.route("/")
@login_required
def top():
    return render_template("index.html")

def searchBook(searchTerm):
    bookInfo = []

    # ISBN検索
    url_isbn = "https://www.googleapis.com/books/v1/volumes?q=isbn:" + searchTerm
    getBookInfo = loads(get(url_isbn).text)

    if "items" in getBookInfo:
        for ele in getBookInfo["items"]:
            bookInfo.append(ele)

    # タイトル検索
    url_title = "https://www.googleapis.com/books/v1/volumes?q=" + searchTerm
    getBookInfo = loads(get(url_title).text)
    if "items" in getBookInfo:
        for ele in getBookInfo["items"]:
            bookInfo.append(ele)

    return bookInfo

@app.route("/search", methods=['POST'])
@login_required
def search():
    searchTerm = request.form.get("searchTerm")
    bookInfo = searchBook(str(request.form.get("searchTerm")))
    if len(bookInfo) == 0:
        flash("検索した内容の本が見つかりませんでした")
    return render_template("search.html", bookInfo=bookInfo)