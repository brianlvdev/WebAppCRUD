from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import banco

app = Flask(__name__)
app.secret_key = "chave-secreta-muito-segura-troque-isso" 
banco.criar_banco()



def login_obrigatorio(f):
    @wraps(f)
    def funcao_decorada(*args, **kwargs):
        if "usuario_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return funcao_decorada


@app.route("/login", methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha = request.form.get("senha", "")

        usuario = banco.buscar_usuario(username)
        if usuario and check_password_hash(usuario["senha"], senha):
            session["usuario_id"] = usuario["id"]
            session["username"] = usuario["username"]
            return redirect(url_for("index"))
        else:
            erro = "Usuário ou senha inválidos."

    return render_template("login.html", erro=erro)


@app.route("/registrar", methods=["GET", "POST"])
def registrar():
    erro = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        senha = request.form.get("senha", "")

        if not username or not senha:
            erro = "Preencha usuário e senha."
        elif banco.buscar_usuario(username):
            erro = "Este nome de usuário já existe."
        else:
            senha_hash = generate_password_hash(senha)
            banco.criar_usuario(username, senha_hash)
            return redirect(url_for("login"))

    return render_template("registrar.html", erro=erro)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def validar(nome, cargo):
    nome = nome.strip()
    cargo = cargo.strip()
    
    if not nome:
        return None, "O Nome é obrigatório."
    if not cargo:
        return None, "O Cargo é obrigatório."
    return cargo, None

@app.route("/")
@login_obrigatorio
def index():
    termo = request.args.get("q", "").strip()
    if termo:
        pessoas = banco.busca_por_nome(termo)
        
    else:
        pessoas = banco.listar()
    return render_template("index.html", pessoas=pessoas, termo=termo)


@app.route("/cadastrar", methods=["GET", "POST"])
@login_obrigatorio
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
@login_obrigatorio
def editar(pid):
    pessoa = banco.buscar_por_id(pid)
    if pessoa is None:
        return redirect(url_for("index"))
    
    erro = None
    if request.method == "POST":
        novo_nome = request.form.get("nome", "").strip()
        novo_cargo = request.form.get("cargo", "").strip()

        if not novo_nome and not novo_cargo:
            erro = "Preencha pelo menos um campo para atualizar."
        else:
            nome_final = novo_nome or pessoa["nome"]
            cargo_final = novo_cargo or pessoa["cargo"]
            banco.atualizar(pid, nome_final, cargo_final)
            return redirect(url_for("index"))
            
    return render_template("editar.html", pessoa=pessoa, erro=erro)

@app.route("/excluir<int:pid>", methods=["POST"])
@login_obrigatorio
def excluir(pid):
    banco.excluir(pid)
    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)
