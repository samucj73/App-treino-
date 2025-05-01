import streamlit as st
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        faixa_imc = "Abaixo do peso"
    elif 18.5 <= imc < 24.9:
        faixa_imc = "Peso normal"
    elif 25 <= imc < 29.9:
        faixa_imc = "Sobrepeso"
    else:
        faixa_imc = "Obesidade"
    return imc, faixa_imc

def calcular_tmb(idade, peso, altura, genero):
    if genero.lower() == "masculino":
        tmb = 10 * peso + 6.25 * altura * 100 - 5 * idade + 5
    else:
        tmb = 10 * peso + 6.25 * altura * 100 - 5 * idade - 161
    return tmb

def calcular_percentual_gordura(peso, circunferencia_cintura, idade, genero):
    if genero.lower() == "masculino":
        gordura = (0.1 * peso) + (0.23 * circunferencia_cintura) - (0.25 * idade) - 5.4
    else:
        gordura = (0.1 * peso) + (0.23 * circunferencia_cintura) - (0.25 * idade) - 4.5
    return gordura

def calcular_massa_muscular(peso, percentual_gordura):
    return peso * (1 - percentual_gordura / 100)

def calcular_idade_metabolica(tmb, idade):
    return idade + (tmb - 1500) / 25

def recomendacao_hidratacao(peso):
    return peso * 35  # ml por kg

def recomendacao_proteina(peso, objetivo):
    if objetivo.lower() == "aumento muscular":
        proteina = peso * 2.0
    elif objetivo.lower() == "manutenção":
        proteina = peso * 1.5
    else:
        proteina = peso * 1.2
    return proteina
