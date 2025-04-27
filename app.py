import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

# Função para conectar ao banco de dados
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",
        database="sal_6scc",
        user="sal_6scc_user",
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"
    )
    return conn

# Função para criar a tabela no banco de dados
def criar_tabela():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        criar_tabela_sql = """
        CREATE TABLE IF NOT EXISTS usuariosam (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100),
            senha VARCHAR(100),
            idade INT,
            peso FLOAT,
            altura FLOAT,
            genero VARCHAR(10),
            objetivo VARCHAR(100),
            experiencia VARCHAR(20)
        );
        """
        cursor.execute(criar_tabela_sql)
        conn.commit()

    except Exception as e:
        st.error(f"Ocorreu um erro ao criar a tabela: {e}")
    finally:
        cursor.close()
        conn.close()

criar_tabela()

# Função para cadastrar usuário
def cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO usuariosam (nome, senha, idade, peso, altura, genero, objetivo, experiencia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (nome, senha, idade, peso, altura, genero, objetivo, experiencia))
    conn.commit()
    cursor.close()
    conn.close()

# Função para buscar usuário
def obter_usuario(nome, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = sql.SQL("SELECT * FROM usuariosam WHERE nome = %s AND senha = %s")
    cursor.execute(select_query, (nome, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

# Função para gerar treino personalizado
def gerar_treino(usuario):
    idade = usuario[3]
    peso = usuario[4]
    objetivo = usuario[7]
    experiencia = usuario[8]

    treino = ""

    if experiencia == "iniciante":
        treino += "### Treino Iniciante\n"
        treino += "- Agachamento (3x10)\n"
        treino += "- Flexão de braço (3x10)\n"
        treino += "- Remada unilateral (3x12 por lado)\n"
    elif experiencia == "intermediário":
        treino += "### Treino Intermediário\n"
        treino += "- Agachamento com barra (4x8)\n"
        treino += "- Supino reto (4x8)\n"
        treino += "- Levantamento terra (4x8)\n"
    elif experiencia == "avançado":
        treino += "### Treino Avançado\n"
        treino += "- Agachamento pesado (5x6)\n"
        treino += "- Supino pesado (5x6)\n"
        treino += "- Deadlift (5x6)\n"

    treino += "\n---\n"
    treino += f"**Idade:** {idade} anos\n\n"
    treino += f"**Peso:** {peso:.1f} kg\n\n"
    treino += f"**Objetivo:** {objetivo}\n\n"

    return treino

# Exibir treino
def exibir_treino(usuario):
    treino = gerar_treino(usuario)
    st.markdown(treino)

    if st.button("Exportar treino para PDF (em breve)"):
        st.info("Função de exportação em PDF ainda não implementada.")

# Interface de login
def login():
    st.subheader("Login")
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = obter_usuario(nome, senha)
        if usuario:
            st.session_state['usuario'] = usuario
            st.success(f"Bem-vindo(a), {usuario[1]}!")
            st.rerun()
        else:
            st.error("Nome ou senha inválidos!")

# Interface de cadastro
def cadastro():
    st.subheader("Cadastro")
    nome = st.text_input("Nome", key="cad_nome")
    senha = st.text_input("Senha", type="password", key="cad_senha")
    idade = st.number_input("Idade", min_value=18, max_value=120, key="cad_idade")
    peso = st.number_input("Peso (kg)", min_value=1.0, key="cad_peso")
    altura = st.number_input("Altura (m)", min_value=1.0, key="cad_altura")
    genero = st.selectbox("Gênero", ["masculino", "feminino"], key="cad_genero")
    objetivo = st.text_input("Objetivo", key="cad_objetivo")
    experiencia = st.selectbox("Experiência", ["iniciante", "intermediário", "avançado"], key="cad_experiencia")

    if st.button("Cadastrar"):
        cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia)
        st.success(f"Usuário {nome} cadastrado com sucesso!")
        st.info("Agora faça login para acessar seu treino.")

# Função principal
def main():
    st.title("🏋️‍♂️ App de Treino Personalizado")

    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])

    if 'usuario' in st.session_state:
        st.sidebar.success(f"Logado como: {st.session_state['usuario'][1]}")
        if st.sidebar.button("Sair"):
            del st.session_state['usuario']
            st.rerun()

        st.subheader("Seu Treino Personalizado")
        exibir_treino(st.session_state['usuario'])

    else:
        if menu == "Login":
            login()
        elif menu == "Cadastro":
            cadastro()

if __name__ == "__main__":
    main()
