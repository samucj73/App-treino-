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

# Função para cadastrar o usuário
def cadastrar_usuario(nome, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir os dados do usuário no banco de dados
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

# Função para gerar treino semanal baseado no nível do usuário
def gerar_treino(usuario):
    experiencia = usuario[6]  # Experiência do usuário: iniciante, intermediário, avançado
    treino = f"Treino semanal personalizado para {usuario[1]}:\n\n"

    if experiencia == "iniciante":
        treino += "Segunda: Peito e tríceps\n- Supino reto: 3x10\n- Tríceps pulley: 3x12\n- Flexão de braços: 3x10\n"
        treino += "Terça: Pernas\n- Agachamento: 3x12\n- Leg press: 3x12\n- Panturrilha em pé: 3x15\n"
        treino += "Quarta: Descanso\n"
        treino += "Quinta: Costas e bíceps\n- Puxada frontal: 3x12\n- Rosca direta: 3x10\n- Remada unilateral: 3x12\n"
        treino += "Sexta: Ombros\n- Desenvolvimento com barra: 3x10\n- Elevação lateral: 3x12\n- Encolhimento de ombros: 3x12\n"
        treino += "Sábado e Domingo: Descanso\n"
    
    elif experiencia == "intermediário":
        treino += "Segunda: Peito e tríceps\n- Supino reto: 4x10\n- Tríceps pulley: 4x12\n- Flexão de braços: 4x12\n"
        treino += "Terça: Pernas\n- Agachamento: 4x10\n- Leg press: 4x12\n- Panturrilha em pé: 4x15\n"
        treino += "Quarta: Costas e bíceps\n- Puxada frontal: 4x10\n- Rosca direta: 4x10\n- Remada unilateral: 4x12\n"
        treino += "Quinta: Ombros\n- Desenvolvimento com barra: 4x10\n- Elevação lateral: 4x12\n- Encolhimento de ombros: 4x12\n"
        treino += "Sexta: Full body (treino completo)\n- Supino reto: 4x10\n- Agachamento: 4x10\n- Puxada frontal: 4x12\n"
        treino += "Sábado e Domingo: Descanso\n"

    elif experiencia == "avançado":
        treino += "Segunda: Peito e tríceps\n- Supino reto: 5x8\n- Tríceps pulley: 5x10\n- Flexão de braços: 5x12\n"
        treino += "Terça: Pernas\n- Agachamento: 5x8\n- Leg press: 5x10\n- Panturrilha em pé: 5x15\n"
        treino += "Quarta: Costas e bíceps\n- Puxada frontal: 5x8\n- Rosca direta: 5x8\n- Remada unilateral: 5x10\n"
        treino += "Quinta: Ombros\n- Desenvolvimento com barra: 5x8\n- Elevação lateral: 5x10\n- Encolhimento de ombros: 5x10\n"
        treino += "Sexta: Full body (treino completo)\n- Supino reto: 5x8\n- Agachamento: 5x8\n- Puxada frontal: 5x10\n"
        treino += "Sábado e Domingo: Descanso\n"

    return treino

# Interface de login
def login():
    nome = st.text_input("Nome")
    if st.button("Login"):
        usuario = obter_usuario(nome)
        if usuario:
            st.write(f"Bem-vindo de volta, {usuario[1]}!")
            # Exibir IMC, metabolismo basal e situação
            imc = calcular_imc(usuario[3], usuario[4])
            st.write(f"Seu IMC: {imc}")
            st.write(f"Sua situação IMC: {situacao_imc(imc)}")
            
            metabolismo_basal = calcular_metabolismo_basal(usuario[3], usuario[4], usuario[2], usuario[5])
            st.write(f"Seu metabolismo basal: {metabolismo_basal} kcal/dia")
            
            # Gerar treino
            treino = gerar_treino(usuario)
            st.write(treino)
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
        login
