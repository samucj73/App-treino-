# Use o Python 3.8 como base
FROM python:3.8-slim

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libssl-dev \
    libffi-dev \
    libmysqlclient-dev \
    libjpeg-dev \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho
WORKDIR /app

# Copie o código do app para o container
COPY . .

# Instale as dependências do Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Defina a porta que o Streamlit vai usar
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "app.py"]
