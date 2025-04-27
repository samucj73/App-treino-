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

# Função para calcular IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        status = "Abaixo do peso"
    elif 18.5 <= imc < 25:
        status = "Peso normal"
    elif 25 <= imc < 30:
        status = "Sobrepeso"
    else:
        status = "Obesidade"
    return imc, status

# Função para calcular TMB
def calcular_tmb(peso, altura, idade, genero):
    altura_cm = altura * 100
    if genero == "masculino":
        tmb = 10 * peso + 6.25 * altura_cm - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura_cm - 5 * idade - 161
    return tmb

# Função para gerar treino
def gerar_treino(usuario):
    idade = usuario[3]
    peso = usuario[4]
    altura = usuario[5]
    genero = usuario[6]
    objetivo = usuario[7].lower()
    experiencia = usuario[8]

    imc, status_imc = calcular_imc(peso, altura)
    tmb = calcular_tmb(peso, altura, idade, genero)

    treino = f"## Dados Físicos\n"
    treino += f"- **Idade:** {idade} anos\n"
    treino += f"- **Peso:** {peso:.1f} kg\n"
    treino += f"- **Altura:** {altura:.2f} m\n"
    treino += f"- **IMC:** {imc:.2f} ({status_imc})\n"
    treino += f"- **TMB:** {tmb:.0f} kcal/dia\n"
    treino += f"- **Objetivo:** {objetivo.capitalize()}\n"
    treino += "---\n\n"

    treino += "## Treino Semanal\n"

    if objetivo == "emagrecimento":
        treino += """
**Treino A (Peito e Tríceps)**  
- Supino reto com halteres (3x15)  
- Crossover no cabo (3x20)  
- Tríceps corda (3x20)  

**Treino B (Costas e Bíceps)**  
- Puxada frente aberta (3x15)  
- Remada baixa (3x15)  
- Rosca direta (3x20)  

**Treino C (Pernas e Abdômen)**  
- Agachamento livre (3x15)  
- Leg press (3x20)  
- Abdominal prancha (3x30s)  

**Treino D (Ombros)**  
- Desenvolvimento com halteres (3x15)  
- Elevação lateral (3x20)  

**Treino E (Cardio/Funcional)**  
- Corrida/caminhada (30 minutos)  
- Circuito funcional (20 minutos)  
"""
    elif objetivo == "hipertrofia":
        treino += """
**Treino A (Peito e Tríceps)**  
- Supino reto barra (4x8)  
- Supino inclinado halteres (4x10)  
- Tríceps francês (4x12)  

**Treino B (Costas e Bíceps)**  
- Barra fixa assistida (4x8)  
- Remada unilateral (4x10)  
- Rosca alternada (4x12)  

**Treino C (Pernas e Abdômen)**  
- Agachamento livre (4x8)  
- Leg press (4x10)  
- Stiff (4x10)  
- Abdominal infra solo (3x20)  

**Treino D (Ombro e Trapézio)**  
- Desenvolvimento militar (4x8)  
- Elevação frontal (4x10)  
- Encolhimento trapézio (4x12)  

**Treino E (Cardio leve)**  
- Bicicleta ergométrica (20 minutos)  
"""
    else:  # resistência
        treino += """
**Treino A (Peito e Tríceps)**  
- Supino máquina (3x20)  
- Crossover leve (3x20)  
- Tríceps pulley (3x25)  

**Treino B (Costas e Bíceps)**  
- Puxada frente leve (3x20)  
- Remada máquina (3x20)  
- Rosca martelo (3x25)  

**Treino C (Pernas e Abdômen)**  
- Cadeira extensora (3x20)  
- Mesa flexora (3x20)  
- Abdominal oblíquo (3x30)  

**Treino D (Ombro e Core)**  
- Elevação lateral leve (3x20)  
- Prancha isométrica (3x30s)  

**Treino E (Cardio longo)**  
- Caminhada intensa (40 minutos)  
"""

    treino += "\n---\n"
    treino += "_Recomendamos avaliação médica antes de iniciar atividades físicas._"

    return treino

# Exibir treino
def exibir_treino(usuario):
    treino = gerar_treino(usuario)
    st.markdown(treino)

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
            st.experimental_rerun()
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
    objetivo = st.selectbox("Objetivo", ["emagrecimento", "hipertrofia", "resistência"], key="cad_objetivo")
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
            st.experimental_rerun()

        st.subheader("Seu Treino Personalizado")
        exibir_treino(st.session_state['usuario'])

    else:
        if menu == "Login":
            login()
        elif menu == "Cadastro":
            cadastro()

if __name__ == "__main__":
    main()
