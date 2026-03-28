from SistemaGerenciamentoProdutos import db, login_manager
from datetime import date
from flask_login import UserMixin


@login_manager.user_loader
def load_user(id_usuario):
    return Usuario.query.get(id_usuario)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_produto = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade_estoque = db.Column(db.Integer, nullable=False)
    data_cadastro = db.Column(db.DateTime, nullable=False, default=date.today())


class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(60), nullable=False)
    ADMIN = db.Column(db.Boolean, default=False)
    foto = db.Column(db.String(100), nullable=True)
