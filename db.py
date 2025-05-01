import psycopg2
from psycopg2 import sql

# Nome da tabela
NOME_TABELA = "alunos"

# Conexão com o banco de dados
def get_db_connection():
    return psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",
        database="sal_6scc",
        user="sal_6scc_user",
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"
    )

# Criar a tabela (se não existir)
def criar_tabela():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {table} (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) UNIQUE,
                email VARCHAR(100) UNIQUE,
                senha VARCHAR(100),
                idade INT,
                peso FLOAT,
                altura FLOAT,
                genero VARCHAR(10),
                objetivo VARCHAR(100),
                experiencia VARCHAR(20),
                dias_treino INT
            )
        """).format(table=sql.Identifier(NOME_TABELA)))
        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao criar a tabela: {e}")
    finally:
        cursor.close()
        conn.close()

# Verifica se o nome já existe
def usuario_existe(nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("SELECT 1 FROM {table} WHERE nome = %s").format(
            table=sql.Identifier(NOME_TABELA)), (nome,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conn.close()

# Cadastrar novo usuário
def cadastrar_usuario(nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino):
    if usuario_existe(nome):
        raise ValueError(f"O usuário '{nome}' já existe.")

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("""
            INSERT INTO {table} (nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """).format(table=sql.Identifier(NOME_TABELA)),
        (nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino))
        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao cadastrar usuário: {e}")
    finally:
        cursor.close()
        conn.close()

# Obter usuário por nome ou email e senha — CORRIGIDO para retornar dicionário
def obter_usuario(nome_ou_email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("""
            SELECT id, nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino
            FROM {table}
            WHERE (nome = %s OR email = %s) AND senha = %s
        """).format(table=sql.Identifier(NOME_TABELA)),
        (nome_ou_email, nome_ou_email, senha))
        
        row = cursor.fetchone()
        if row:
            keys = ["id", "nome", "idade", "peso", "altura", "genero", "objetivo", "experiencia", "dias_treino"]
            return dict(zip(keys, row))
        else:
            return None
    except Exception as e:
        raise Exception(f"Erro ao obter usuário: {e}")
    finally:
        cursor.close()
        conn.close()

# Atualizar dados do usuário
def atualizar_usuario(id_usuario, nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("""
            UPDATE {table}
            SET nome = %s, idade = %s, peso = %s, altura = %s, genero = %s,
                objetivo = %s, experiencia = %s, dias_treino = %s
            WHERE id = %s
        """).format(table=sql.Identifier(NOME_TABELA)),
        (nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino, id_usuario))
        conn.commit()
    except Exception as e:
        raise Exception(f"Erro ao atualizar usuário: {e}")
    finally:
        cursor.close()
        conn.close()

# Recuperar senha pelo email
def recuperar_por_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("""
            SELECT nome, senha FROM {table}
            WHERE email = %s
        """).format(table=sql.Identifier(NOME_TABELA)), (email,))
        return cursor.fetchone()
    except Exception as e:
        raise Exception(f"Erro ao recuperar por email: {e}")
    finally:
        cursor.close()
        conn.close()
# Obter usuário por nome ou email e senha — retornando dicionário
def obter_usuario(nome_ou_email, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql.SQL("""
            SELECT id, nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino
            FROM {table}
            WHERE (nome = %s OR email = %s) AND senha = %s
        """).format(table=sql.Identifier(NOME_TABELA)), (nome_ou_email, nome_ou_email, senha))
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "nome": row[1],
                "email": row[2],
                "senha": row[3],
                "idade": row[4],
                "peso": row[5],
                "altura": row[6],
                "genero": row[7],
                "objetivo": row[8],
                "experiencia": row[9],
                "dias_treino": row[10],
            }
        return None
    finally:
        cursor.close()
        conn.close()
