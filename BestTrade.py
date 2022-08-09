from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from flask import redirect



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://well:123456@localhost:3306/BestTrade"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    user_id = db.Column("user_id", db.Integer, primary_key = True)
    user_nome = db.Column("user_nome", db.String(100), nullable=False)
    cpf = db.Column("cpf", db.String(100), nullable=False)
    email = db.Column("email", db.String(100), nullable=False)
    senha = db.Column("senha", db.String(100), nullable=False)
    cep = db.Column("cep", db.String(100), nullable=False)
    rua = db.Column("rua", db.String(256), nullable=False)
    num = db.Column("num", db.String(10), nullable=False)
    bairro = db.Column("bairro", db.String(100), nullable=False)
    comp = db.Column("comp", db.String(256))
    estado = db.Column("estado", db.String(100), nullable=False)

def __init__(self, user_nome, cpf, email, senha, cep, rua, num, bairro, comp, estado):
    self.user_nome = user_nome
    self.cpf = cpf
    self.email = email
    self.senha = senha
    self.cep = cep
    self.rua = rua
    self.num = num
    self.bairro = bairro
    self.comp = comp
    self.estado = estado


class Produto(db.Model):
    __tablename__ = "produto"
    prod_id = db.Column("prod_id", db.Integer, primary_key = True)
    prod_nome = db.Column("prod_nome", db.String(100), nullable=False)
    descricao = db.Column("info", db.Text, nullable=False)
    qtd = db.Column("qtd", db.Integer, nullable=False)
    valor= db.Column("valor", db.Float, nullable=False)

def __init__(self, prod_nome, descricao, qtd, valor):
    self.prod_nome = prod_nome
    self.descricao = descricao
    self.qdt = qtd
    self.valor = valor
    
class Anuncio(db.Model):
    __tablename__ = "anuncio"
    anuncio_id  = db.Column("anun_id", db.Integer, primary_key = True)
    produto_id = db.Column("prod_id", db.ForeignKey("produto.prod_id"), nullable=False)
    vendedor_id = db.Column("info", db.ForeignKey("usuario.user_id"), nullable=False)
    data_anun = db.Column("d_anun", db.DateTime)

def __init__(self, produto_id, vendedor_id, data_anun):
    self.produto_id = produto_id
    self.vendedor_id = vendedor_id
    self.data_anun = data_anun

class Transacao(db.Model):
    __tablename__ = "trades"
    trade_id  = db.Column("trade_id", db.Integer, primary_key = True)
    anun_id = db.Column("anun_id", db.ForeignKey("anuncio.anun_id"), nullable=False)
    vendedor_id_anun = db.Column("v_id", db.ForeignKey("usuario.user_id"), nullable=False)
    data_trade = db.Column("d_trade", db.DateTime)

def __init__(self, anun_id, vendedor_id_anun, data_trade):
    self.anun_id = anun_id
    self.vendedor_id_anun = vendedor_id_anun
    self.data_trade = data_trade

class Categoria(db.Model):
    __tablename__ = "cat"
    cat_id  = db.Column("cat_id", db.Integer, primary_key = True)
    produto_id_c = db.Column("prod_id", db.ForeignKey("produto.prod_id"), nullable=False)
    nome_cat = db.Column("cat_nome", db.String(100), nullable=False)

def __init__(self,produto_id_c, nome_cat):
    self.produto_id_c = produto_id_c
    self.nome_cat = nome_cat

 
@app.route("/")
def index():
    return render_template("index.html")
   
    
@app.route("/signup")
def cadastro():
    return render_template("cadastro.html")

@app.route("/anuncio")
def produtos():
    return render_template("anuncios.html")

@app.route("/cad/anuncio")
def novo_produto():
    return render_template("cad_produto.html")

@app.route("/favoritos/lista")
def lista_favoritos():
    return render_template("favoritos.html")  

@app.route("/hist/compras")
def historico_compras():
    return render_template("hist_compras.html") 

@app.route("/hist/vendas")
def historico_vendas():
    return render_template("hist_vendas.html")

@app.route("/anuncios/meus")
def meus_anuncios():
    return render_template("meus_anuncios.html")

@app.route("/signup/cad", methods=['POST'])
def cad_user():
    usuario = Usuario(request.form.get("user_nome"), request.form.get("cpf"), request.form.get("email"), request.form.get("senha"), request.form.get("cep"), request.form.get("rua"), request.form.get("num"), request.form.get("bairro"), request.form.get("comp"), request.form.get("estado"))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for("cadastro"))

@app.route("/anuncios/meus/del")
def remover_anuncio():
    return

@app.route("/perguntas")
def perguntas():
    return

@app.route("/compra")
def compra():
    return

@app.route("/favorito")
def fav():
    return


@app.route("/login")
def login():
    return

@app.route("/busca")
def busca():
    return

@app.route("/categoria")
def categorias():
    return


if __name__ == 'BestTrade':
        db.create_all()