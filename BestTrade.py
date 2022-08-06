from flask import Flask, make_response
from markupsafe import escape
from flask import render_template
from flask import request


app = Flask(__name__)

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

@app.route("/anuncios/meus/del")
def remover_anuncio():
    return()

@app.route("/perguntas")
def perguntas():
    return()  

@app.route("/compra")
def compra():
    return()

@app.route("/favorito")
def fav():
    return()


@app.route("/login")
def login():
    return()

@app.route("/busca")
def busca():
    return()

@app.route("/categoria")
def busca():
    return()