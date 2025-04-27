import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
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

        # Verifique se a tabela "usuarios" já existe
        cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'usuarios'
        );
        """)

        # Se a tabela não existir, crie-a
        if not cursor.fetchone()[0]:
            criar_tabela_sql = """
            CREATE TABLE usuarios (
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
def cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir os dados do usuário no banco de dados
    insert_query = sql.SQL("""
        INSERT INTO usuarios (nome, senha, idade, peso, altura, genero, objetivo, experiencia)
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

    select_query = sql.SQL("SELECT * FROM usuarios WHERE nome = %s AND senha = %s")
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
    treino = {
        "Segunda-feira": [
            {"exercicio": "Supino Reto", "series_repeticoes": "4x10-12", "equipamento": "Barra e banco reto"},
            {"exercicio": "Supino Inclinado com Halteres", "series_repeticoes": "4x8-10", "equipamento": "Halteres e banco inclinado"},
            {"exercicio": "Crossover", "series_repeticoes": "3x12-15", "equipamento": "Cabo e polia"}
        ],
        "Terça-feira": [
            {"exercicio": "Puxada na Barra Fixa", "series_repeticoes": "4x6-8", "equipamento": "Barra fixa"},
            {"exercicio": "Remada Unilateral com Halteres", "series_repeticoes": "4x10-12", "equipamento": "Halteres e banco inclinado"},
            {"exercicio": "Rosca Direta com Barra", "series_repeticoes": "3x10-12", "equipamento": "Barra reta"}
        ]
        # Adicionar mais dias com exercícios
    }
    return treino

# Função para gerar o PDF da ficha de treino
def gerar_pdf_ficha(usuario, treino):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Adicionar título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Ficha de Treino Personalizado", ln=True, align="C")

    # Dados do usuário
    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Usuário: {usuario[1]}", ln=True)
    pdf.cell(200, 10, f"Idade: {usuario[2]}", ln=True)
    pdf.cell(200, 10, f"Objetivo: {usuario[6]}", ln=True)
    pdf.cell(200, 10, f"Nível: {usuario[7]}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Treino Semanal", ln=True)

    # Ficha de treino
    pdf.set_font("Arial", "", 12)
    for dia, exercicios in treino.items():
        pdf.ln(5)
        pdf.cell(200, 10, f"{dia}:", ln=True)
        for exercicio in exercicios:
            pdf.cell(200, 10, f"{exercicio['exercicio']} - Séries: {exercicio['series_repeticoes']} - Equipamento: {exercicio['equipamento']}", ln=True)

    # Salvar PDF
    pdf.output(f"treino_{usuario[1]}.pdf")
    return f"treino_{usuario[1]}.pdf"

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
            
            # Gerar e disponibilizar o PDF
            pdf_path = gerar_pdf_ficha(usuario, treino)
            st.download_button("Baixar Ficha de Treino", data=open(pdf_path, "rb").read(), file_name=f"treino_{usuario[1]}.pdf", mime="application/pdf")
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
