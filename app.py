import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
import matplotlib.pyplot as plt
from fpdf import FPDF

# Função para conectar ao banco de dados PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",  
        database="sal_6scc",  
        user="sal_6scc_user",  
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"
    )
    return conn

# Função para criar as tabelas no banco
def criar_tabelas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Criar tabela usuarios se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(100) UNIQUE,
                idade INT,
                peso FLOAT,
                altura FLOAT,
                genero VARCHAR(10),
                objetivo VARCHAR(100),
                experiencia VARCHAR(20)
            );
        """)
        # Criar tabela fichas de treino se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fichas_treino (
                id SERIAL PRIMARY KEY,
                usuario_id INT REFERENCES usuarios(id),
                treino TEXT
            );
        """)
        conn.commit()
        print("Tabelas verificadas/criadas com sucesso!")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        cursor.close()
        conn.close()

# Criar as tabelas ao iniciar
criar_tabelas()

# Função para cadastrar ou atualizar usuário
def cadastrar_usuario(nome, idade, peso, altura, genero, objetivo, experiencia):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar se usuário já existe
    cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (nome,))
    usuario = cursor.fetchone()

    if usuario:
        # Atualizar dados existentes
        cursor.execute("""
            UPDATE usuarios
            SET idade = %s, peso = %s, altura = %s, genero = %s, objetivo = %s, experiencia = %s
            WHERE nome = %s
        """, (idade, peso, altura, genero, objetivo, experiencia, nome))
    else:
        # Inserir novo usuário
        cursor.execute("""
            INSERT INTO usuarios (nome, idade, peso, altura, genero, objetivo, experiencia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nome, idade, peso, altura, genero, objetivo, experiencia))

    conn.commit()
    cursor.close()
    conn.close()

# Função para obter usuário
def obter_usuario(nome):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

# Função para gerar treino personalizado
def gerar_treino(experiencia):
    if experiencia == "iniciante":
        treino = {
            "Segunda": "Peito e Tríceps - 3x12",
            "Terça": "Costas e Bíceps - 3x12",
            "Quarta": "Pernas - 3x15",
            "Quinta": "Ombros e Abdômen - 3x12",
            "Sexta": "Treino Funcional - 2x circuito",
            "Sábado": "Alongamento/Yoga",
            "Domingo": "Descanso"
        }
    elif experiencia == "intermediário":
        treino = {
            "Segunda": "Peito - 4x10",
            "Terça": "Costas - 4x10",
            "Quarta": "Pernas e Abdômen - 4x12",
            "Quinta": "Ombros e Trapézio - 4x10",
            "Sexta": "Bíceps e Tríceps - 4x10",
            "Sábado": "Treino HIIT - 3x circuito",
            "Domingo": "Descanso"
        }
    else:  # Avançado
        treino = {
            "Segunda": "Peito pesado + Abdômen - 5x8",
            "Terça": "Costas + Bíceps pesado - 5x8",
            "Quarta": "Pernas (agachamento livre) - 5x10",
            "Quinta": "Ombros + Cardio intenso - 5x10",
            "Sexta": "Braços (ênfase) - 5x8",
            "Sábado": "Funcional + Core - 4x circuito",
            "Domingo": "Mobilidade/Recuperação"
        }
    return treino

# Função para salvar ficha no banco
def salvar_ficha(usuario_id, treino_texto):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Verifica se ficha já existe
    cursor.execute("SELECT id FROM fichas_treino WHERE usuario_id = %s", (usuario_id,))
    ficha = cursor.fetchone()

    if ficha:
        # Atualizar ficha
        cursor.execute("""
            UPDATE fichas_treino
            SET treino = %s
            WHERE usuario_id = %s
        """, (treino_texto, usuario_id))
    else:
        # Inserir nova ficha
        cursor.execute("""
            INSERT INTO fichas_treino (usuario_id, treino)
            VALUES (%s, %s)
        """, (usuario_id, treino_texto))

    conn.commit()
    cursor.close()
    conn.close()

# Função para gerar PDF da ficha
def gerar_pdf(nome, treino):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Ficha de Treino - {nome}", ln=True, align="C")

    for dia, atividade in treino.items():
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"{dia}: {atividade}", ln=True)

    caminho = f"ficha_{nome}.pdf"
    pdf.output(caminho)
    return caminho

# Interface de login
def login():
    nome = st.text_input("Nome")
    if st.button("Login"):
        usuario = obter_usuario(nome)
        if usuario:
            st.success(f"Bem-vindo de volta, {usuario[1]}!")

            treino = gerar_treino(usuario[7])
            st.subheader("Ficha Semanal:")
            for dia, atividade in treino.items():
                st.write(f"**{dia}**: {atividade}")

            if st.button("Salvar Ficha"):
                treino_texto = "\n".join([f"{dia}: {atividade}" for dia, atividade in treino.items()])
                salvar_ficha(usuario[0], treino_texto)
                st.success("Ficha salva no banco de dados!")

            if st.button("Gerar PDF"):
                caminho_pdf = gerar_pdf(usuario[1], treino)
                with open(caminho_pdf, "rb") as file:
                    st.download_button(label="Baixar Ficha em PDF", data=file, file_name=caminho_pdf, mime="application/pdf")

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
        st.success(f"Usuário {nome} cadastrado/atualizado com sucesso!")

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
