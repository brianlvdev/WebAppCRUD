from flask import Flask, render_template, request, redirect, url_for
import banco

app = Flask(__name__)
banco.criar_banco()
def validar(nome, cargo):
    nome = nome.strip()
    cargo = cargo.strip()
    
    if not nome:
        return None, "O Nome é obrigatório."
    if not cargo:
        return None, "O Cargo é obrigatório."
    return cargo, None

@app.route("/")
def index():
    termo = request.args.get("q", "").strip()
    if termo:
        pessoas = banco.busca_por_nome(termo)
        
    else:
        pessoas = banco.listar()
    return render_template("index.html", pessoas=pessoas, termo=termo)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    erro = None
    
    if request.method == "POST":
        nome = request.form["nome"].strip()
        cargo, erro = validar(nome, request.form["cargo"])
        if erro is None:
            banco.cadastrar(nome, cargo)
            return redirect(url_for("index"))
    return render_template("cadastrar.html", erro=erro)


@app.route("/editar/<int:pid>", methods=["GET","POST"])
def editar(pid):
    pessoa = banco.buscar_por_id(pid)
    if pessoa is None:
        return redirect(url_for("index"))
    erro = None
    if request.method == "POST":
        nome = request.form["nome"].strip()
        cargo, erro = validar(nome, request.form["cargo"])
        if erro is None:
            banco.atualizar(pid, nome, cargo)
            return redirect(url_for("index"))        
    return render_template("editar.html", pessoa=pessoa, erro=erro)

@app.route("/excluir<int:pid>", methods=["POST"])
def excluir(pid):
    banco.excluir(pid)
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)
