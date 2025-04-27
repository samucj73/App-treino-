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
        CREATE TABLE IF NOT EXISTS usuariosa (
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
        INSERT INTO usuariosa (nome, senha, idade, peso, altura, genero, objetivo, experiencia)
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

    select_query = sql.SQL("SELECT * FROM usuariosa WHERE nome = %s AND senha = %s")
    cursor.execute(select_query, (nome, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return usuario

# Função para calcular IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return round(imc, 2)

# Função para calcular metabolismo basal (Harris-Benedict)
def calcular_metabolismo_basal(peso, altura, idade, genero):
    if genero == "masculino":
        metabolismo_basal = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
    else:
        metabolismo_basal = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
    
    return round(metabolismo_basal, 2)

# Função para exibir a situação do usuário com base no IMC
def situacao_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc <= 24.9:
        return "Peso normal"
    elif 25 <= imc <= 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

# Função para criar o treino personalizado
def gerar_treino(usuario):
    # Lógica de treino baseada nas informações do usuário
    treino = "Treino personalizado baseado nos dados do usuário"
    return treino

# Interface de login
def login():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        usuario = obter_usuario(nome, senha)
        if usuario:
            st.write(f"Bem-vindo de volta, {usuario[1]}!")
            # Gerar treino
            treino = gerar_treino(usuario)
            st.write(treino)
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
