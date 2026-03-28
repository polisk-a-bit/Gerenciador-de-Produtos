from SistemaGerenciamentoProdutos.models import Produto, Usuario
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    FileField,
    DecimalField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    ValidationError,
    Optional,
    InputRequired,
    NumberRange,
)


class Form_LoginUsuario(FlaskForm):
    email = StringField("E-mail:", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha:", validators=[DataRequired()])
    botao_confirm = SubmitField("Fazer Login")


class Form_CriarConta(FlaskForm):
    username = StringField(
        "Nome de usuário:", validators=[DataRequired(), Length(6, 20)]
    )
    email = StringField("E-mail:", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha:", validators=[DataRequired(), Length(6, 20)])
    senha_confirm = PasswordField(
        "Confirme sua senha:",
        validators=[DataRequired(), EqualTo("senha"), Length(6, 20)],
    )
    botao_confirm = SubmitField("Criar Conta")



class Form_AttConta(FlaskForm):
    username = StringField("Nome de usuário:", validators=[Optional(), Length(6, 20)])
    senha = PasswordField("Senha:", validators=[Optional(), Length(6, 20)])
    senha_confirm = PasswordField(
        "Confirme sua senha:", validators=[Optional(), EqualTo("senha")]
    )
    foto = FileField("Foto de Perfil", validators=[Optional()])
    botao_confirm = SubmitField("Atualizar Conta")



class Form_Produto(FlaskForm):
    nome_prod = StringField("Nome do produto:", validators=[DataRequired()])
    preco = DecimalField(
        "Preço do produto:",
        validators=[InputRequired(), NumberRange(min=0.01, max=99999.99)],
        places=2,
        rounding=None,
    )
    quantidade_est = IntegerField(
        "Quantidade em estoque:", validators=[InputRequired(), NumberRange(min=0)]
    )
    botao_confirm = SubmitField("Adicionar Produto")



class Form_AttProduto(FlaskForm):
    nome_prod = StringField("Nome do produto:", validators=[Optional()])
    preco = DecimalField(
        "Preço do produto:",
        validators=[Optional(), NumberRange(min=0.01, max=99999.99)],
        places=2,
        rounding=None,
    )
    quantidade_est = IntegerField(
        "Quantidade em estoque:", validators=[Optional(), NumberRange(min=0)]
    )
    botao_confirm = SubmitField("Atualizar Produto")



class Form_Busca(FlaskForm):
    busca=IntegerField('Buscar ID...', validators=[Optional(), NumberRange(min=1)])
    botao_confirm = SubmitField("Buscar")


class Form_Busca_User(FlaskForm):
    busca_user=IntegerField('Buscar ID...', validators=[Optional(), NumberRange(min=1)])
    botao_confirm_user = SubmitField("Buscar")


class Form_Busca_ADM(FlaskForm):
    busca_adm=IntegerField('Buscar ID...', validators=[Optional(), NumberRange(min=1)])
    botao_confirm_adm = SubmitField("Buscar")
