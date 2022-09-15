from crypt import methods
from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect
from flask_login import (current_user, LoginManager, login_user, logout_user, login_required)
import hashlib
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://well:123456@localhost:3306/BestTrade"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "@123"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db = SQLAlchemy(app)



class Usuario(db.Model):
    __tablename__ = "usuario"
    user_id = db.Column("user_id", db.Integer, primary_key = True)
    user_nome = db.Column("user_nome", db.String(100), nullable=False)
    senha = db.Column("senha", db.String(300), nullable=False)
    email = db.Column("email", db.String(100), nullable=False)
    cpf = db.Column("cpf", db.String(100), nullable=False)
    cep = db.Column("cep", db.String(100), nullable=False)
    rua = db.Column("rua", db.String(256), nullable=False)
    num = db.Column("num", db.String(10), nullable=False)
    bairro = db.Column("bairro", db.String(100), nullable=False)
    cidade = db.Column("cidade", db.String(100), nullable=False)
    comp = db.Column("comp", db.String(256))
    estado = db.Column("estado", db.String(100), nullable=False)

    def __init__(self, user_nome, senha, email, cpf, cep, rua, num, bairro, cidade, comp, estado):
        self.user_nome = user_nome
        self.senha = senha
        self.email = email
        self.cpf = cpf
        self.cep = cep
        self.rua = rua
        self.num = num
        self.bairro = bairro
        self.cidade = cidade
        self.comp = comp
        self.estado = estado

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Categoria(db.Model):
    __tablename__ = "cat"
    cat_id  = db.Column("cat_id", db.Integer, primary_key = True)
    cat_nome = db.Column("cat_nome", db.String(100), nullable=False)

    def __init__(self, cat_nome):
        self.cat_nome = cat_nome

class Produto(db.Model):
    __tablename__ = "produto"
    prod_id = db.Column("prod_id", db.Integer, primary_key = True)
    prod_nome = db.Column("prod_nome", db.String(100), nullable=False)
    descricao = db.Column("info", db.Text, nullable=False)
    qtd = db.Column("qtd", db.Integer, nullable=False)
    valor= db.Column("valor", db.Float, nullable=False)
    cat_id_anun = db.Column("cat_id", db.ForeignKey("cat.cat_id"), nullable=False)
    user_id = db.Column("user_id", db.ForeignKey("usuario.user_id"), nullable=False)
    data_anun = db.Column("data_anun", db.DATETIME)
    prod_stt = db.Column("prod_stt", db.Integer)


    def __init__(self, prod_nome, descricao, qtd, valor, cat_id_anun, user_id, data_anun, prod_stt):
        self.prod_nome = prod_nome
        self.descricao = descricao
        self.qtd = qtd
        self.valor = valor
        self.cat_id_anun = cat_id_anun
        self.user_id = user_id
        self.data_anun = data_anun
        self.prod_stt = prod_stt


class Favoritos(db.Model):
    __tablename__ = "favoritos"
    fav_id = db.Column("fav_id", db.Integer, primary_key = True)
    fav_anun = db.Column("fav_anun", db.ForeignKey("produto.prod_id"), nullable=False)
    fav_user = db.Column("fav_user", db.ForeignKey("usuario.user_id"), nullable=False)

    def __init__(self, fav_anun, fav_user):
        self.fav_anun = fav_anun
        self.fav_user = fav_user

class Transacao(db.Model):
    __tablename__ = "trades"
    trade_id  = db.Column("trade_id", db.Integer, primary_key = True)
    anun_id = db.Column("anun_id", db.ForeignKey("produto.prod_id"), nullable=False)
    vendedor_id = db.Column("v_id", db.ForeignKey("produto.user_id"), nullable=False)
    comprador_id = db.Column("c_id", db.ForeignKey("usuario.user_id"), nullable=False)
    data_trade = db.Column("d_trade", db.DateTime)

    def __init__(self, anun_id, vendedor_id, comprador_id, data_trade):
        self.anun_id = anun_id
        self.vendedor_id = vendedor_id
        self.comprador_id = comprador_id
        self.data_trade = data_trade

class Mensagens(db.Model):
    __tablename__ = "mensagens"
    msg_id = db.Column("msg_id", db.Integer, primary_key = True)
    msg = db.Column("msg", db.Text, nullable=False)
    anun_id = db.Column("anun_id", db.ForeignKey("produto.prod_id"), nullable=True)
    nome = db.Column("nome", db.String(100), nullable=False)
    data_msg = db.Column("data_msg", db.DateTime)
    
    def __init__(self, msg, anun_id, nome, data_msg):
        self.msg = msg
        self.anun_id = anun_id
        self.nome = nome
        self.data_msg = data_msg
        

class Respostas(db.Model):
    __tablename__ = "respostas"
    resp_id = db.Column("resp_id", db.Integer, primary_key = True)
    resp = db.Column("resp", db.Text, nullable = False)
    resp_to = db.Column("resp_to", db.ForeignKey("mensagens.msg_id"), nullable=False)
    anun_id = db.Column("anun_id", db.ForeignKey("produto.prod_id"), nullable=False)
    nome = db.Column("nome", db.String(100), nullable=False)
    data_resp = db.Column("data_resp", db.DateTime)

    def __init__(self, resp, resp_to, anun_id, nome, data_resp):
        self.resp = resp
        self.resp_to= resp_to
        self.anun_id = anun_id
        self.nome = nome
        self.data_resp = data_resp

@app.errorhandler(404)
def pag_erro(error):
    return render_template("ops.html")

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(user_id)
 
@app.route("/")
def index():
    
    if current_user.is_authenticated:       
        return render_template("index.html", titulo="Home", name = current_user.user_nome)
    else:
        return render_template("index.html", titulo="Home", usuario = Usuario.query.all())
   
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = hashlib.sha512(str(request.form.get("senha")).encode("utf-8")).hexdigest()
        user = Usuario.query.filter_by(email=email, senha=senha).first()

        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            return redirect(url_for("index"))
    return redirect(url_for("index"))
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
    

@app.route("/usuario/novo")
def cadastro():
    return render_template("cadastro.html", titulo="Cadastro de Usuario")

@app.route("/usuario/detalhes")
@login_required
def list_users():
    return render_template("list_users.html", usuarios = Usuario.query.all(), titulo="Lista de usuarios cadastrados")

@app.route("/usuario/detalhes/editar/<int:id>", methods=["GET","POST"])
@login_required
def user_edit(id):
    usuario = Usuario.query.get(id)
    if request.method == "POST":
        usuario.user_nome = request.form.get("user_nome")
        usuario.email = request.form.get("email")
        usuario.cpf = request.form.get("cpf")
        usuario.cep = request.form.get("cep")
        usuario.rua = request.form.get("rua")
        usuario.num = request.form.get("num")
        usuario.bairro = request.form.get("bairro")
        usuario.cidade = request.form.get("cidade")
        usuario.comp = request.form.get("comp")
        usuario.estado = request.form.get("estado")
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for( "user_edit", id = usuario.user_id))

    return render_template("user_edit.html", usuario = usuario , titulo="Edição de Usuario")


@app.route("/usuario/detalhes/remover/<int:id>")
@login_required
def user_del(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('usuario'))   

@app.route("/anuncio/detalhes/<int:id>")
@login_required
def anun_info(id):
    favs = Favoritos.query.all()
    anun = Produto.query.get(id)
    info = anun
    conta = 0
    for fav in favs:
        if (fav.fav_anun == info.prod_id) and (fav.fav_user == current_user.user_id):
            conta = conta +1
    if conta == 0:
        stt = 1
    else:
        stt = 0
    return render_template("anuncios_info.html", info = anun, stt = stt, favs = Favoritos.query.all(), resps = Respostas.query.all(), msgs = Mensagens.query.all(), titulo = "detalhes do produto")

@app.route("/anuncio")
def anuncios():
    return render_template("anuncios.html", produtos = Produto.query.all(), titulo = "Lista de anuncios")

@app.route("/anuncio/novo")
@login_required
def novo_anuncio():
    return render_template("novo_anun.html", categorias = Categoria.query.all(), titulo = "Criar novo anuncio")

@app.route("/anuncios/meus")
@login_required
def meus_anuncios():
    return render_template("meus_anun.html", cats = Categoria.query.all(), anuns = Produto.query.all(), titulo = "Meus Anuncios")   

@app.route("/anuncios/meus/del/<int:id>")
@login_required
def anun_del(id):
    anun = Produto.query.get(id)
    anun.prod_stt = 1
    db.session.commit()
    return redirect(url_for('meus_anuncios'))


@app.route("/anuncios/meus/edit")
@login_required
def anun_edit():
    return

@app.route("/usuario/favoritos/lista")
@login_required
def lista_favoritos():
    return render_template("favoritos.html")  

@app.route("/hist/compras")
@login_required 
def historico_compras():
    return render_template("hist_compras.html") 

@app.route("/hist/vendas")
@login_required
def historico_vendas():
    return render_template("hist_vendas.html")

@app.route("/usuario/novo/criar", methods=['POST'])
def cad_user():
    hash = hashlib.sha512(str(request.form.get("senha")).encode("utf-8")).hexdigest()
    usuario = Usuario(request.form.get("user_nome"), hash, request.form.get("email"), request.form.get("cpf"), request.form.get("cep"), request.form.get("rua"), request.form.get("num"), request.form.get("bairro"), request.form.get("cidade"), request.form.get("comp"), request.form.get("estado"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for("cadastro"))

@app.route("/anuncio/novo/criar", methods=["POST"])
@login_required
def cad_novo_anun():
    user_id = current_user.user_id
    dat = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    novo_anun = Produto(request.form.get("prod_nome"), request.form.get("descricao"), request.form.get("qtd"), request.form.get("valor"), request.form.get("cat_id_anun"), user_id, dat)
    db.session.add(novo_anun)
    db.session.commit()
    return redirect(url_for("novo_anuncio"))

@app.route("/anuncio/msg/criar", methods=["POST"])
@login_required
def msg_novo():
    user_nome = current_user.user_nome
    dat = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    nova_msg = Mensagens(request.form.get("msg"), request.form.get("anun_id"), user_nome, dat)
    db.session.add(nova_msg)
    db.session.commit()
    return redirect(url_for("anun_info",id = nova_msg.anun_id ))

@app.route("/anuncio/msg/resp", methods=["POST"])
@login_required
def msg_resp():
    user_nome = current_user.user_nome
    dat = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    resp_msg = request.form.get("anun_id")
    nova_msg = Respostas(request.form.get("resp"), request.form.get("resp_to"), request.form.get("anun_id"), user_nome, dat )
    db.session.add(nova_msg)
    db.session.commit()
    return redirect(url_for("anun_info",id = resp_msg))

@app.route("/anuncio/favoritos/novo", methods=["POST"])
@login_required
def novo_fav():
    user_id = current_user.user_id
    fav_id = request.form.get("fav")
    novo_fav = Favoritos(fav_id, user_id)
    print(novo_fav)
    db.session.add(novo_fav)
    db.session.commit()
    return redirect(url_for("anun_info",id = fav_id))

        

@app.route("/sobre")
def sobre():
    return render_template("sobre.html") 

@app.route("/anuncio/compra", methods=["POST"])
@login_required
def conf_compra():
    qtd = int(request.form.get("qtd_compra"))
    prod = request.form.get("prod_id")
    aux = Produto.query.get(prod)
    aux2 = aux.valor
    total = aux2 * qtd

    return render_template("comprar.html", info = aux, qtd = qtd, total = total, titulo = "Confirmação de Compra")

@app.route("/anuncio/compra/confirma", methods=["POST"])
@login_required
def comprado():
    comprador = current_user.user_id
    dat = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    v_id = request.form.get("v_id")
    print(v_id)
    trade = Transacao(request.form.get("prod_id"), request.form.get("v_id"), comprador, dat)
    db.session.add(trade)
    db.session.commit()
    qtd = int(request.form.get("qtd"))
    prod_id = request.form.get("prod_id")
    prod = Produto.query.get(prod_id)
    prod.qtd = prod.qtd - qtd
    db.session.commit()
    aux = Produto.query.get(prod_id)
    total = aux.valor * qtd
    return render_template("comprado.html", info = aux, qtd = qtd, total = total, titulo = "Compra realizada")

@app.route("/favorito")
@login_required
def fav():
    return


@app.route("/busca")
def busca():
    return

@app.route("/categoria/novo")
@login_required
def cat_novo():
    return render_template("cat_novo.html", cats = Categoria.query.all(), titulo = "Nova Categoria")

@app.route("/categoria/criar", methods=["POST"])
@login_required
def cat_criar():
    cat = Categoria(request.form.get("cat_nome"))
    db.session.add(cat)
    db.session.commit()
    return redirect(url_for("cat_novo"))

@app.route("/categoria/del/<int:id>")
@login_required
def cat_del(id):
    cat = Categoria.query.get(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('cat_novo'))
    



if __name__ == 'BestTrade':
    db.create_all()

