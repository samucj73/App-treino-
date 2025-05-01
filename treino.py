import streamlit as st
from datetime import datetime

# Sessão de histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Dados do usuário (simulado)
usuario = {
    "nome": "João",
    "objetivo": "hipertrofia",
    "experiencia": "intermediário",
    "dias_treino": 4
}

# Exercícios por grupo
grupos_musculares = {
    "Peito": ["Supino reto", "Supino inclinado", "Crucifixo", "Crossover", "Peck deck"],
    "Costas": ["Puxada frente", "Remada curvada", "Remada baixa", "Pulldown", "Levantamento terra"],
    "Perna": ["Agachamento", "Leg press", "Cadeira extensora", "Mesa flexora", "Stiff"],
    "Ombro": ["Desenvolvimento militar", "Elevação lateral", "Arnold press", "Crucifixo inverso"],
    "Bíceps": ["Rosca direta", "Rosca alternada", "Rosca martelo"],
    "Tríceps": ["Tríceps corda", "Tríceps francês", "Tríceps banco"],
    "Abdômen": ["Prancha", "Crunch", "Elevação de pernas", "Bicicleta"],
}

# Função para gerar treino automático
def gerar_treino(objetivo, experiencia, dias):
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

# Função para gerar treino personalizado
def gerar_treino_personalizado(grupos_escolhidos, dias, volume, intensidade):
    volume_map = {"baixo": 2, "médio": 3, "alto": 4}
    intensidade_map = {"leve": "15-20", "moderada": "10-15", "alta": "6-10"}

    series = volume_map.get(volume, 3)
    reps = intensidade_map.get(intensidade, "10-15")

    treino = {}
    for i in range(dias):
        grupo = grupos_escolhidos[i % len(grupos_escolhidos)]
        exercicios = grupos_musculares[grupo][:series + 1]
        treino[f"Dia {i+1} - {grupo}"] = [f"{ex} - {series}x{reps}" for ex in exercicios]
    return treino

# Interface
st.title("App de Treino Completo")

aba = st.sidebar.radio("Menu", ["Treino Automático", "Treino Personalizado", "Registrar Manual", "Histórico"])

if aba == "Treino Automático":
    st.header("Treino Gerado Automaticamente")
    treino = gerar_treino(usuario["objetivo"], usuario["experiencia"], usuario["dias_treino"])
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
        st.success("Treino automático salvo no histórico!")

elif aba == "Treino Personalizado":
    st.header("Gerar Treino Personalizado")

    grupos_escolhidos = st.multiselect("Grupos Musculares", list(grupos_musculares.keys()))
    dias = st.slider("Dias de Treino", 1, 7, 3)
    volume = st.selectbox("Volume do Treino", ["baixo", "médio", "alto"])
    intensidade = st.selectbox("Intensidade do Treino", ["leve", "moderada", "alta"])

    if st.button("Gerar Treino"):
        if not grupos_escolhidos:
            st.warning("Selecione pelo menos um grupo muscular.")
        else:
            treino = gerar_treino_personalizado(grupos_escolhidos, dias, volume, intensidade)
            for dia, exercicios in treino.items():
                with st.expander(dia):
                    for ex in exercicios:
                        st.markdown(f"- {ex}")

            if st.button("Salvar este treino personalizado"):
                for dia, exs in treino.items():
                    st.session_state.historico.append({
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "tipo": "Personalizado",
                        "grupo": dia,
                        "exercicios": exs
                    })
                st.success("Treino personalizado salvo no histórico!")

elif aba == "Registrar Manual":
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

elif aba == "Histórico":
    st.header("Histórico de Treinos")
    if st.session_state.historico:
        for treino in reversed(st.session_state.historico):
            st.subheader(f"{treino['data']} - {treino['grupo']} ({treino['tipo']})")
            for ex in treino["exercicios"]:
                st.markdown(f"- {ex}")
    else:
        st.info("Nenhum treino registrado ainda.")
