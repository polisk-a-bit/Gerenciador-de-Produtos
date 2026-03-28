from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = ("sqlite:///sistema_gerenciamento.db")
app.config["SECRET_KEY"] = ("29a161dd7dc730778cdff846adf919b0")
app.config["UPLOAD_FOLDER"] = ("static/uploads")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from SistemaGerenciamentoProdutos import routes
