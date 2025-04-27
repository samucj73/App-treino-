import streamlit as st
import psycopg2
from psycopg2 import sql

# ======== Banco de dados =========
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-d06oq3qli9vc73ejebbg-a",
        database="sal_6scc",
        user="sal_6scc_user",
        password="NT5pmK5SWCB0voVzFqRkofj8YVKjL3Q1"
    )
    return conn

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
        print(f"Erro ao criar tabela: {e}")
    finally:
        cursor.close()
        conn.close()

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

def obter_usuario(nome, senha):
    conn = get_db_connection()
    cursor = conn.cursor()
    select_query = sql.SQL("SELECT * FROM usuariosam WHERE nome = %s AND senha = %s")
    cursor.execute(select_query, (nome, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario

# ======== Funções do app =========
def gerar_treino(usuario):
    idade = usuario[3]
    peso = usuario[4]
    objetivo = usuario[7]
    experiencia = usuario[8]

    treino = f"### Plano de Treino para {objetivo.capitalize()}\n"
    treino += f"- **Idade**: {idade} anos\n"
    treino += f"- **Peso**: {peso} kg\n\n"

    if experiencia == "iniciante":
        treino += """
- **Agachamento** (3x10)
- **Flexão de braço** (3x10)
- **Remada unilateral** (3x12 por lado)

**Equipamentos**: Halteres, banco
"""
    elif experiencia == "intermediário":
        treino += """
- **Agachamento com barra** (4x8)
- **Supino reto com barra** (4x8)
- **Levantamento terra** (4x8)

**Equipamentos**: Barra, halteres
"""
    elif experiencia == "avançado":
        treino += """
- **Agachamento com barra pesado** (5x6)
- **Supino reto pesado** (5x6)
- **Deadlift pesado** (5x6)

**Equipamentos**: Barra, pesos livres
"""
    return treino

def login():
    nome = st.text_input("Nome")
    senha = st.text_input("Senha", type="password")
    if st.button("Login"):
        usuario = obter_usuario(nome, senha)
        if usuario:
            st.session_state.usuario = usuario
            st.success(f"Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos!")

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

def main():
    st.title("App de Treino Personalizado")

    # Inicializar sessão
    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    criar_tabela()

    # Se usuário já logado
    if st.session_state.usuario:
        st.success(f"Bem-vindo, {st.session_state.usuario[1]}!")

        # Mostrar treino
        treino = gerar_treino(st.session_state.usuario)
        st.markdown(treino)

        # Botão de logout
        if st.button("Logout"):
            st.session_state.usuario = None
            st.experimental_rerun()

    else:
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"])

        if opcao == "Login":
            login()
        elif opcao == "Cadastro":
            cadastro()

if __name__ == "__main__":
    main()
