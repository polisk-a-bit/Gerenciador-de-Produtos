from flask import render_template, url_for, redirect, flash, request, jsonify
from SistemaGerenciamentoProdutos import app, db, bcrypt
from SistemaGerenciamentoProdutos.models import Usuario, Produto
from SistemaGerenciamentoProdutos.forms import *
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.utils import secure_filename
import os

@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = Form_LoginUsuario()

    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
    
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("gerenciador"))
        else:
            flash("Usuário ou senha errados!")

    return render_template("homepage.html", form=form_login)


@app.route("/criar_conta", methods=["GET", "POST"])
def criar_conta():
    form_criarConta = Form_CriarConta()
    if form_criarConta.validate_on_submit():
        usuario_ver=Usuario.query.filter_by(username=form_criarConta.username.data).first()
        email_ver=Usuario.query.filter_by(email=form_criarConta.email.data).first()

        senha_cript = bcrypt.generate_password_hash(form_criarConta.senha.data)

        if usuario_ver:
            flash('Usuário Inválido!')
        if email_ver:
            flash('Email Inválido!')

        if not usuario_ver and not email_ver:
            usuario = Usuario(
                username=form_criarConta.username.data,
                email=form_criarConta.email.data,
                senha=senha_cript,
                ADMIN=False,
                foto=None,
            )

            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for("homepage"))

    return render_template("criar_conta.html", form=form_criarConta)


@app.route("/gerenciador", methods=["GET","POST"])
@login_required
def gerenciador():
    usuario=Usuario.query.get(current_user.id)
    produtos=Produto.query.order_by(Produto.id).all()
    atualizar=request.form.get('Atualizar')


    form_busca=Form_Busca()
    if form_busca.validate_on_submit():
        if form_busca.busca.data:
            produto = Produto.query.filter_by(id=form_busca.busca.data).first()
            produtos = [produto]
        else:
            flash('Informe um ID para busca!')
            pass
        
    if atualizar==('Atualizar'):
        produtos=Produto.query.order_by(Produto.id).all()

    return render_template("gerenciador.html", produtos=produtos, form=form_busca, usuario=usuario)


@app.route('/adicionar_produto', methods=["GET", "POST"])
@login_required
def add_prod():
    usuario=Usuario.query.get(current_user.id)
    if usuario.ADMIN == False:
        return redirect(url_for('gerenciador'))

    form_prod = Form_Produto()
    if form_prod.validate_on_submit():
        add=False

        produto_ver=Produto.query.filter_by(nome_produto=form_prod.nome_prod.data).first()
        if produto_ver:
            flash('Produto já cadastrado!')
        else:
            produto=Produto(
                nome_produto=form_prod.nome_prod.data,
                preco=form_prod.preco.data,
                quantidade_estoque=form_prod.quantidade_est.data
            )
            db.session.add(produto)
            add=True

        if add==True:
            db.session.commit()
            flash("Produto adicionado com sucesso!")
            return redirect(url_for("gerenciador"))
    
    return render_template("add_prod.html", form=form_prod)


@app.route('/atualizar_produto/<id_produto>', methods=["GET", "POST"])
@login_required
def att_prod(id_produto):
    usuario=Usuario.query.get(current_user.id)
    if usuario.ADMIN == False:
        return redirect(url_for('gerenciador'))
    
    att=False
    form_attProduto=Form_AttProduto()

    produto=Produto.query.get(id_produto)
    
    if form_attProduto.validate_on_submit():
        deletar=request.form.get('deletar')
        
        if form_attProduto.nome_prod.data:
            produto_ver=Produto.query.filter_by(nome_produto=form_attProduto.nome_prod.data).first()
            if produto_ver:
                flash('Produto já cadastrado!')
            else:
                produto.nome_produto=form_attProduto.nome_prod.data
                att=True
            
                if form_attProduto.preco.data:
                    produto.preco=form_attProduto.preco.data
                    att=True

                if form_attProduto.quantidade_est.data:
                    produto.quantidade_estoque=form_attProduto.quantidade_est.data
                    att=True
        
        if att==True:
            db.session.commit()
            flash("Produto atualizado com sucesso!")
    
        if deletar == ('delete'):
            db.session.delete(produto)
            db.session.commit()

            flash("Produto Excluído com Sucesso!")
            return redirect(url_for('gerenciador'))

        
    return render_template("att_prod.html", form=form_attProduto)


@app.route('/perfil/<username_usuario>', methods=["GET","POST"])
@login_required
def perfil(username_usuario):
    usuario=Usuario.query.get(current_user.id)
    excluir=request.form.get("excluir")
    form_attConta=Form_AttConta()

    if usuario.username!=username_usuario:
        return redirect(url_for('perfil', username_usuario=usuario.username))
    
    if form_attConta.validate_on_submit():
        changed=False
        if form_attConta.username.data:
            usuario_ver=Usuario.query.filter_by(username=form_attConta.username.data).first()

            if usuario_ver:
                flash('Usuário já cadastrado!')
            else:
                usuario.username=form_attConta.username.data
                changed=True 
        
        if form_attConta.senha.data and not form_attConta.senha_confirm.data:
            flash('Preencha o campo "Confirme sua senha"!')
        elif form_attConta.senha.data and form_attConta.senha_confirm.data:
            senha_cript=bcrypt.generate_password_hash(form_attConta.senha.data)
            usuario.senha=senha_cript
            changed=True
            flash("Senha atualizada com sucesso!")
 
        
        if form_attConta.foto.data and hasattr(form_attConta.foto.data, 'filename'): #hasattr(form_attConta.foto.data, 'filename') verifica se é um arquivo novo
            
            if current_user.foto != None:
                caminho_antigo=os.path.join(
                    os.path.abspath(os.path.dirname(__file__)),
                    app.config["UPLOAD_FOLDER"],
                    usuario.foto,
                )
                if os.path.exists(caminho_antigo):
                    os.remove(caminho_antigo)

            arquivo=form_attConta.foto.data
            nome_seguro=secure_filename(arquivo.filename)
            caminho = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                app.config["UPLOAD_FOLDER"],
                nome_seguro,
            )
            arquivo.save(caminho)
            usuario.foto=nome_seguro
            changed=True
        
        if changed==True:
            db.session.commit()
            flash('Conta atualizada com sucesso!')
    
        if excluir == ("excluir"):
            db.session.delete(usuario)
            db.session.commit()
            flash('Usuário excluído com sucesso!')
            return redirect(url_for('homepage'))

    return render_template('perfil.html', usuario=usuario, form=form_attConta)

@app.route('/gerenciar_usuarios/<username_usuario>', methods=["GET", "POST"])
@login_required
def gerenciador_user(username_usuario):
    usuario=Usuario.query.get(current_user.id)
    if usuario.ADMIN == False:
        return redirect(url_for('gerenciador'))
    
    form_busca_usuario=Form_Busca_User()
    form_busca_ADM=Form_Busca_ADM()
    
    usuarios_padrao=Usuario.query.filter_by(ADMIN=False).all()
    usuarios_ADM=Usuario.query.filter_by(ADMIN=True).filter(Usuario.email != 'adm@gmail.com').all()


    atualizar_user=request.form.get('atualizar_user')
    if form_busca_usuario.validate_on_submit():
        if form_busca_usuario.busca_user.data:
            user=Usuario.query.filter_by(id=form_busca_usuario.busca_user.data).filter_by(ADMIN=False).first()
            usuarios_padrao=[user]
            
    if atualizar_user == ('user'):
        usuarios_padrao=Usuario.query.filter_by(ADMIN=False).all()


    atualizar_ADM=request.form.get('atualizar_ADM')
    if form_busca_ADM.validate_on_submit():
        if form_busca_ADM.busca_adm.data:
            adm=Usuario.query.filter_by(id=form_busca_ADM.busca_adm.data).filter_by(ADMIN=True).filter(Usuario.email != 'adm@gmail.com').first()
            usuarios_ADM=[adm]
        
    if atualizar_ADM == ('ADM'):
        usuarios_ADM=Usuario.query.filter_by(ADMIN=True).filter(Usuario.email != 'adm@gmail.com').all()

    return render_template('gerenciar_usuarios.html', usuarios_padrao=usuarios_padrao, usuarios_ADM=usuarios_ADM,
        form_busca_usuario=form_busca_usuario, form_busca_ADM=form_busca_ADM, usuario=usuario
    )


@app.route('/excluir_user/<id_user>', methods=['GET'])
def excluir_user(id_user):
    user=Usuario.query.get(id_user)

    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('gerenciador_user', username_usuario=current_user.username))


@app.route('/conceder_privilegios/<id_user>', methods=['GET'])
def conceder_privilegios(id_user):
    user=Usuario.query.get(id_user)

    user.ADMIN=True
    db.session.commit()
    return redirect(url_for('gerenciador_user', username_usuario=current_user.username))


@app.route('/remover_privilegios/<id_user>', methods=['GET'])
def remover_privilegios(id_user):
    user=Usuario.query.get(id_user)

    user.ADMIN=False
    db.session.commit()
    return redirect(url_for('gerenciador_user', username_usuario=current_user.username))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))