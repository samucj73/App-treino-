import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql
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

# Função para criar a tabela no banco de dados, se ela não existir
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
        print(f"Ocorreu um erro ao criar a tabela: {e}")

    finally:
        cursor.close()
        conn.close()

# Função para cadastrar o usuário
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
    idade = usuario[3]
    peso = usuario[4]
    objetivo = usuario[7].lower()
    experiencia = usuario[8].lower()

    treino = f"## Plano de Treino Personalizado para {usuario[1]}\n"
    treino += "---\n\n"

    treino += f"**Faixa etária:** {idade} anos  \n"
    treino += f"**Peso atual:** {peso} kg  \n"
    treino += f"**Objetivo:** {objetivo.capitalize()}  \n"
    treino += f"**Nível de experiência:** {experiencia.capitalize()}\n\n"
    treino += "---\n\n"

    if objetivo == "emagrecimento":
        treino += "### Foco: Emagrecimento\n"
        treino += "- Corrida leve ou caminhada rápida (30 min)\n"
        treino += "- HIIT: 20 minutos (Ex: 40s alta intensidade / 20s descanso)\n"
        treino += "- Circuito funcional: agachamento, flexão, abdominal\n\n"

    elif objetivo == "ganho de massa":
        treino += "### Foco: Ganho de Massa Muscular\n"
        treino += "- Treino de musculação pesado\n"
        treino += "- Baixas repetições, alta carga\n"
        treino += "- Agachamento, Supino reto, Remada curvada\n\n"

    elif objetivo == "definição":
        treino += "### Foco: Definição Muscular\n"
        treino += "- Supersets: 2 exercícios seguidos sem descanso\n"
        treino += "- Alta intensidade e volume\n"
        treino += "- Agachamento + Flexão, Puxada + Remada\n\n"

    else:
        treino += "### Foco: Condicionamento Geral\n"
        treino += "- Treinos variados com pesos e cardio\n"
        treino += "- 3x por semana\n\n"

    treino += "---\n\n"

    if experiencia == "iniciante":
        treino += "### Sugestão de treino (Iniciante)\n"
        treino += "- Agachamento livre (3x12)\n"
        treino += "- Flexão de braço adaptada (3x10)\n"
        treino += "- Remada com halteres (3x12)\n"
        treino += "- Abdominais básicos (3x15)\n\n"

    elif experiencia == "intermediário":
        treino += "### Sugestão de treino (Intermediário)\n"
        treino += "- Agachamento com barra (4x8)\n"
        treino += "- Supino reto (4x8)\n"
        treino += "- Deadlift tradicional (4x8)\n"
        treino += "- Prancha abdominal (4x30s)\n\n"

    elif experiencia == "avançado":
        treino += "### Sugestão de treino (Avançado)\n"
        treino += "- Agachamento frontal (5x6)\n"
        treino += "- Supino inclinado pesado (5x6)\n"
        treino += "- Levantamento terra sumô (5x6)\n"
        treino += "- Core avançado (ab wheel, L-sit)\n\n"

    treino += "---\n\n"

    treino += "_Importante: sempre consultar um profissional antes de iniciar qualquer programa de treinamento._\n"

    return treino

# Função para exportar treino em PDF
def exportar_treino_pdf(treino_texto, nome_usuario):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Treino personalizado para {nome_usuario}", ln=True, align='C')
    pdf.ln(10)

    for linha in treino_texto.strip().split('\n'):
        pdf.multi_cell(0, 10, linha)

    nome_arquivo = f"treino_{nome_usuario}.pdf"
    pdf.output(nome_arquivo)
    return nome_arquivo

# Função para exibir treino após login
def exibir_treino(usuario):
    treino = gerar_treino(usuario)
    st.markdown(treino)

    if st.button("Exportar treino para PDF"):
        nome_arquivo = exportar_treino_pdf(treino.replace("#", "").replace("*", ""), usuario[1])
        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="Baixar Treino em PDF",
                data=file,
                file_name=nome_arquivo,
                mime="application/pdf"
            )

# Interface de login
def login():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        usuario = obter_usuario(nome, senha)
        if usuario:
            st.session_state['usuario_logado'] = usuario
            st.success(f"Bem-vindo de volta, {usuario[1]}!")
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
    objetivo = st.selectbox("Objetivo", ["emagrecimento", "ganho de massa", "definição", "condicionamento geral"])
    experiencia = st.selectbox("Experiência", ["iniciante", "intermediário", "avançado"])

    if st.button("Cadastrar"):
        cadastrar_usuario(nome, senha, idade, peso, altura, genero, objetivo, experiencia)
        st.success(f"Usuário {nome} cadastrado com sucesso!")

# Função principal
def main():
    st.title("App de Treino Personalizado")

    criar_tabela()

    if 'usuario_logado' in st.session_state:
        st.success(f"Bem-vindo, {st.session_state['usuario_logado'][1]}!")
        exibir_treino(st.session_state['usuario_logado'])

        if st.button("Logout"):
            del st.session_state['usuario_logado']
            st.experimental_rerun()

    else:
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"])
        if opcao == "Login":
            login()
        elif opcao == "Cadastro":
            cadastro()

if __name__ == "__main__":
    main()
