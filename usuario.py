from db import cadastrar_usuario, obter_usuario, atualizar_usuario, recuperar_por_email

def cadastrar(nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino):
    try:
        if not nome or not email or not senha:
            raise ValueError("Nome, e-mail e senha são obrigatórios.")
        cadastrar_usuario(nome, email, senha, idade, peso, altura, genero, objetivo, experiencia, dias_treino)
    except Exception as e:
        raise Exception(f"Erro ao cadastrar: {e}")

def obter(nome_ou_email, senha):
    try:
        return obter_usuario(nome_ou_email, senha)
    except Exception as e:
        raise Exception(f"Erro ao obter usuário: {e}")

def atualizar(id_usuario, nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino):
    try:
        atualizar_usuario(id_usuario, nome, idade, peso, altura, genero, objetivo, experiencia, dias_treino)
    except Exception as e:
        raise Exception(f"Erro ao atualizar usuário: {e}")

def recuperar_senha(email):
    try:
        usuario = recuperar_por_email(email)
        if usuario:
            return f"Usuário encontrado: {usuario[1]} - Sua senha é: {usuario[2]}"
        else:
            raise ValueError("E-mail não encontrado.")
    except Exception as e:
        raise Exception(f"Erro ao recuperar senha: {e}")
