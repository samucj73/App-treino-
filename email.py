import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email_recuperacao(email_destino, senha_usuario):
    # Definir as configurações do e-mail
    email_remetente = "seu_email@dominio.com"
    senha_email = "sua_senha_email"
    smtp_servidor = "smtp.dominio.com"
    smtp_porta = 587

    # Criar a mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = email_remetente
    mensagem['To'] = email_destino
    mensagem['Subject'] = 'Recuperação de Senha'

    corpo_email = f"Sua senha de acesso é: {senha_usuario}"

    mensagem.attach(MIMEText(corpo_email, 'plain'))

    # Conectar ao servidor SMTP e enviar o e-mail
    try:
        servidor = smtplib.SMTP(smtp_servidor, smtp_porta)
        servidor.starttls()
        servidor.login(email_remetente, senha_email)
        servidor.sendmail(email_remetente, email_destino, mensagem.as_string())
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
