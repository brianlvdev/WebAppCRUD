import sqlite3
from pathlib import Path

NOME_BANCO = Path(__file__).resolve().parent / "cadastro.db"

def conectar():
    db = sqlite3.connect(NOME_BANCO)
    db.row_factory = sqlite3.Row
    return db

def criar_banco():
    with conectar() as db:
       return db.execute("CREATE TABLE IF NOT EXISTS pessoas(pid INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, cargo TEXT NOT NULL);")

def listar():
    with conectar() as db:
        return db.execute("SELECT pid, nome, cargo FROM pessoas ORDER BY pid").fetchall()
        
def buscar_por_id(pid):
    with conectar() as db:
        return db.execute("SELECT pid, nome, cargo FROM pessoas WHERE pid = ? ORDER BY pid", (pid,)).fetchall()
    
def cadastrar(nome, cargo):
    with conectar() as db:
        db.execute("INSERT INTO pessoas (nome, cargo) VALUES (?, ?)", (nome, cargo))
        
def atualizar(nome, cargo, pid):
    with conectar() as db:
        db.execute(
            "UPDATE pessoas SET nome = ?, cargo = ? WHERE pid = ?",(nome, cargo, pid),)
        
def excluir(pid):
    with conectar() as db:
        db.execute("DELETE FROM pessoas WHERE pid = ?", (pid,))
        
def busca_por_nome(termo):
    with conectar() as db:
        return db.execute("SELECT pid, nome, cargo FROM pessoas WHERE nome LIKE ? ORDER BY nome",(f"%{termo}%",),).fetchall()
    
 