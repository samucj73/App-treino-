import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt

# Função para conectar ao banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",  # Substitua pelo host do seu banco de dados no Render
        database="sal_6scc",  # Substitua pelo nome do banco de dados
        user="sal_6scc_user",  # Substitua pelo seu nome de usuário
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"  # Substitua pela sua senha
    )
    return conn

# Função para criar a tabela no banco de dados, se ela não existir
def criar_tabela():
    try:
        # Conecte-se ao banco de dados PostgreSQL
        conn = get_db_connection()
        cursor = conn.cursor()

        # Criar a tabela se ela não existir
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
        print("Tabela criada com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao criar a tabela: {e}")
        
    finally:
        cursor.close()
        conn.close()

# Chamar a função para criar a tabela
criar_tabela()

# Função para cadastrar o usuário
def cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir os dados do usuário no banco de dados
    insert_query = sql.SQL("""
        INSERT INTO usuariosam (nome, senha, idade, peso, altura, genero, objetivo, experiencia)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (nome, senha, idade, peso, altura, genero, objetivo, experiencia))
    conn.commit()

    cursor.close()
    conn.close()

# Função para obter dados do usuário
def obter_usuario(nome, senha):
    conn = get_db_connection()
    cursor = conn.cursor()

    select_query = sql.SQL("SELECT * FROM usuariosam WHERE nome = %s AND senha = %s")
    cursor.execute(select_query, (nome, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return usuario

# Função para gerar treino baseado nas informações do usuário
def gerar_treino(usuario):
    # Definir treino de acordo com a experiência
    experiencia = usuario[7]  # A experiência é o 7º campo no banco de dados (iniciante, intermediário, avançado)
    
    treino = ""
    if experiencia == "iniciante":
        treino = """
        - Agachamento (3 séries de 10 repetições)
        - Flexão de braço (3 séries de 10 repetições)
        - Remada unilateral (3 séries de 12 repetições por lado)
        Equipamento: Halteres, banco
        """
    elif experiencia == "intermediário":
        treino = """
        - Agachamento com barra (4 séries de 8 repetições)
        - Supino reto com barra (4 séries de 8 repetições)
        - Levantamento terra (4 séries de 8 repetições)
        Equipamento: Barra, halteres
        """
    elif experiencia == "avançado":
        treino = """
        - Agachamento com barra (5 séries de 6 repetições)
        - Supino reto com barra (5 séries de 6 repetições)
        - Deadlift (5 séries de 6 repetições)
        Equipamento: Barra, pesos livres
        """
    return treino

# Função para exibir treino após login
def exibir_treino(usuario):
    treino = gerar_treino(usuario)
    st.write("Seu treino personalizado é:")
    st.write(treino)

# Interface de login
def login():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        usuario = obter_usuario(nome, senha)
        if usuario:
            st.write(f"Bem-vindo de volta, {usuario[1]}!")
            # Exibir treino personalizado
            exibir_treino(usuario)
        else:
            st.error("Usuário ou senha incorretos!")

# Interface de cadastro
def cadastro():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    idade = st.number_input("Idade", min_value=18, max_value=120)
    peso = st.number_input("Peso (kg)", min_value=1.0)
    altura = st.number_input("Altura (m)", min_value=1.0)
    genero = st.selectbox("Gênero", ["masculino", "feminino"])
    objetivo = st.text_input("Objetivo")
    experiencia = st.selectbox("Experiência", ["iniciante", "intermediário", "avançado"])

    if st.button("Cadastrar"):
        cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia)
        st.success(f"Usuário {nome} cadastrado com sucesso!")

# Função principal
def main():
    st.title("App de Treino Personalizado")

    opcao = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"])

    if opcao == "Login":
        login()
    elif opcao == "Cadastro":
        cadastro()

if __name__ == "__main__":
    main()
