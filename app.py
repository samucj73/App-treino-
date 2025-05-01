import streamlit as st
from datetime import datetime
from usuario import cadastrar, obter, atualizar, recuperar_por_email
from email_utils import enviar_email_recuperacao
from treino import gerar_treino as gerar_treino_padrao
from calculos import (
    calcular_imc, calcular_tmb, calcular_percentual_gordura,
    calcular_massa_muscular, calcular_idade_metabolica,
    recomendacao_hidratacao, recomendacao_proteina
)

# ---------------- NOVO BLOCO PARA TREINO PERSONALIZADO ----------------
grupos_musculares = {
    "Peito": ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover", "Peck deck"],
    "Costas": ["Puxada frente", "Remada curvada", "Remada baixa", "Pulldown", "Levantamento terra"],
    "Perna": ["Agachamento", "Leg press", "Cadeira extensora", "Mesa flexora", "Stiff"],
    "Ombro": ["Desenvolvimento militar", "Elevação lateral", "Arnold press", "Crucifixo inverso"],
    "Bíceps": ["Rosca direta", "Rosca alternada", "Rosca martelo"],
    "Tríceps": ["Tríceps corda", "Tríceps francês", "Tríceps banco"],
    "Abdômen": ["Prancha", "Crunch", "Elevação de pernas", "Bicicleta"],
}

def gerar_treino_personalizado(objetivo, experiencia, dias):
    if objetivo == "hipertrofia":
        reps = "8-12"
        series = 4 if experiencia == "intermediário" else 3
    elif objetivo == "emagrecimento":
        reps = "15-20"
        series = 3
    else:
        reps = "10-15"
        series = 3

    treino = {}
    grupos = list(grupos_musculares.keys())
    for i in range(dias):
        grupo = grupos[i % len(grupos)]
        treino[f"Dia {i+1} - {grupo}"] = [
            f"{ex} - {series}x{reps}" for ex in grupos_musculares[grupo][:5]
        ]
    return treino

def aba_treino_personalizado(usuario):
    st.subheader("Treino Personalizado")

    if "historico" not in st.session_state:
        st.session_state.historico = []

    menu = st.radio("Escolha uma opção", ["Treino Automático", "Registrar Manual", "Histórico"])

    if menu == "Treino Automático":
        treino = gerar_treino_personalizado(usuario["objetivo"], usuario["experiencia"], usuario["dias_treino"])
        st.header("Treino Gerado Automaticamente")
        for dia, exercicios in treino.items():
            with st.expander(dia):
                for ex in exercicios:
                    st.markdown(f"- {ex}")
        if st.button("Salvar este treino no histórico"):
            for dia, exs in treino.items():
                st.session_state.historico.append({
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "tipo": "Automático",
                    "grupo": dia,
                    "exercicios": exs
                })
            st.success("Treino salvo no histórico!")

    elif menu == "Registrar Manual":
        st.header("Registrar Treino Manual")
        grupo = st.selectbox("Grupo Muscular", list(grupos_musculares.keys()))
        opcoes = grupos_musculares[grupo]
        escolhidos = st.multiselect("Escolha os exercícios", opcoes)
        if st.button("Registrar treino manual"):
            if escolhidos:
                st.session_state.historico.append({
                    "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "tipo": "Manual",
                    "grupo": grupo,
                    "exercicios": escolhidos
                })
                st.success("Treino manual registrado!")
            else:
                st.warning("Selecione pelo menos um exercício.")

    elif menu == "Histórico":
        st.header("Histórico de Treinos")
        if st.session_state.historico:
            for treino in reversed(st.session_state.historico):
                st.subheader(f"{treino['data']} - {treino['grupo']} ({treino['tipo']})")
                for ex in treino["exercicios"]:
                    st.markdown(f"- {ex}")
        else:
            st.info("Nenhum treino registrado ainda.")

# ---------------- FIM DO BLOCO NOVO ----------------

def splash_screen():
    st.markdown("<h1 style='text-align: center;'>Personal Trainer App</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Seu treino, suas metas, sua evolução!</p>", unsafe_allow_html=True)
    st.markdown("---")

def cadastro():
    st.subheader("Cadastro de Novo Usuário")
    with st.form("cadastro_form"):
        nome = st.text_input("Nome de usuário")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        idade = st.number_input("Idade", min_value=10, max_value=100, step=1)
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=300.0, step=0.1)
        altura = st.number_input("Altura (m)", min_value=1.0, max_value=2.5, step=0.01)
        genero = st.radio("Gênero", ("Masculino", "Feminino"))
        objetivo = st.selectbox("Objetivo", ["Perda de peso", "Ganhar massa muscular", "Melhorar resistência"])
        experiencia = st.selectbox("Nível de experiência", ["Iniciante", "Intermediário", "Avançado"])
        dias_treino = st.slider("Dias de treino na semana", 1, 7, 3)

        if st.form_submit_button("Cadastrar"):
            try:
                cadastrar(nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino)
                st.success("Usuário cadastrado com sucesso!")
                st.balloons()
            except Exception as e:
                st.error(str(e))

def login():
    st.subheader("Login")
    with st.form("login_form"):
        nome = st.text_input("Nome de usuário")
        senha = st.text_input("Senha", type="password")
        if st.form_submit_button("Entrar"):
            usuario = obter(nome, senha)
            if usuario:
                st.session_state['usuario'] = usuario
                st.toast(f"Bem-vindo(a), {usuario['nome']}!", icon="🎉")
                st.rerun()
            else:
                st.error("Nome de usuário ou senha incorretos.")
    if st.button("Esqueceu a senha?"):
        recuperar_senha_form()

def recuperar_senha_form():
    st.subheader("Recuperação de Senha")
    email = st.text_input("Digite seu e-mail cadastrado")
    if st.button("Recuperar Senha"):
        if email:
            try:
                usuario = recuperar_por_email(email)
                if usuario:
                    enviar_email_recuperacao(email, usuario["senha"])
                    st.success("E-mail de recuperação enviado!")
                else:
                    st.error("E-mail não encontrado!")
            except Exception as e:
                st.error(f"Erro: {e}")
        else:
            st.warning("Insira um e-mail válido.")

def exibir_treino():
    usuario = st.session_state['usuario']
    st.title(f"Treino de {usuario['nome']}")
    tabs = st.tabs(["📋 Perfil", "🏋️ Treino", "⚙️ Configurações", "📊 Análises Corporais", "📆 Treino Personalizado"])

    with tabs[0]:
        st.subheader("Informações do Usuário")
        st.write(f"**Idade:** {usuario['idade']} anos")
        st.write(f"**Peso:** {usuario['peso']} kg")
        st.write(f"**Altura:** {usuario['altura']} m")
        st.write(f"**Gênero:** {usuario['genero']}")
        st.write(f"**Objetivo:** {usuario['objetivo']}")
        st.write(f"**Experiência:** {usuario['experiencia']}")
        st.write(f"**Dias de treino por semana:** {usuario['dias_treino']}")

    with tabs[1]:
        st.subheader("Plano de Treino")
        treino = gerar_treino_padrao(usuario['objetivo'], usuario['experiencia'], usuario['dias_treino'])
        progress = st.progress(0)
        for i in range(100):
            progress.progress(i + 1)
        st.success("Treino carregado!")
        for dia, exercicios in treino.items():
            with st.expander(dia):
                for exercicio in exercicios:
                    st.write(f"- {exercicio}")

    with tabs[2]:
        st.subheader("Atualizar Dados")
        with st.form("form_atualizar"):
            nome = st.text_input("Nome", value=usuario['nome'])
            idade = st.number_input("Idade", value=usuario['idade'])
            peso = st.number_input("Peso", value=usuario['peso'])
            altura = st.number_input("Altura", value=usuario['altura'])
            genero = st.radio("Gênero", ["Masculino", "Feminino"], index=0 if usuario['genero'] == "Masculino" else 1)
            objetivo = st.selectbox("Objetivo", ["Perda de peso", "Ganhar massa muscular", "Melhorar resistência"], index=["Perda de peso", "Ganhar massa muscular", "Melhorar resistência"].index(usuario['objetivo']))
            experiencia = st.selectbox("Experiência", ["Iniciante", "Intermediário", "Avançado"], index=["Iniciante", "Intermediário", "Avançado"].index(usuario['experiencia']))
            dias_treino = st.slider("Dias de treino por semana", 1, 7, value=usuario['dias_treino'])

            if st.form_submit_button("Salvar"):
                atualizar(usuario['id'], nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino)
                st.success("Dados atualizados!")
                st.rerun()
        if st.button("Sair da Conta"):
            del st.session_state['usuario']
            st.rerun()

    with tabs[3]:
        st.subheader("Relatório Corporal")
        circ = st.number_input("Circunferência da cintura (cm)", min_value=30.0)
        if circ:
            imc, faixa = calcular_imc(usuario['peso'], usuario['altura'])
            tmb = calcular_tmb(usuario['idade'], usuario['peso'], usuario['altura'], usuario['genero'])
            gordura = calcular_percentual_gordura(usuario['peso'], circ, usuario['idade'], usuario['genero'])
            massa_magra = calcular_massa_muscular(usuario['peso'], gordura)
            idade_met = calcular_idade_metabolica(tmb, usuario['idade'])
            agua = recomendacao_hidratacao(usuario['peso'])
            proteina = recomendacao_proteina(usuario['peso'], usuario['objetivo'])

            st.markdown(f"**IMC:** {imc:.2f} ({faixa})")
            st.markdown(f"**TMB:** {tmb:.0f} kcal")
            st.markdown(f"**% Gordura:** {gordura:.2f}%")
            st.markdown(f"**Massa Magra:** {massa_magra:.2f} kg")
            st.markdown(f"**Idade Metabólica:** {idade_met:.0f} anos")
            st.markdown(f"**Hidratação Diária:** {agua:.0f} ml")
            st.markdown(f"**Proteína Diária:** {proteina:.2f} g")

    with tabs[4]:
        aba_treino_personalizado(usuario)

# EXECUÇÃO PRINCIPAL
if __name__ == "__main__":
    st.set_page_config(page_title="Personal Trainer App", page_icon=":muscle:", layout="centered")
    if 'usuario' in st.session_state:
        exibir_treino()
    else:
        splash_screen()
        opcao = st.sidebar.selectbox("Escolha uma opção", ["Login", "Cadastro"])
        login() if opcao == "Login" else cadastro()
