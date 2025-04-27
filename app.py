import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
from fpdf import FPDF

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

        # Criar a tabela se ela não existir (agora com nome 'usuarios_a')
        criar_tabela_sql = """
        CREATE TABLE IF NOT EXISTS usuarios_a (
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
        print("Tabela 'usuarios_a' criada com sucesso!")

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

    # Inserir os dados do usuário na tabela 'usuarios_a'
    insert_query = sql.SQL("""
        INSERT INTO usuarios_a (nome, senha, idade, peso, altura, genero, objetivo, experiencia)
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

    select_query = sql.SQL("SELECT * FROM usuarios_a WHERE nome = %s AND senha = %s")
    cursor.execute(select_query, (nome, senha))
    usuario = cursor.fetchone()

    cursor.close()
    conn.close()
    
    return usuario

# Função para calcular IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    return round(imc, 2)

# Função para calcular taxa de metabolismo basal (TMB)
def calcular_metabolismo_basal(peso, altura, idade, genero):
    if genero == "masculino":
        tmb = 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)
    else:
        tmb = 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
    
    return round(tmb, 2)

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

# Função para exibir informações do usuário e treino
def exibir_informacoes(usuario):
    # Exibindo as informações do usuário
    st.subheader("Informações Pessoais:")
    st.write(f"**Nome:** {usuario[1]}")
    st.write(f"**Idade:** {usuario[3]} anos")
    st.write(f"**Peso:** {usuario[4]} kg")
    st.write(f"**Altura:** {usuario[5]} m")
    st.write(f"**Gênero:** {usuario[6]}")
    st.write(f"**Objetivo:** {usuario[7]}")
    st.write(f"**Experiência:** {usuario[8]}")
    
    # Calcular IMC e TMB
    imc = calcular_imc(usuario[4], usuario[5])
    tmb = calcular_metabolismo_basal(usuario[4], usuario[5], usuario[3], usuario[6])
    
    # Exibindo IMC e TMB
    st.write(f"**IMC:** {imc} ({situacao_imc(imc)})")
    st.write(f"**Taxa de Metabolismo Basal (TMB):** {tmb} calorias/dia")
    
    # Gerando e exibindo o treino
    treino = gerar_treino(usuario)
    st.subheader("Ficha de Treino Personalizado:")
    st.write(treino)

    # Botão para gerar PDF
    if st.button("Gerar PDF"):
        gerar_pdf(usuario, imc, tmb, treino)

# Função para salvar PDF com as informações do usuário
def gerar_pdf(usuario, imc, tmb, treino):
    pdf = FPDF()
    pdf.add_page()

    # Definindo o título do PDF
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Ficha de Treino Personalizada", ln=True, align="C")
    pdf.ln(10)
    
    # Informações do usuário
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Nome: {usuario[1]}", ln=True)
    pdf.cell(200, 10, txt=f"Idade: {usuario[3]} anos", ln=True)
    pdf.cell(200, 10, txt=f"Peso: {usuario[4]} kg", ln=True)
    pdf.cell(200, 10, txt=f"Altura: {usuario[5]} m", ln=True)
    pdf.cell(200, 10, txt=f"Gênero: {usuario[6]}", ln=True)
    pdf.cell(200, 10, txt=f"Objetivo: {usuario[7]}", ln=True)
    pdf.cell(200, 10, txt=f"Experiência: {usuario[8]}", ln=True)
    
    # IMC e TMB
    pdf.cell(200, 10, txt=f"IMC: {imc} ({situacao_imc(imc)})", ln=True)
    pdf.cell(200, 10, txt=f"TMB: {tmb} calorias/dia", ln=True)
    
    # Ficha de treino
    pdf.ln(10)
    pdf.multi_cell(200, 10, txt=f"Ficha de Treino:\n{treino}")
    
    # Salvar o PDF
    pdf.output("ficha_treino.pdf")
    st.success("PDF gerado com sucesso!")

# Função para determinar a situação do IMC
def situacao_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc <= 24.9:
        return "Peso normal"
    elif 25 <= imc <= 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

# Interface de login
def login():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        usuario = obter_usuario(nome, senha)
