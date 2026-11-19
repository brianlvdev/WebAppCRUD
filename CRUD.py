from pathlib import Path

import sqlite3

NOME_BANCO = Path(__file__).resolve().parent / "cadastro.db"

with sqlite3.connect(NOME_BANCO) as db:
    pass

def criar_banco() -> bool:
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS pessoas(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, altura REAL NOT NULL);")
            return True
    except sqlite3.Error as erro:
        print(f"[FALHA] na criação do banco: {erro}")
        return False
    
def cadastro_em_massa():
    cad_pessoas = [
        ("1","katia", "1.84"),
        ("2","leandro", "1.63"),
        ("3","januario", "2.02"),
        ("4","lindomar", "1.72"),
    ]
    
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            cur.executemany("INSERT INTO pessoas(cod, nome, altura) VALUES (?, ?, ?)", cad_pessoas)
        
    except sqlite3.Error as erro:
        print("\n[FALHA] Falha ao criar cadastro em massa..")

def Cadastrar_Pessoa() -> bool:
    print("\n ==== NOVO CADASTRO DE PESSOA ==== ")
    # leitura e Validacao de dados
    val_nome = input("\nNome: ").strip()
    if not val_nome:
        print("\n[ERRO] o nome é um campo obrigatorio!")
        return Cadastrar_Pessoa()
    
    while True:
        val_altura = input("Altura (metros): ").strip().replace(",",".")
        if not val_altura:
            print("\n[ERRO] A Altrura é um campo obrigatorio!")
            continue
        try:
            altura = float(val_altura)
            if altura <= 0.30 or altura > 3.0:
                print("\n[ERRO] Valor incoerente para Altura.")
                continue
        except ValueError:
            print("\n[ERRO] A Altura precisa ser um numero.")
        try:
            with sqlite3.connect(NOME_BANCO) as db:
                cur = db.cursor()
                cur.execute("INSERT INTO pessoas (nome, altura) VALUES (?, ?)", (val_nome, val_altura))
                print(f"\nCadastro de {val_nome} realizado com sucesso!")
                return True
        except sqlite3.Error as erro:
            print(f"[FALHA] Falha no cadastro do banco: {erro}")
            return False
        
def Listar_Pessoas() -> bool:
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            cur.execute("SELECT cod, nome, altura FROM pessoas ORDER BY cod;")
            primeiro = cur.fetchone()
            if not primeiro:
                print("\n[AVISO] Nenhuma pessoa foi cadastrada ate agora.")
                return True
            print(f"\n" + "=" * 45)
            print(f"{'CÓD':<8} {'NOME':<18} {'ALTURA':>15}")
            print(f"-" * 45)
            
            vcod, vnome, valtura = primeiro
            print(f"{vcod:<8} {vnome:<18} {valtura:>15} m")
            
            for vcod, vnome, valtura in cur:
                print(f"{vcod:<8} {vnome:<18} {valtura:>15} m")
                
            print(f"\n" + "=" * 45)
            return True
    except sqlite3.Error as erro:
        print(f"[FALHA] Falha ao acessar o banco: {erro}")
        return False

def Buscar_por_nome() -> bool:
    print("\n --- BUSCA DE PESSOA POR NOME --- " )
    termo = input("Digite o nome (ou parte dele) para buscar: ")
    if not termo:
        print(f"\n[AVISO] Nenhum termo foi informado ")
        return True
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            cur.execute("SELECT cod, nome, altura FROM pessoas WHERE nome LIKE ? ORDER BY nome;", (f"%{termo}%",))
            
            primeiro = cur.fetchone()
            if not primeiro:
                print(f"\n[AVISO] Nenhuma pessoa foi encontrada com '{termo}'.")
                return True
            print(f"\n" + "=" * 45)
            print(f"{'CÓD':<8} {'NOME':<18} {'ALTURA':>15}")
            print(f"-" * 45)
             
            vcod, vnome, valtura = primeiro
            print(f"{vcod:<8} {vnome:<18} {valtura:>15}m")
             
            for vcod, vnome, valtura in cur:
                print(f"{vcod:<8} {vnome:<18} {valtura:>15}m")
                 
            print(f"\n" + "=" * 45)
            return True           
    except sqlite3.Error as erro:
        print(f"[FALHA] Falaha ao buscar")
        return False

def Atualizar_Pessoa() -> bool:
    print("\n ==== ATUALIZAR PESSOAS ==== ")
    Listar_Pessoas()
    cod = int(input("\nDigite o codigo da pessoas que deseja atualizar: "))
    if not cod:
        print(f"\n[ERRO] Informe um codigo valido")          
        return Atualizar_Pessoa()
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            cur.execute("SELECT cod, nome, altura FROM pessoas WHERE cod LIKE ? ORDER BY nome;", (f"%{cod}%",))
            pesquisa = cur.fetchone()
            if not pesquisa:
                print(f"\n[AVISO] Nenhuma pessoa foi encontrada com o codigo:'{cod}'. ")
                return Atualizar_Pessoa()
            while True:
                novo_nome = input("Novo nome: ").strip()
                if not novo_nome:
                    print("\n[ERRO] O nome é um campo obrigatorio!")  
                    continue
                while True:
                    nova_altura = input("Altura (metros): ").strip().replace(",",".")
                    if not nova_altura:
                        print("\n[ERRO] A Altrura é um campo obrigatorio!")
                        continue
                    try:
                        altura = float(nova_altura)
                        if altura <= 0.30 or altura > 3.0:
                            print("\n[ERRO] Valor incoerente para Altura.")
                            continue
                    except ValueError:
                        print("\n[ERRO] A Altura precisa ser um numero.")
                    cur.execute("UPDATE pessoas SET nome = ?, altura = ? WHERE cod = ?", (novo_nome, nova_altura, cod))
                    print("\n A Atualizacao foi salva com sucesso!")
                    return True
    except sqlite3.Error as erro:
        print(f"[FALHA] Ocorreu um erro ao atualizar {erro}")
        return False

def Excluir_Pessoa() -> bool:
    Listar_Pessoas()
    print("\n ==== EXCLUIR PESSOAS ==== ")
    
    try:
        with sqlite3.connect(NOME_BANCO) as db:
            cur = db.cursor()
            while True:
                cod = input("\nDigite o Cod do usuario para prosseguir com a exclusao: ")
                if not cod:
                    input(f"\nO Cod '{cod}' é invalido, tente novamente\n [ENTER] para continuar..")
                    continue
                cur.execute("SELECT cod, nome, altura FROM pessoas WHERE cod = ? ORDER BY nome;", (cod,))
                pesquisa = cur.fetchone()
                if not pesquisa:
                    print(f"\n[AVISO] Nenhuma pessoa foi encontrada com o codigo:'{cod}'. ")
                    return Excluir_Pessoa()
                cur.execute("DELETE FROM pessoas WHERE cod = ?", (cod,))
                print(f"\nO usuario de codigo {cod} foi excluido com sucesso!")
                return True
    except sqlite3.Error as erro:
        print(f"[FALHA] Ococrreu uma falha ao tentar excluir ")
        return False