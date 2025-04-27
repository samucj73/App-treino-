import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt

# Função para conectar ao banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",
        database="sal_6scc",
        user="sal_6scc_user",
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"
    )
    return conn

# Função para criar a tabela no banco de dados, se ela não existir
def criar_tabela():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'usuarios'
        );
        """)
        if not cursor.fetchone()[0]:
            criar_tabela_sql = """
            CREATE TABLE usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100),
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
        else:
            print("Tabela já existe, não será recriada.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        cursor.close()
        conn.close()

# Chamar a função para criar a tabela
criar_tabela()

# Função para cadastrar o usuário
def cadastrar_usuario(nome, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = sql.SQL("""
        INSERT INTO usuarios (nome, idade, peso, altura, genero, objetivo, experiencia)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """)
    cursor.execute(insert_query, (nome, idade, peso, altura, genero, objetivo, experiencia))
    conn.commit()
    cursor.close()
    conn.close()

# Função para obter dados do usuário
def obter_usuario(nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = sql.SQL("SELECT * FROM usuarios WHERE nome = %s")
    cursor.execute(select_query, (nome,))
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

# Função para exibir a situação do IMC
def situacao_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc <= 24.9:
        return "Peso normal"
    elif 25 <= imc <= 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

# Função para gerar treino semanal personalizado
def gerar_treino(usuario):
    experiencia = usuario[7]  # Experiência está na coluna 7
    treino = ""

    if experiencia == "iniciante":
        treino = {
            "Segunda": "Treino A: Peito e Tríceps (leve)",
            "Terça": "Descanso ou cardio leve",
            "Quarta": "Treino B: Costas e Bíceps (leve)",
            "Quinta": "Descanso ou yoga",
            "Sexta": "Treino C: Pernas e Abdômen (leve)",
            "Sábado": "Alongamento e caminhada",
            "Domingo": "Descanso"
        }
    elif experiencia == "intermediário":
        treino = {
            "Segunda": "Treino A: Peito e Tríceps (moderado)",
            "Terça": "Treino B: Costas e Bíceps (moderado)",
            "Quarta": "Cardio + Abdômen",
            "Quinta": "Treino C: Pernas e Ombros (moderado)",
            "Sexta": "Funcional ou HIIT leve",
            "Sábado": "Corrida leve ou circuito",
            "Domingo": "Descanso"
        }
    elif experiencia == "avançado":
        treino = {
            "Segunda": "Treino A: Peito pesado",
            "Terça": "Treino B: Costas pesadas",
            "Quarta": "Treino C: Pernas (pesadas)",
            "Quinta": "Treino D: Ombros + Abdômen",
            "Sexta": "Treino E: Braços",
            "Sábado": "Treino funcional intenso ou crossfit",
            "Domingo": "Alongamento e mobilidade"
        }
    else:
        treino = {"Mensagem": "Experiência não definida corretamente."}
    
    return treino

# Interface de login
def login():
    nome = st.text_input("Nome")
    if st.button("Login"):
        usuario = obter_usuario(nome)
        if usuario:
            st.success(f"Bem-vindo de volta, {usuario[1]}!")
            imc = calcular_imc(usuario[3], usuario[4])
            metabolismo = calcular_metabolismo_basal(usuario[3], usuario[4], usuario[2], usuario[5])
            situacao = situacao_imc(imc)

            st.subheader("Seus dados:")
            st.write(f"IMC: {imc} ({situacao})")
            st.write(f"Metabolismo Basal: {metabolismo} kcal/dia")
            st.write(f"Objetivo: {usuario[6]}")
            st.write(f"Experiência: {usuario[7]}")

            treino = gerar_treino(usuario)
            st.subheader("Ficha de Treino Semanal")
            for dia, atividade in treino.items():
                st.write(f"**{dia}:** {atividade}")
        else:
            st.error("Usuário não encontrado!")

# Interface de cadastro
def cadastro():
    nome = st.text_input("Nome")
    idade = st.number_input("Idade", min_value=18, max_value=120)
    peso = st.number_input("Peso (kg)", min_value=1.0)
    altura = st.number_input("Altura (m)", min_value=1.0)
    genero = st.selectbox("Gênero", ["masculino", "feminino"])
    objetivo = st.text_input("Objetivo")
    experiencia = st.selectbox("Experiência", ["iniciante", "intermediário", "avançado"])

    if st.button("Cadastrar"):
        cadastrar_usuario(nome, idade, peso, altura, genero, objetivo, experiencia)
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
