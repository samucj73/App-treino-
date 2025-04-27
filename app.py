import streamlit as st
import sqlite3
from datetime import date
import matplotlib.pyplot as plt
import pandas as pd

# Função para conectar ao banco de dados SQLite
def init_db():
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 senha TEXT NOT NULL,
                 nome TEXT NOT NULL,
                 idade INTEGER,
                 peso REAL,
                 altura REAL,
                 nivel_experiencia TEXT,
                 objetivo TEXT,
                 sexo TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS historico_treinos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT NOT NULL,
                 treino TEXT,
                 data DATE NOT NULL)''')

    conn.commit()
    conn.close()

# Função para cadastrar novos usuários
def cadastrar_usuario(username, senha, nome, idade, peso, altura, nivel_experiencia, objetivo, sexo):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''INSERT INTO usuarios (username, senha, nome, idade, peso, altura, nivel_experiencia, objetivo, sexo) 
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
              (username, senha, nome, idade, peso, altura, nivel_experiencia, objetivo, sexo))
    conn.commit()
    conn.close()

# Função para validar login
def validar_login(username, senha):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('SELECT * FROM usuarios WHERE username=? AND senha=?', (username, senha))
    user = c.fetchone()
    conn.close()
    return user

# Função para atualizar dados do usuário
def atualizar_dados_usuario(username, idade, peso, altura, nivel_experiencia, objetivo, sexo):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('''UPDATE usuarios 
                 SET idade=?, peso=?, altura=?, nivel_experiencia=?, objetivo=?, sexo=? 
                 WHERE username=?''', 
              (idade, peso, altura, nivel_experiencia, objetivo, sexo, username))
    conn.commit()
    conn.close()

# Função para gerar treino personalizado com base no objetivo
def gerar_treino(idade, peso, altura, nivel_experiencia, objetivo):
    treino = ""
    if nivel_experiencia == "Iniciante":
        treino = "Treino para Iniciante: 3x por semana, 2 exercícios por grupo muscular."
    elif nivel_experiencia == "Intermediário":
        treino = "Treino para Intermediário: 4x por semana, 3-4 exercícios por grupo muscular."
    elif nivel_experiencia == "Avançado":
        treino = "Treino para Avançado: 5x por semana, 5 exercícios por grupo muscular."
    
    if objetivo == "Hipertrofia":
        treino += "\nObjetivo: Hipertrofia muscular\n- Agachamento (4x12)\n- Supino reto (4x10)\n- Remada (3x10)\n- Desenvolvimento de ombro (3x12)"
    elif objetivo == "Emagrecimento":
        treino += "\nObjetivo: Emagrecimento\n- Cardio (20-30 minutos)\n- Agachamento (3x15)\n- Flexão de braço (3x15)\n- Prancha (3x30 segundos)"
    elif objetivo == "Força":
        treino += "\nObjetivo: Força\n- Agachamento pesado (5x5)\n- Supino reto (5x5)\n- Levantamento terra (4x6)"
    else:
        treino += "\nObjetivo: Manutenção\n- Circuito de full body (3x10 para cada exercício)"
    
    # Registro do treino gerado no histórico
    registrar_historico_treino(username, treino)
    return treino

# Função para registrar o histórico de treino no banco de dados
def registrar_historico_treino(username, treino):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('INSERT INTO historico_treinos (username, treino, data) VALUES (?, ?, ?)', 
              (username, treino, str(date.today())))
    conn.commit()
    conn.close()

# Função para calcular o IMC (Índice de Massa Corporal)
def calcular_imc(peso, altura):
    altura_metros = altura / 100  # Convertendo altura de cm para metros
    imc = peso / (altura_metros ** 2)
    return round(imc, 2)

# Função para calcular o Metabolismo Basal (TMB) usando a fórmula de Harris-Benedict
def calcular_tmb(peso, altura, idade, sexo):
    if sexo == "Masculino":
        tmb = 66.5 + (13.75 * peso) + (5.003 * altura) - (6.75 * idade)
    else:
        tmb = 655 + (9.563 * peso) + (1.850 * altura) - (4.676 * idade)
    return round(tmb, 2)

# Função para gerar gráfico de progresso do peso
def gerar_grafico_progresso(username):
    conn = sqlite3.connect('usuarios.db')
    c = conn.cursor()
    c.execute('SELECT data, peso FROM historico_treinos WHERE username=?', (username,))
    dados = c.fetchall()
    conn.close()
    
    if dados:
        df = pd.DataFrame(dados, columns=["Data", "Peso"])
        df['Data'] = pd.to_datetime(df['Data'])
        plt.figure(figsize=(10, 6))
        plt.plot(df['Data'], df['Peso'], marker='o', color='b')
        plt.title(f"Evolução do Peso de {username}")
        plt.xlabel("Data")
        plt.ylabel("Peso (kg)")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning("Ainda não há dados de progresso.")

# Função para exportar treino como planilha Excel
def exportar_treino_excel(treino, username):
    treino_lista = treino.split("\n")
    treino_df = pd.DataFrame(treino_lista, columns=["Exercícios"])
    nome_arquivo = f"treino_{username}.xlsx"
    treino_df.to_excel(nome_arquivo, index=False)
    st.download_button(
        label="Baixar Treino em Excel",
        data=treino_df.to_excel(index=False),
        file_name=nome_arquivo,
        mime="application/vnd.ms-excel"
    )

# Função para determinar a situação do IMC
def situacao_imc(imc):
    if imc < 18.5:
        return "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        return "Peso normal"
    elif 25 <= imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidade"

# Função para determinar a situação do TMB
def situacao_tmb(tmb, sexo):
    if sexo == "Masculino":
        if tmb < 1800:
            return "Metabolismo abaixo da média"
        elif 1800 <= tmb < 2200:
            return "Metabolismo normal"
        else:
            return "Metabolismo elevado"
    else:
        if tmb < 1500:
            return "Metabolismo abaixo da média"
        elif 1500 <= tmb < 1800:
            return "Metabolismo normal"
        else:
            return "Metabolismo elevado"

# Iniciar banco de dados
init_db()

# Interface Streamlit
st.title("App de Treino Personalizado")

menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro"])

if menu == "Cadastro":
    st.subheader("Cadastrar Novo Usuário")
    username = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")
    nome = st.text_input("Nome Completo")
    idade = st.number_input("Idade", min_value=18, max_value=100)
    peso = st.number_input("Peso (kg)", min_value=30, max_value=200)
    altura = st.number_input("Altura (cm)", min_value=140, max_value=220)
    nivel_experiencia = st.selectbox("Nível de experiência", ["Iniciante", "Intermediário", "Avançado"])
    objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Emagrecimento", "Força", "Manutenção"])
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])

    if st.button("Cadastrar"):
        cadastrar_usuario(username, senha, nome, idade, peso, altura, nivel_experiencia, objetivo, sexo)
        st.success("Usuário cadastrado com sucesso!")

if menu == "Login":
    username = st.text_input("Nome de usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        user = validar_login(username, senha)
        
        if user:
            st.success(f"Bem-vindo de volta, {user[3]}!")
            
            # Coletando e atualizando dados do usuário
            idade = st.number_input("Idade", value=user[4], min_value=18, max_value=100)
            peso = st.number_input("Peso (kg)", value=user[5], min_value=30, max_value=200)
            altura = st.number_input("Altura (cm)", value=user[6], min_value=140, max_value=220)
            nivel_experiencia = st.selectbox("Nível de experiência", ["Iniciante", "Intermediário", "Avançado"])
            objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Emagrecimento", "Força", "Manutenção"])
            sexo = st.selectbox("Sexo", ["Masculino", "Feminino"])

            if st.button("Salvar Dados"):
                atualizar_dados_usuario(username, idade, peso, altura, nivel_experiencia, objetivo, sexo)
                st.success("Dados atualizados com sucesso!")
            
            # Gerando e exibindo o treino personalizado
            treino_personalizado = gerar_treino(idade, peso, altura, nivel_experiencia, objetivo)
            st.header("Seu Treino Personalizado:")
            st.write(treino_personalizado)
            
            # Exibir IMC e TMB
            imc = calcular_imc(peso, altura)
            tmb = calcular_tmb(peso, altura, idade, sexo)
            st.write(f"Seu IMC: {imc} - {situacao_imc(imc)}")
            st.write(f"Seu Metabolismo Basal (TMB): {tmb} kcal/dia - {situacao_tmb(tmb, sexo)}")
            
            # Exibir gráfico de progresso
            gerar_grafico_progresso(username)
            
            # Exportar treino em Excel
            exportar_treino_excel(treino_personalizado, username)
