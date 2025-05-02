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

# Exercícios por grupo e objetivo
exercicios = {
    "Peito": {
        "hipertrofia": [("Supino reto", "4x8-12"), ("Supino inclinado", "4x8-12"), ("Crucifixo", "4x8-12"), ("Crossover", "4x8-12")],
        "emagrecimento": [("Supino reto", "3x15-20"), ("Supino inclinado", "3x15-20"), ("Crossover", "3x15-20")],
        "resistencia": [("Peck deck", "3x10-15"), ("Supino reto", "3x10-15")]
    },
    "Costas": {
        "hipertrofia": [("Puxada frente aberta", "4x8-12"), ("Remada curvada", "4x8-12"), ("Levantamento terra", "4x8-12")],
        "emagrecimento": [("Pulldown", "3x15-20"), ("Puxada frente aberta", "3x15-20")],
        "resistencia": [("Remada baixa", "3x10-15"), ("Levantamento terra", "3x10-15")]
    },
    "Perna": {
        "hipertrofia": [("Agachamento", "4x8-12"), ("Leg press", "4x8-12"), ("Cadeira extensora", "4x8-12")],
        "emagrecimento": [("Cadeira adutora", "3x15-20"), ("Afundo", "3x15-20")],
        "resistencia": [("Stiff", "3x10-15"), ("Leg press", "3x10-15")]
    },
    "Ombro": {
        "hipertrofia": [("Desenvolvimento militar", "4x8-12"), ("Arnold press", "4x8-12"), ("Elevação lateral", "4x8-12")],
        "emagrecimento": [("Elevação lateral", "3x15-20"), ("Desenvolvimento militar", "3x15-20")],
        "resistencia": [("Arnold press", "3x10-15"), ("Crucifixo inverso", "3x10-15")]
    },
    "Bíceps": {
        "hipertrofia": [("Rosca direta", "4x8-12"), ("Rosca alternada", "4x8-12"), ("Rosca martelo", "4x8-12")],
        "emagrecimento": [("Rosca direta", "3x15-20"), ("Rosca martelo", "3x15-20")],
        "resistencia": [("Rosca alternada", "3x10-15"), ("Rosca direta", "3x10-15")]
    },
    "Tríceps": {
        "hipertrofia": [("Tríceps francês", "4x8-12"), ("Tríceps banco", "4x8-12")],
        "emagrecimento": [("Tríceps banco", "3x15-20"), ("Tríceps corda", "3x15-20")],
        "resistencia": [("Tríceps banco", "3x10-15"), ("Tríceps francês", "3x10-15")]
    },
    "Abdômen": {
        "hipertrofia": [("Prancha", "4x30s"), ("Crunch", "4x15-20")],
        "emagrecimento": [("Bicicleta", "3x15-20"), ("Prancha", "3x30s")],
        "resistencia": [("Crunch", "3x10-15"), ("Elevação de pernas", "3x10-15")]
    },
}

# Função para gerar treino automático
def gerar_treino(objetivo, experiencia, dias):
    treino = {}
    grupos = list(exercicios.keys())
    for i in range(dias):
        grupo = grupos[i % len(grupos)]
        treino[f"Dia {i+1} - {grupo}"] = [f"{ex[0]} - {ex[1]}" for ex in exercicios[grupo][objetivo]]
    return treino

# Função para gerar treino personalizado
def gerar_treino_personalizado(grupos_escolhidos, dias, volume, intensidade, objetivo):
    volume_map = {"baixo": 2, "médio": 3, "alto": 4}
    intensidade_map = {"leve": "15-20", "moderada": "10-15", "alta": "6-10"}

    series = volume_map.get(volume, 3)
    reps = intensidade_map.get(intensidade, "10-15")

    treino = {}
    for i in range(dias):
        grupo = grupos_escolhidos[i % len(grupos_escolhidos)]
        exercicios_grupo = exercicios[grupo][objetivo]
        treino[f"Dia {i+1} - {grupo}"] = [f"{ex[0]} - {series}x{reps}" for ex in exercicios_grupo]
    return treino

# Interface
st.title("App de Treino Completo")

aba = st.sidebar.radio("Menu", ["Treino Automático", "Treino Personalizado", "Registrar Manual", "Histórico"])

if aba == "Treino Automático":
    st.header("Treino Gerado Automaticamente")
    treino = gerar_treino(usuario["objetivo"], usuario["experiencia"], usuario["dias_treino"])
    for dia, lista_exercicios in treino.items():
        with st.expander(dia):
            for ex in lista_exercicios:
                st.markdown(f"- {ex}")

    if st.button("Salvar este treino no histórico"):
        for dia, lista_exercicios in treino.items():
            st.session_state.historico.append({
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": "Automático",
                "grupo": dia,
                "exercicios": lista_exercicios
            })
        st.success("Treino automático salvo no histórico!")

elif aba == "Treino Personalizado":
    st.header("Gerar Treino Personalizado")

    grupos_escolhidos = st.multiselect("Grupos Musculares", list(exercicios.keys()))
    dias = st.slider("Dias de Treino", 1, 7, 3)
    volume = st.selectbox("Volume do Treino", ["baixo", "médio", "alto"])
    intensidade = st.selectbox("Intensidade do Treino", ["leve", "moderada", "alta"])

    if st.button("Gerar Treino"):
        if not grupos_escolhidos:
            st.warning("Selecione pelo menos um grupo muscular.")
        else:
            treino = gerar_treino_personalizado(grupos_escolhidos, dias, volume, intensidade, usuario["objetivo"])
            for dia, lista_exercicios in treino.items():
                with st.expander(dia):
                    for ex in lista_exercicios:
                        st.markdown(f"- {ex}")

            if st.button("Salvar este treino personalizado"):
                for dia, lista_exercicios in treino.items():
                    st.session_state.historico.append({
                        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "tipo": "Personalizado",
                        "grupo": dia,
                        "exercicios": lista_exercicios
                    })
                st.success("Treino personalizado salvo no histórico!")

elif aba == "Registrar Manual":
    st.header("Registrar Treino Manual")
    grupo = st.selectbox("Grupo Muscular", list(exercicios.keys()))
    objetivo = st.selectbox("Objetivo", ["hipertrofia", "emagrecimento", "resistencia"])
    opcoes = [ex[0] for ex in exercicios[grupo][objetivo]]
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
        for treino_registrado in reversed(st.session_state.historico):
            st.subheader(f"{treino_registrado['data']} - {treino_registrado['grupo']} ({treino_registrado['tipo']})")
            for ex in treino_registrado["exercicios"]:
                st.markdown(f"- {ex}")
    else:
        st.info("Nenhum treino registrado ainda.")
