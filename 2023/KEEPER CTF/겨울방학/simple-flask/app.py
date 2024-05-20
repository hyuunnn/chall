from flask import Flask, request, render_template, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_migrate import Migrate

import uuid

DB_NAME = "test.db"

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.password}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("login"))

@app.route("/")
def main():
    if current_user.is_authenticated:
        return f"{current_user.username}!"
    else:
        return "test"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main"))
        
        return render_template_string(f"username: {username} password: {password}")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if User.query.filter_by(username=username).first():
            return render_template("register.html", error="Username already exists")
        
        user = User(username, generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main"))

if __name__ == "__main__":
    app.run()
